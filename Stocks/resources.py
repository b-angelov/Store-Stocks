from abc import ABC, abstractmethod

from flask.sansio.blueprints import Blueprint
from sqlalchemy import Select, select, inspect, desc, cast, Float
from sqlalchemy.orm import Session, aliased, selectinload

from models import PhonesModel, ModelsModel, BrandsModel, DeviceTypesModel, AccessoryModel, \
    MandatoryAccessoriesModel, accessories_compatible_models

from extensions import db

model_device_type = aliased(DeviceTypesModel,name="model_device_type")


class BaseResource(ABC):

    filters_mapper = {}

    def __init__(self, query, *args,**kwargs):
        self.query = query
        if kwargs.get("model",False):
            self.model = kwargs.get("model")
        else:
            self.model = self.query.column_descriptions[0]["entity"]

    def _clone(self, query):
        return self.__class__(query)

    def all(self, *args, **kwargs):
        return self._execute_statement(self.query)

    def build_result(self, *args, **kwargs):
        return self.all()

    @staticmethod
    def _get_raw_result(statement, *args, **kwargs):
        # with Session(engine) as session:
        #     result = [r for r in session.execute(statement)]
        #     return result
        result = [r for r in db.session.execute(statement)]
        return result

    @abstractmethod
    def _execute_statement(self, *args, **kwargs):
        pass

    @staticmethod
    def _api_selectinload(statement,objects:tuple|list|object):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        statement = statement.options(*(selectinload(object_) for object_ in objects))
        return statement

    def apply_filters(self, filters: dict | None=None):
        query = self
        if filters:
            for filter_,value in filters.items():
                if filter_ in self.filters_mapper.keys():
                    query = query.filters_mapper[filter_](value,**filters)
        return query

    def api_include_related(self):
        return self

    def _order_query(self,rel:list|tuple|str,asc=True):
        asc_desc = lambda field, asc: field if asc else desc(field)
        if not isinstance(rel,(list,tuple)):
            rel = (rel,)
        for r in rel:
            self.query = self.query.order_by(asc_desc(r, asc))

    def sort_by_multiple(self, sort_map=None,items=None, *args, **kwargs):
        sort_map = sort_map or {}
        base_map = {
                "id":lambda asc=True: self._order_query(self.model.id,asc)
        }
        base_map.update(sort_map)
        if not items:
            items = kwargs.get("items",[["id","asc"]])
        for field,ord in items:
            base_map.get(field, lambda *_:None)(ord == "asc")
        return self._clone(self.query)

class BrandsResource(BaseResource):

    def __init__(self, query=None,*args,**kwargs):
        if query is None:
            query = select(BrandsModel)
        super().__init__(query)

        self.filters_mapper = {
            "of_brand": self.of_brand,
            "of_nationality": self.of_nationality,
            "with_id": self.with_id,
        }

    def sort_by_multiple(self, sort_map=None, *args, **kwargs):
        sort_map = {
            "name": lambda asc: self._order_query(self.model.name, asc),
            "nationality": lambda asc: self._order_query(self.model.nationality, asc)
        }
        return super().sort_by_multiple(sort_map, *args, **kwargs)

    @staticmethod
    def _execute_statement(statement, *args, **kwargs):
        results = BaseResource._get_raw_result(statement, *args, **kwargs)
        return [
            {
                "brand": {b.key: getattr(brand, b.key) for b in inspect(brand).mapper.column_attrs},
            }
                for brand, in results ]

    def of_brand(self, brand_name: str, *args, **kwargs):
        return self._clone(self.query.where(BrandsModel.__table__.c.name.ilike(f"%{brand_name}%")))

    def of_nationality(self, nationality: str, *args, **kwargs):
        return self._clone(self.query.where(BrandsModel.__table__.c.nationality.ilike(f"%{nationality}%")))

    def with_id(self, id: int, *args, **kwargs):
        return self._clone(self.query.where(BrandsModel.__table__.c.id==id))


class DeviceTypesResource(BaseResource):

    def __init__(self, query = None, *args,**kwargs):
        if query is None:
            query = select(DeviceTypesModel)
        super().__init__(query)

        self.filters_mapper = {
            "of_type": self.of_type,
            "with_id": self.with_id,
        }

    def sort_by_multiple(self, sort_map=None, *args, **kwargs):
        sort_map = {
            "device_type": lambda asc: self._order_query(self.model.device_type, asc),
        }
        super().sort_by_multiple(sort_map, *args, **kwargs)

    @staticmethod
    def _execute_statement(statement, *args, **kwargs):
        results = BaseResource._get_raw_result(statement)
        return [
            {
                "device_type":{dt.key: getattr(device_type, dt.key) for dt in inspect(device_type).mapper.column_attrs}
            }
            for device_type, in results
        ]

    def with_id(self, id_: int, *args, **kwargs):
        return self._clone(self.query.where(DeviceTypesModel.__table__.c.id==id_))

    def of_type(self, type_: str, *args, **kwargs):
        return self._clone(self.query.where(DeviceTypesModel.__table__.c.device_type.ilike(f"%{type_}%")))


class ModelsResource(BaseResource):

    def __init__(self, query = None,*args,**kwargs):
        self.api = False
        if kwargs.get("API", False):
            self.api = True
        if query is None:
            if self.api:
                query = select(ModelsModel).join(BrandsModel).join(DeviceTypesModel,ModelsModel.device_type==DeviceTypesModel.id)
            else:
                query = select(ModelsModel,BrandsModel,DeviceTypesModel).join(BrandsModel,BrandsModel.__table__.c.id==ModelsModel.__table__.c.brand).join(DeviceTypesModel,DeviceTypesModel.__table__.c.id==ModelsModel.__table__.c.device_type)
        super().__init__(query)

        self.filters_mapper = {
            "of_brand": self.of_brand,
            "with_name": self.with_name,
            "with_id": self.with_id,
            "with_device_type": self.with_device_type,
        }

    def sort_by_multiple(self, sort_map=None, *args, **kwargs):
        sort_map = {
            "device_type": lambda asc: self._order_query(self.model.device_type, asc),
            "modification": lambda asc: self._order_query(self.model.modification, asc),
            "model": lambda asc: self._order_query(self.model.model, asc),
            "brand": lambda asc: self._order_query((BrandsModel.name,BrandsModel.id), asc),
        }
        return super().sort_by_multiple(sort_map, *args, **kwargs)

    def api_include_related(self):
        if self.api:
            return self._clone(self._api_selectinload(self.query, (ModelsModel.brand_data,ModelsModel.device_type_data)))
        return self

    def api_load_compatible_accessories(self):
        return self._clone(self.query.options(
            selectinload(ModelsModel.compatible_accessories),
        ))

    def of_brand(self,brand:str,*args,**kwargs):
        return self._clone(self.query.where(BrandsModel.__table__.c.name.ilike(f"%{brand}%")))

    def with_name(self,model:str, modification:str=None, *args, **kwargs):
        query =  self.query.where(ModelsModel.__table__.c.model.ilike(f"%{model}%"))

        if "modification" in kwargs.keys():
            modification = kwargs["modification"]

        if modification is not None:
            query = query.where(ModelsModel.__table__.c.modification.ilike(f"%{modification}%"))
        return self._clone(query)

    def with_id(self,id:int, *args, **kwargs):
        return self._clone(self.query.where(ModelsModel.__table__.c.id==id))

    def with_device_type(self, device_type:str, *args, **kwargs):
        return self._clone(self.query.where(DeviceTypesModel.__table__.c.device_type.ilike(f"%{device_type}%")))

    def in_id_list(self,ids:list|tuple,*args,**kwargs):
        return self._clone(self.query.where(ModelsModel.__table__.c.id.in_(ids)))


    @staticmethod
    def _execute_statement(statement, *args, **kwargs):
        results = BaseResource._get_raw_result(statement, *args, **kwargs)
        return [
            {
                "model":{m.key:getattr(model,m.key) for m in inspect(model).mapper.column_attrs},
                "brand":{b.key:getattr(brand,b.key) for b in inspect(brand).mapper.column_attrs},
                "device_type":{dt.key:getattr(device_type,dt.key) for dt in inspect(device_type).mapper.column_attrs},
            }
            for model,brand,device_type in results
        ]

class AccessoriesResource(BaseResource):

    def __init__(self, query=None,*args,**kwargs):
        self.api = False
        if kwargs.get("API", False):
            self.api = True
        if query is None:
            if self.api:
                query = select(AccessoryModel)\
                    .outerjoin(DeviceTypesModel, AccessoryModel.__table__.c.device_type == DeviceTypesModel.__table__.c.id) \
                    .outerjoin(ModelsModel, AccessoryModel.__table__.c.model == ModelsModel.__table__.c.id) \
                    .outerjoin(BrandsModel, ModelsModel.__table__.c.brand == BrandsModel.__table__.c.id) \
                    .outerjoin(model_device_type,
                               ModelsModel.__table__.c.device_type == model_device_type.id)
            else:
                query =  select(AccessoryModel,DeviceTypesModel,ModelsModel,BrandsModel,model_device_type)\
                     .outerjoin(DeviceTypesModel,AccessoryModel.__table__.c.device_type==DeviceTypesModel.__table__.c.id)\
                     .outerjoin(ModelsModel,AccessoryModel.__table__.c.model==ModelsModel.__table__.c.id)\
                     .outerjoin(BrandsModel, ModelsModel.__table__.c.brand==BrandsModel.__table__.c.id)\
                     .outerjoin(model_device_type, ModelsModel.__table__.c.device_type==model_device_type.id)

        super().__init__(query)

        self.filters_mapper = {
            "of_type": self.of_type,
            "with_id": self.with_id,
            "in_ids": self.in_ids,
            "with_model_id": self.with_model_id,
            "in_model_ids": self.in_model_ids,
            "with_accessory_type": self.with_accessory_type,
            "with_accessory_type_exact": lambda x,*args,**kwargs: self.with_accessory_type(x,exact=True),
            "in_accessory_type_ids": self.in_accessory_type_ids,
            "for_model": self.for_model,
            "for_model_relative_modif": lambda x,*args,**kwargs: self.for_model(x,rel_modif=True,*args,**kwargs),
            "for_device_type": self.for_device_type,
            "for_device_type_exact": lambda x,*args,**kwargs: self.for_device_type(x,exact=True),
            "for_device_type_ids": self.for_device_type_ids,
            "with_count_below": self.with_count_below,
            "with_count_above": self.with_count_above,
            "with_price": self.with_price,
            "with_price_below": self.with_price_below,
            "with_price_above": self.with_price_above,
            "of_brand": self.of_brand,
        }

    def sort_by_multiple(self, sort_map=None, *args, **kwargs):
        sort_map = {
            "device_type": lambda asc: self._order_query(self.model.device_type, asc),
            "brand": lambda asc: self._order_query((BrandsModel.name,BrandsModel.id), asc),
            "model": lambda asc: self._order_query((ModelsModel.model,ModelsModel.id), asc),
            "count": lambda asc: self._order_query((self.model.count,), asc),
            "price_per_item": lambda asc: self._order_query((self.model.price_per_item,), asc),
        }
        return super().sort_by_multiple(sort_map, *args, **kwargs)

    def api_include_related(self):
        if self.api:
            return self._clone(self._api_selectinload(self.query, (AccessoryModel.device_type_data,AccessoryModel.model_data))
                               .options(
                                        selectinload(AccessoryModel.model_data).selectinload(ModelsModel.brand_data),
                                        selectinload(AccessoryModel.model_data).selectinload(ModelsModel.device_type_data),
                                        )
                               )
        return self

    def api_load_compatible_models(self):
        return self._clone(self.query.selectinload(AccessoryModel.compatible_models))

    def of_type(self, type, *args, **kwargs):
        return self._clone(self.query.where(DeviceTypesModel.__table__.c.device_type.ilike(f"%{type}%")))

    def of_brand(self, brand_name, *args, **kwargs):
        return  self._clone(self.query.where(BrandsModel.__table__.c.name.ilike(f"%{brand_name}%")))

    def with_id(self, id:int, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.id==id))

    def in_ids(self, ids:tuple|list, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.id.in_(ids)))

    def with_model_id(self, model_id:int, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.model==model_id))

    def in_model_ids(self, model_ids:tuple|list, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.id.in_(model_ids)))

    def with_accessory_type(self, accessory_type:str, *args, **kwargs):
        if kwargs.get("exact",False):
            return self._clone(self.query.where(DeviceTypesModel.device_type == accessory_type))
        return self._clone(self.query.where(DeviceTypesModel.__table__.c.device_type.ilike(f"%{accessory_type}%")))

    def in_accessory_type_ids(self, accessory_type_ids:tuple|list, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.device_type.in_(accessory_type_ids)))

    def for_model(self, model:str, modification:str=None, device_type:str=None, *args, **kwargs):
        if "modification" in kwargs.keys():
            modification = kwargs["modification"]
        if "for_device_type" in kwargs.keys():
            device_type = kwargs["for_device_type"]
        query = self.query.where(ModelsModel.__table__.c.model.ilike(f"%{model}%"))
        if modification is not None:
            if kwargs.get("rel_modif",False):
                query = query.where(ModelsModel.__table__.c.modification.ilike(f"%{modification}%"))
            else:
                query = query.where(ModelsModel.__table__.c.modification == modification)

        if device_type is not None:
            query = query.where(model_device_type.device_type.ilike(f"%{device_type}%"))
        return self._clone(query)

    def for_device_type(self, device_type_name:str, *args, **kwargs):
        if kwargs.get("exact",False):
            return self._clone(
                self.query.where(model_device_type.device_type == device_type_name))
        return self._clone(self.query.where(model_device_type.device_type.ilike(f"%{device_type_name}%")))

    def for_device_type_ids(self, device_type_ids:tuple|list, *args, **kwargs):
        return self._clone(self.query.where(model_device_type.id.in_(device_type_ids)))

    def with_count_below(self, count_:int, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.count<count_))

    def with_count_above(self, count_:int, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.count>=count_))

    def with_price_below(self, price:float, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.price_per_item<price))

    def with_price_above(self, price:float, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.price_per_item>=price))

    def with_price(self, price:float, *args, **kwargs):
        return self._clone(self.query.where(AccessoryModel.__table__.c.price_per_item==price))



    @staticmethod
    def _execute_statement(statement, *args, **kwargs):
        result = BaseResource._get_raw_result(statement, *args, **kwargs)
        return [
            {
                "accessory":{a.key:getattr(accessory,a.key) for a in inspect(accessory).mapper.column_attrs} if accessory else {},
                "accessory_type":{at.key:getattr(accessory_type, at.key) for at in inspect(accessory_type).mapper.column_attrs} if accessory_type else {},
                "model": {m.key:getattr(model, m.key) for m in inspect(model).mapper.column_attrs} if model else {},
                "model_brand": {mb.key:getattr(model_brand, mb.key) for mb in inspect(model_brand).mapper.column_attrs} if model_brand else {},
                "model_device_type": {mdt.key:getattr(model_dt, mdt.key) for mdt in inspect(model_dt).mapper.column_attrs} if model_dt else {},
            }
            for accessory,accessory_type,model,model_brand,model_dt in result
        ]

class PhoneDeviceResource(BaseResource):

    def __init__(self, query=None,*args,**kwargs):
        self.api = False
        if kwargs.get("API", False):
            self.api = True
        if query is None:
            if self.api:
                query = select(PhonesModel).join(ModelsModel,PhonesModel.__table__.c.model==ModelsModel.__table__.c.id).join(BrandsModel,ModelsModel.__table__.c.brand==BrandsModel.__table__.c.id)
            else:
                query = select(PhonesModel,ModelsModel,BrandsModel).join(ModelsModel,PhonesModel.__table__.c.model==ModelsModel.__table__.c.id).join(BrandsModel,ModelsModel.__table__.c.brand==BrandsModel.__table__.c.id)
        super().__init__(query)

        self.filters_mapper = {
            "in_stock": self.in_stock,
            "of_brand": self.of_brand,
            "of_model": self.of_model,
            "with_price_above": self.with_price_above,
            "with_price_below": self.with_price_below,
            "with_id": self.with_id,
            "old_only": self.old_only,
            "new_only": self.new_only,
            "available": self.available,
            "unavailable": self.unavailable,
            "with_memory_capacity_above": self.with_memory_capacity_above,
            "with_memory_capacity_below": self.with_memory_capacity_below,
            "with_ram_capacity_above": self.with_ram_capacity_above,
            "with_ram_capacity_below": self.with_ram_capacity_below,
            "with_battery_status_above": self.with_battery_status_above,
            "with_battery_status_below": self.with_battery_status_below,

        }

    def sort_by_multiple(self, sort_map=None, *args, **kwargs):
        sort_map = {
            "brand": lambda asc: self._order_query((BrandsModel.name,BrandsModel.id), asc),
            "model": lambda asc: self._order_query((ModelsModel.model,ModelsModel.id), asc),
            "price": lambda asc: self._order_query((cast(self.model._price, Float),), asc),
            "capacity_gb": lambda asc: self._order_query((self.model._capacity_gb,), asc),
            "battery_capacity": lambda asc: self._order_query((self.model.battery_capacity,), asc),
            "RAM": lambda asc: self._order_query((self.model._ram,), asc),
            "processor": lambda asc: self._order_query((self.model.processor,), asc),
            "phone_status": lambda asc: self._order_query((self.model.phone_status,), asc),
            "sold": lambda asc: self._order_query((self.model.sold,), asc),
            "notes": lambda asc: self._order_query((self.model.notes,), asc),
        }
        return super().sort_by_multiple(sort_map, *args, **kwargs)

    def api_include_related(self):
        if self.api:
            return self._clone(self._api_selectinload(self.query, PhonesModel.model_data).options(selectinload(PhonesModel.model_data).selectinload(ModelsModel.brand_data)))
        return self

    @staticmethod
    def _get_all():
        statement = select(PhonesModel,ModelsModel,BrandsModel).join(ModelsModel,PhonesModel.__table__.c.model==ModelsModel.__table__.c.id).join(BrandsModel,ModelsModel.__table__.c.brand==BrandsModel.__table__.c.id)
        return statement

    @staticmethod
    def _get_in_stock():
        statement = PhoneDeviceResource._get_all().where(PhonesModel.__table__.c.sold==0)
        return statement

    def in_stock(self, *args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.sold==0))

    def of_brand(self,brand_name: str, *args, **kwargs):
        return self._clone(self.query.where(BrandsModel.__table__.c.name.ilike(f"%{brand_name}%")))

    def of_model(self,model_name: str, modification_name: str=None, *args, **kwargs):
        if "modification" in dict(kwargs).keys():
            modification_name = kwargs.pop("modification")
        query = self.query.where(ModelsModel.__table__.c.model.ilike(f"%{model_name}%"))
        if modification_name:
            query = query.where(ModelsModel.__table__.c.modification.ilike(f"%{modification_name}%"))
        return self._clone(query)

    def with_price_above(self, price: float,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.price>=price))

    def with_price_below(self, price: float,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.price<price))

    def with_id(self, id: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.id==id))

    def old_only(self,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.phone_status.ilike(f"%old%")))

    def new_only(self,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.phone_status.ilike(f"%new%")))

    def available(self,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.sold==0))

    def unavailable(self,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.sold==1))

    def with_memory_capacity_above(self, capacity: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.capacity_gb>=capacity))

    def with_memory_capacity_below(self, capacity: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.capacity_gb<capacity))

    def with_ram_capacity_above(self, capacity: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.RAM>=capacity))

    def with_ram_capacity_below(self, capacity: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.RAM<capacity))

    def with_battery_status_above(self, battery_status: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.batter_status>=battery_status))

    def with_battery_status_below(self, battery_status: int,*args, **kwargs):
        return self._clone(self.query.where(PhonesModel.__table__.c.batter_status<battery_status))




    @staticmethod
    def _execute_statement(statement,*args,**kwargs):
        result = BaseResource._get_raw_result(statement,*args,**kwargs)
        return [
            {
                "phone": {p.key: getattr(phone, p.key) for p in inspect(phone).mapper.column_attrs},
                "model": {m.key: getattr(model, m.key) for m in inspect(model).mapper.column_attrs},
                "brand": {b.key: getattr(brand, b.key) for b in inspect(brand).mapper.column_attrs},
            }
            for phone, model, brand in result]

    @staticmethod
    def get_items(filter_:str|None = None) -> list:

        method = {
            "in_stock": PhoneDeviceResource._get_in_stock,
            "all": PhoneDeviceResource._get_all,
        }.get(filter_, PhoneDeviceResource._get_all)

        return PhoneDeviceResource._execute_statement(method())


class MandatoryAccessoriesResource(BaseResource):

    def __init__(self, query=None, *args,**kwargs):
        self.api = False
        if kwargs.get("API", False):
            self.api = True
        if query is None:
            query = (select(MandatoryAccessoriesModel)
                     .join(ModelsModel,MandatoryAccessoriesModel.model_id==ModelsModel.id)
                     .join(DeviceTypesModel,ModelsModel.device_type==DeviceTypesModel.id)
                     .join(BrandsModel,ModelsModel.brand==BrandsModel.id)
                     .join(AccessoryModel,MandatoryAccessoriesModel.model_id==AccessoryModel.model)
                     .join(model_device_type,AccessoryModel.device_type==model_device_type.id)
                     .distinct())
        super().__init__(query)

        self.model_resource_instance = ModelsResource(api=self.api)._clone(self.query)
        self.filters_mapper = self.model_resource_instance.filters_mapper
        self.sort_by_multiple = self.model_resource_instance.sort_by_multiple
        exclusions = {
            "with_accessory_type": self.with_accessory_type,
            "with_accessory_type_exact": lambda x, *args, **kwargs: self.with_accessory_type(x, exact=True),
        }
        for key,value in self.filters_mapper.items():
            if key not in exclusions.keys():
                setattr(self,value.__name__,value)
        self.filters_mapper.update(exclusions)


    @staticmethod
    def _execute_statement(statement,*args,**kwargs):
        return ModelsResource._execute_statement(statement,*args,**kwargs)

    def api_include_related(self,*args,**kwargs):
        if self.api:
            return self._clone(self._api_selectinload(self.query, (MandatoryAccessoriesModel.accessories,MandatoryAccessoriesModel.model_data)))
        return self

    def with_accessory_type(self, accessory_type: str, *args, **kwargs):
        if kwargs.get("exact", False):
            return self._clone(self.query.where(model_device_type.device_type == accessory_type))
        return self._clone(self.query.where(model_device_type.device_type.ilike(f"%{accessory_type}%")))




