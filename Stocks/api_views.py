from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort, Page
from marshmallow import Schema
from sqlalchemy import select, func, desc
from sqlalchemy.exc import NoResultFound
from validators import ViewValidators as vv

from extensions import db
from models import PhonesModel, AccessoryModel
from resources import PhoneDeviceResource, BaseResource, BrandsResource, DeviceTypesResource, ModelsResource, \
    AccessoriesResource, MandatoryAccessoriesResource
from schema import PhoneSchema, PhoneJoinedSchema, BrandsSchema, DeviceTypeSchema, ModelsSchema, ModelsJoinedSchema, \
    AccessorySchema, AccessoryJoinedSchema, MandatoryAccessorySchema, MandatoryAccessoryJoinedSchema, ErrorSchema

blp = Blueprint('api_routes',__name__)


class BaseAPIView(MethodView):

    model = None
    allowed_sort_columns = []

    def __init__(self,resource:BaseResource,main_schema:Schema=None,joined_schema:Schema=None,*args,**kwargs):
        self.main_schema = main_schema
        self.joined_schema = joined_schema
        self.resource = resource
        self.related = request.args.get("related",False) in (1,'1','true')
        if not joined_schema:
            self.joined_schema = main_schema
        super().__init__(*args)

    def _load_related_schema(self,query = None):
        schema = self.main_schema if not self.related else self.joined_schema
        if query:
            query = query.api_include_related()
        return schema, query

    def _get_sort_fields(self):
        sort_fields = map(lambda x: [x.replace("-",""),"asc" if not x.startswith("-") else "desc"],request.args.getlist("sort"))
        sort_fields = filter(lambda x: x[0] in self.allowed_sort_columns,sort_fields)
        sort_fields = list(sort_fields)
        return list(sort_fields) if len(sort_fields) else [["id","asc"]]

    @blp.paginate()
    def get(self, pagination_parameters, query=None):
        if query is None:
            query = self.resource(api=True).apply_filters(request.args)
        related = request.args.get("related", "false")
        schema = self.main_schema
        schema, query = self._load_related_schema(query)
        sort_params = self._get_sort_fields()
        query = query.sort_by_multiple(items=sort_params)
        query = query.query
        items = select(func.count()).select_from(query.subquery())
        pagination_parameters.item_count = db.session.execute(items).scalar()
        query = query.limit(pagination_parameters.page_size).offset(pagination_parameters.first_item)
        # sort_params = self._get_sort_fields()
        # model = query.column_descriptions[0]["entity"]
        # query = query.order_by(*(getattr(model,field,None) if direction =="asc" else  desc(getattr(model,field,None)) for field,direction in sort_params))
        res = db.session.execute(query).scalars().all()
        return schema(many=True).dump(res)

    @vv.has_id
    def _update_singular_logic(self, id, data, item=None):
        if item is None:
            item = self.resource(api=True).with_id(id).query
            item = db.session.execute(item).scalar_one()
        schema, _ = self._load_related_schema()
        # if not item:
        #     abort(404, message="Record with the specified ID was not found.")
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return schema().dump(item)

    @vv.has_id
    def _delete_singular_logic(self, id, item=None):
        if item is None:
            item = self.resource(api=True).with_id(id).query
            item = db.session.execute(item).scalar_one()
        schema, _ = self._load_related_schema()
        db.session.delete(item)
        db.session.commit()
        return schema().dump(item)

    @vv.has_id
    @blp.alt_response(404, schema=ErrorSchema, description="Record with the specified ID was not found.")
    def _get_singular_logic(self, id, *args, **kwargs):
        query = self.resource(api=True).with_id(id).apply_filters(request.args)
        schema, query = self._load_related_schema(query)
        query = db.session.execute(query.query).scalar_one()
        return schema().dump(query)


class PhonesAPIView(BaseAPIView):

    methods = ["GET","POST"]
    allowed_sort_columns = ["id","model","capacity_gb","battery_capacity","RAM","price","processor","id","phone_status","sold","notes","brand"]
    model = PhonesModel


    def __init__(self,*args,**kwargs):
        super().__init__(resource=PhoneDeviceResource,main_schema=PhoneSchema,joined_schema=PhoneJoinedSchema,*args,**kwargs)

    @blp.arguments(PhoneJoinedSchema(many=True))
    @blp.response(200, PhoneJoinedSchema)
    def post(self,req, *args, **kwargs):
        model = self.model
        query = [model(**req) for req in req]
        db.session.add_all(query)
        db.session.commit()
        return query

class PhonesItemAPIView(BaseAPIView):

    methods = ["GET","PUT","DELETE","PATCH"]
    model = PhonesModel

    def __init__(self,*args,**kwargs):
        super().__init__(resource=PhoneDeviceResource,main_schema=PhoneSchema,joined_schema=PhoneJoinedSchema,*args,**kwargs)


    def get(self, id, *args, **kwargs):
        return self._get_singular_logic(id,*args,**kwargs)


    @blp.arguments(PhoneJoinedSchema)
    def put(self, data, id,*args, **kwargs):
       return self._update_singular_logic(id,data)

    @blp.arguments(PhoneJoinedSchema(partial=True))
    def patch(self, data, id,*args, **kwargs):
        return self._update_singular_logic(id,data)


    def delete(self,id,*args, **kwargs):
        return self._delete_singular_logic(id)





class BrandsAPIView(BaseAPIView):

    methods = ["GET"]
    allowed_sort_columns = ["name","nationality","id"]

    def __init__(self,*args,**kwargs):
        super().__init__(resource=BrandsResource,main_schema=BrandsSchema,*args,**kwargs)

class PhonesDistinctBrandsAPIView(BrandsAPIView):

    def get(self,*args,**kwargs):
        return super().get(query=PhoneDeviceResource(api=True).get_distinct_brands(),*args,**kwargs)

class BrandsItemAPIView(BrandsAPIView):
    methods = ["GET","PUT","DELETE","PATCH"]

    def get(self,id,*args, **kwargs):
        return self._get_singular_logic(id,*args,**kwargs)

    @blp.arguments(BrandsSchema)
    def put(self,data,id,*args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(BrandsSchema(partial=True))
    def patch(self,data,id,*args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(BrandsSchema)
    def delete(self,id,*args, **kwargs):
        return self._delete_singular_logic(id)


class DeviceTypesAPIView(BaseAPIView):

    methods = ["GET"]
    allowed_sort_columns = ["device_type","id"]


    def __init__(self,*args,**kwargs):
        super().__init__(resource=DeviceTypesResource, main_schema=DeviceTypeSchema, *args, **kwargs)


class DeviceTypesItemAPIView(DeviceTypesAPIView):

    methods = ["GET","PUT","DELETE","PATCH"]

    def get(self,id,*args, **kwargs):
        return self._get_singular_logic(id,*args,**kwargs)

    @blp.arguments(DeviceTypeSchema)
    def put(self, data,id, *args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(DeviceTypeSchema(partial=True))
    def patch(self, data,id, *args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(DeviceTypeSchema)
    def delete(self, id, *args, **kwargs):
        return self._delete_singular_logic(id)


class ModelsAPIView(BaseAPIView):

    methods = ["GET"]
    allowed_sort_columns = ["brand","model","modification","device_type","id"]


    def __init__(self,*args,**kwargs):
        super().__init__(resource=ModelsResource,main_schema=ModelsSchema,joined_schema=ModelsJoinedSchema,*args,**kwargs)

    def get(self):
        return super().get(query=self.resource(api=True).apply_filters().api_load_compatible_accessories())


class ModelsItemAPIView(ModelsAPIView):

    methods = ["GET","PUT","DELETE","PATCH"]

    def get(self,id,*args, **kwargs):
        return self._get_singular_logic(id,*args,**kwargs)

    @blp.arguments(ModelsSchema)
    def put(self,data,id,*args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(ModelsSchema(partial=True))
    def patch(self,data,id,*args, **kwargs):
        if data.get("compatible_accessories", False):
            c_accessory = data.pop("compatible_accessories")
            acc_ids = [a['id'] if isinstance(a, dict) else a for a in c_accessory]
            accessories = AccessoriesResource.in_ids(acc_ids)
            accessories = db.session.execute(accessories).scalars().all()
            item = self.resource(api=True).with_id(id).query
            item = db.session.execute(item).scalar_one()
            item.compatible_accessories.extend(accessories)
        return self._update_singular_logic(id,data)

    @blp.arguments(ModelsSchema)
    def delete(self,id,*args, **kwargs):
        return self._delete_singular_logic(id)


class MandatoryAccessoriesAPIView(BaseAPIView):

    methods = ["GET"]


    def __init__(self,*args,**kwargs):
        super().__init__(resource=MandatoryAccessoriesResource,main_schema=MandatoryAccessorySchema,joined_schema=MandatoryAccessoryJoinedSchema,*args,**kwargs)

class MandatoryAccessoriesItemAPIView(MandatoryAccessoriesAPIView):
    methods = ["GET","PUT","DELETE","PATCH"]

    def get(self,id,*args, **kwargs):
        return self._get_singular_logic(id,*args,**kwargs)

    @blp.arguments(MandatoryAccessorySchema)
    def put(self,data,id,*args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(MandatoryAccessorySchema(partial=True))
    def patch(self,data,id,*args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(MandatoryAccessorySchema)
    def delete(self,id,*args, **kwargs):
        return self._delete_singular_logic(id)


class AccessoriesAPIView(BaseAPIView):

    methods = ["GET"]
    allowed_sort_columns = ["id","for_device_type","for_device_model","for_device_brand","count","price_per_item","brand","accessory_type"]

    def __init__(self,*args,**kwargs):
        super().__init__(resource=AccessoriesResource,main_schema=AccessorySchema,joined_schema=AccessoryJoinedSchema,*args,**kwargs)

class AccessoriesItemAPIView(AccessoriesAPIView):

    methods = ["GET","PUT","DELETE","PATCH"]

    def get(self,id,*args, **kwargs):
        return self._get_singular_logic(id,*args,**kwargs)

    @blp.arguments(AccessorySchema)
    def put(self,data,id,*args, **kwargs):
        return self._update_singular_logic(id,data)

    @blp.arguments(AccessorySchema(partial=True))
    def patch(self,data,id,*args, **kwargs):
        if data.get("compatible_models", False):
            c_model = data.pop("compatible_models")
            mod_ids = [m['id'] if isinstance(m, dict) else m for m in c_model]
            models = ModelsResource.in_id_list(mod_ids)
            models = db.session.execute(models).scalars().all()
            item = self.resource(api=True).with_id(id).query
            item = db.session.execute(item).scalar_one()
            item.compatible_models.extend(models)
        return self._update_singular_logic(id,data)

    @blp.arguments(AccessorySchema)
    def delete(self,id,*args, **kwargs):
        return self._delete_singular_logic(id)
