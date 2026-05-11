from sqlalchemy import select, create_engine, Table, Column, Integer, ForeignKey, Text, Float, CheckConstraint, Boolean, \
    UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, relationship
from validators import ModelValidators as mv

from extensions import db


# engine = create_engine('sqlite:///phones-database.db', echo=True)



class Base(DeclarativeBase):
    pass

accessories_compatible_models = Table(
    'accessories_compatible_models',
    Base.metadata,
    Column('accessoir', Integer, ForeignKey('accessories.id')),
    Column('model', Integer, ForeignKey('models.id'))
)

class AccessoryModel(Base):

    __tablename__ = 'accessories'
    __table_args__ = UniqueConstraint('device_type','model', name='accessories_unique_device_type_model'),{
        # 'extend_existing': True,
        # 'autoload_with': engine,
    }
    id = mapped_column("id",primary_key=True,type_=Integer)
    device_type = mapped_column("device_type",ForeignKey("device_types.id"), type_=Integer)
    device_type_data = relationship("DeviceTypesModel")
    model = mapped_column("model",ForeignKey("models.id"), type_=Text)
    model_data = relationship("ModelsModel")
    count = mapped_column("count", type_=Integer)
    price_per_item = mapped_column("price_per_item", type_=Float)
    compatible_models = relationship("ModelsModel",secondary=accessories_compatible_models, back_populates="compatible_accessories")

    # def compatible_models(self, *args, **kwargs):
    #     query = select(accessories_compatible_models).where(accessories_compatible_models.accessoir==self.id)
    #     ids = db.session.execute(query).scalars().all()
    #     statement = select(ModelsModel).where(ModelsModel.id.in_(ids))
    #     return db.session.execute(statement).scalars().all()

    def __str__(self):
        return f"{self.device_type} accessory for model with ID {self.model} of count {self.count} with price per item {self.price_per_item}"

class BrandsModel(Base):
    __tablename__ = 'brands'
    __table_args__ = UniqueConstraint('name','nationality',name='brands_unique_name_nationality'),{
        # 'extend_existing': True,
        # 'autoload_with' : engine,

    }
    id = mapped_column("id", primary_key=True, type_=Integer)
    name = mapped_column("name", type_=Text)
    nationality = mapped_column("nationality", type_=Text)


    def __str__(self):
        return f"{self.name}"

class ModelsModel(Base):
    __tablename__ = 'models'
    __table_args__ = UniqueConstraint('device_type','brand','model','modification', name="models_unique_device_type_model_brand_modification"),{
        # 'extend_existing': True,
        # 'autoload_with': engine,

    }
    id = mapped_column("id",primary_key=True,type_=Integer)
    device_type = mapped_column("device_type",ForeignKey("device_types.id"), type_=Text)
    device_type_data = relationship("DeviceTypesModel")
    brand = mapped_column("brand",ForeignKey("brands.id"), type_=Integer)
    brand_data = relationship("BrandsModel")
    model = mapped_column("model", type_=Text)
    modification = mapped_column("modification", type_=Text)
    compatible_accessories = relationship("AccessoryModel",secondary=accessories_compatible_models, back_populates="compatible_models")


    # def compatible_accessories(self, *args, **kwargs):
    #     query = select(accessories_compatible_models.accessoir).where(accessories_compatible_models.model==self.id)
    #     ids = db.session.execute(query).scalars().all()
    #     statement = select(AccessoryModel).where(AccessoryModel.__table__.c.id.in_(ids))
    #     return db.session.execute(statement).scalars().all()


    def __str__(self):
        return f"Model {self.model} {self.modification} with brand ID {self.brand} and device type ID {self.device_type}"

class PhonesModel(Base):
    __tablename__ = 'phones'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    _price = mapped_column("price",type_=Float)
    _battery_status = mapped_column("battery_status_%",type_=Integer)
    id = mapped_column("id", primary_key=True, type_=Integer)
    model = mapped_column("model",ForeignKey("models.id"), type_=Integer)
    model_data = relationship("ModelsModel")
    _capacity_gb = mapped_column("capacity_gb",type_=Integer)
    _ram = mapped_column("RAM",type_=Integer)
    processor = mapped_column("processor", type_=Text)
    phone_status = mapped_column("phone_status",CheckConstraint("phone_status in ('old','new')", name="phones_phones_status_old_new_constraint"),type_=Text)
    sold = mapped_column("sold",type_=Boolean)
    notes = mapped_column("notes",type_=Text)

    @property
    @mv.floatify
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    @mv.integerify
    def battery_status(self):
        return self._battery_status

    @battery_status.setter
    def battery_status(self, value):
        self._battery_status = value

    @property
    @mv.sum_ram
    def RAM(self):
        return self._ram

    @RAM.setter
    def RAM(self, value):
        self._ram = value

    @property
    @mv.sum_ram
    def capacity_gb(self):
        return self._capacity_gb

    @capacity_gb.setter
    def capacity_gb(self, value):
        self._capacity_gb = value


    def __str__(self):
        return f"Phone device with model ID {self.model} memory capacity {self.capacity_gb} maximum battery charge {self.battery_status or 'N/A'} and {self.RAM}GB RAM"

class DeviceTypesModel(Base):
    __tablename__ = 'device_types'
    __table_args__ = UniqueConstraint('device_type',name='device_types_unique_device_type'),{
        # 'extend_existing': True,
        # 'autoload_with': engine,

    }
    id = mapped_column("id", primary_key=True, type_=Integer)
    device_type = mapped_column("device_type", type_=Text)


    def __str__(self):
        return f"{self.device_type}"

class MandatoryAccessoriesModel(Base):
    __tablename__ = 'mandatory_accessories'
    __table_args__ = UniqueConstraint('model_id', name='mandatory_accesories_unique_model_id'),{
        # 'extend_existing': True,
        # 'autoload_with': engine,

    }
    id = mapped_column("id", primary_key=True, type_=Integer)
    model_id = mapped_column("model_id",ForeignKey("models.id"), type_=Integer)
    model_data = relationship("ModelsModel")
    accessories = relationship("AccessoryModel",primaryjoin="MandatoryAccessoriesModel.model_id==AccessoryModel.model", foreign_keys="AccessoryModel.model", viewonly=True, overlaps="model_data")


    def __str__(self):
        return f"Required accessory in stock with model ID {self.model_id}"

class BaseViewModel(Base):
    __abstract__ = True
    def __init_subclass__(cls,*args,**kwargs):
       super().__init_subclass__(**kwargs)

       for name,value in cls.__dict__.items():
           if hasattr(value, "column"):
               value.column.insertable = False
               value.column.updatable = False

class AllPhonesViewModel(BaseViewModel):
    __tablename__ = 'all_phones'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    brand_name = mapped_column("brand_name", type_=Text)
    nationality = mapped_column("nationality",CheckConstraint("len(nationality) = 3"), type_=Text)
    battery_status = mapped_column("battery_status_%",type_=Integer)
    model = mapped_column("model", type_=Text, primary_key=True)
    modification = mapped_column("modification", type_=Text)
    capacity_gb = mapped_column("capacity_gb",type_=Integer)
    RAM = mapped_column("RAM",type_=Integer)
    price = mapped_column("price", type_=Float)
    processor = mapped_column("processor", type_=Text)
    phone_status = mapped_column("phone_status",CheckConstraint("phone_status in ('old','new')", "all_phones_view_status_constraint"), type_=Integer)


    def __str__(self):
        return f"Phone device {self.brand_name} {self.model} {self.modification} with {self.capacity_gb}GB memory, with {self.RAM}GB of RAM, maximum battery capacity {self.battery_status + '%' if self.battery_status else 'N/A'} usage status {self.phone_status}, price per item {self.price}"

class PhonesInStockViewModel(BaseViewModel):
    __tablename__ = 'phones_in_stock'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    brand_name = mapped_column("brand_name", type_=Text)
    nationality = mapped_column("nationality", CheckConstraint("len(nationality) = 3"), type_=Text)
    battery_status = mapped_column("battery_status_%", type_=Integer)
    model = mapped_column("model", type_=Text, primary_key=True)
    modification = mapped_column("modification", type_=Text)
    capacity_gb = mapped_column("capacity_gb", type_=Integer)
    RAM = mapped_column("RAM", type_=Integer)
    price = mapped_column("price", type_=Float)
    processor = mapped_column("processor", type_=Text)
    phone_status = mapped_column("phone_status",
                                 CheckConstraint("phone_status in ('old','new')", "all_phones_view_status_constraint"),
                                 type_=Integer)
    notes = mapped_column("notes", type_=Text)

    def __str__(self):
        return f"Phone device in stock {self.brand_name} {self.model} {self.modification} with {self.capacity_gb}GB memory, with {self.RAM}GB of RAM, maximum battery capacity {self.battery_status + '%' if self.battery_status else 'N/A'} usage status {self.phone_status}, price per item {self.price}. \n {self.notes}"

class PhonesInStockSCVViewModel(BaseViewModel):
    __tablename__ = 'phone_in_stock_scv'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    model = mapped_column("model", type_=Text, primary_key=True)
    phone_name = mapped_column("phone_name", type_=Text)
    nationality = mapped_column("nationality", CheckConstraint("len(nationality) = 3"), type_=Text)
    capacity_gb = mapped_column("capacity_gb", type_=Integer)
    RAM = mapped_column("RAM", type_=Integer)
    battery_status = mapped_column("battery_status", type_=Integer)
    processor = mapped_column("processor", type_=Text)
    price_eur = mapped_column("price_eur", type_=Text)
    price_bgn = mapped_column("price_bgn", type_=Text)
    phone_status = mapped_column("phone_status",CheckConstraint("phone_status in ('new','old')"), type_=Integer)
    notes = mapped_column("notes", type_=Text)


    def __str__(self):
        return f"Phone device {self.phone_name} in stock with memory {self.capacity_gb}, RAM memory {self.RAM}, baterry status {self.batytery_status + '%' if self.battery_status else "N/A"} usage status: {self.phone_status} price per item in EUR: €{self.price_eur}, BGN: {self.price_bgn}лв."

class CasesInStockViewModel(BaseViewModel):
    __tablename__ = 'cases_in_stock'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    case = mapped_column("case", type_=Text, primary_key=True)
    count = mapped_column("count", type_=Integer)


    def __str__(self):
        return f"{self.cases} with count {self.count}"

class CompatibleModelsViewModel(BaseViewModel):
    __tablename__ = 'compatible_models'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    model_id = mapped_column("model_id", type_=Integer, primary_key=True)
    brand_id = mapped_column("brand_id", type_=Integer)
    accessoir_id = mapped_column("accessoir_id", type_=Integer)
    device_type_id =mapped_column("device_type_id", type_=Integer)
    name = mapped_column("name", type_=Text)
    model = mapped_column("model", type_=Text)
    modification = mapped_column("modification", type_=Text)
    device_type = mapped_column("device_type", type_=Text)
    count = mapped_column("count", type_=Integer)
    price_per_item = mapped_column("price_per_item", type_=Float)


    def __str__(self):
        return f"Device {self.name} {self.model} {self.modification} of type {self.device_type} with count {self.count} and price per item {self.price_per_item}"

class MandatoryModelAccessoriesViewModel(BaseViewModel):
    __tablename__ = 'mandatory_model_accessories'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    device = mapped_column("device", type_=Text, primary_key=True)
    cases = mapped_column("cases", type_=Integer)
    wallet_cases = mapped_column("wallet_cases", type_=Integer)
    protectors = mapped_column("protector", type_=Text)



    def __str__(self):
        return f"Device model {self.model} cases count: {self.cases}; wallet cases count {self.wallet_cases}; protectors count {self.protectors} "

class ScreenProtectorsInStockViewModel(BaseViewModel):
    __tablename__ = 'screen_protectors_in_stock'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    protector = mapped_column("protector", type_=Text, primary_key=True)
    count = mapped_column("count", type_=Integer)


    def __str__(self):
        return f"For model {self.protector} with count {self.count}"

class WalletCasesInStockViewModel(BaseViewModel):
    __tablename__ = 'wallet_cases_in_stock'
    # __table_args__ = {
    #     'extend_existing': True,
    #     'autoload_with': engine,
    # }
    case = mapped_column("case", type_=Text, primary_key=True)
    count = mapped_column("count", type_=Integer)


    def __str__(self):
        return f"Walet case for model {self.case} with count {self.count}"
