from marshmallow import Schema, fields


class DeviceTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    device_type = fields.String()
    model = fields.Int()
    count = fields.Int()
    price_per_item = fields.Float()

    class Meta:
        pass

class PhoneSchema(Schema):
    id = fields.Int(dump_only=True)
    model = fields.Int(required=True)
    capacity_gb = fields.Int()
    battery_status = fields.Int()
    RAM = fields.Int()
    price = fields.Float()
    processor = fields.String()
    phone_status = fields.Str()
    notes = fields.Str()
    sold = fields.Bool(load_default=False)

    class Meta:
        pass


class ModelsSchema(Schema):
    id = fields.Int(dump_only=True)
    brand = fields.Int()
    model = fields.String()
    modification = fields.String()
    device_type = fields.Int()
    compatible_accessories = fields.Nested("AccessorySchema", many=True, exclude=("compatible_models",))

    class Meta:
        pass

class AccessorySchema(Schema):
    id = fields.Int(dump_only=True)
    model = fields.Int()
    device_type = fields.Int()
    count = fields.Int()
    price_per_item = fields.Float()
    compatible_models = fields.Nested("ModelsSchema", dump_only=True, many=True, exclude=("compatible_accessories",))

    class Meta:
        pass



class AceessoryCompatibleModelsSchema(Schema):
    id = fields.Int(dump_only=True)
    accessoir = fields.Int()
    model = fields.Int()

    class Meta:
        pass



class BrandsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    nationality = fields.Str()

    class Meta:
        pass



class MandatoryAccessorySchema(Schema):
    id = fields.Int(dump_only=True)
    model_id = fields.Int()

    class Meta:
        pass

class ModelsJoinedSchema(ModelsSchema):
    brand_data = fields.Nested(BrandsSchema, dump_only=True)
    device_type_data = fields.Nested(DeviceTypeSchema, dump_only=True)

class AccessoriesJoinedSchema(AccessorySchema):
    model_data = fields.Nested(ModelsJoinedSchema, dump_only=True)

class PhoneJoinedSchema(PhoneSchema):
    model_data = fields.Nested(ModelsJoinedSchema, dump_only=True)

class AccessoryJoinedSchema(AccessorySchema):
    model_data = fields.Nested(ModelsJoinedSchema, dump_only=True)
    device_type_data = fields.Nested(DeviceTypeSchema, dump_only=True)

class AccessoryCompatibleModelsJoinedSchema(AccessorySchema):
    model = fields.Nested(ModelsJoinedSchema, dump_only=True)
    accessoir = fields.Nested(AccessoryJoinedSchema, dump_only=True)

class MandatoryAccessoryJoinedSchema(MandatoryAccessorySchema):
    model = fields.Nested(ModelsJoinedSchema, dump_only=True)
    accessories = fields.Nested(AccessoryJoinedSchema, dump_only=True,many=True,allow_none=True)
    model_data = fields.Nested(ModelsJoinedSchema, dump_only=True)

class AllPhonesViewSchema(Schema):
    brand_name = fields.Str()
    nationality = fields.Str()
    model = fields.Str()
    modification = fields.Str()
    capacity_gb = fields.Int()
    battery_status = fields.Int()
    RAM = fields.Int()
    price = fields.Float()
    processor = fields.Str()
    phone_status = fields.Str()

    class Meta:
        pass

class CasesInStockViewSchema(Schema):
    case = fields.Str(dump_only=True)
    count = fields.Int(dump_only=True)

    class Meta:
        pass

class CompatibleModelsViewSchema(Schema):
    accessoir_id = fields.Int(dump_only=True)
    model_id = fields.Int(dump_only=True)
    brand_id = fields.Int(dump_only=True)
    device_type_id = fields.Int(dump_only=True)
    name = fields.Str()
    model = fields.Str()
    modification  = fields.Str()
    device_type = fields.Int()
    count = fields.Int(dump_only=True)
    price_per_item = fields.Float()

    class Meta:
        pass

class MandatoryModelAccessoriesViewSchema(Schema):
    device =  fields.Str(dump_only=True)
    cases = fields.Int(dump_only=True)
    wallet_cases = fields.Int(dump_only=True)
    protectors_cases = fields.Int(dump_only=True)

    class Meta:
        pass

class PhonesInStockSCVViewSchema(Schema):
    phone_name = fields.Str(dump_only=True)
    nationality = fields.Str()
    capacity_gb = fields.Str()
    RAM = fields.Str()
    battery_status = fields.Str()
    processor = fields.Str(dump_only=True)
    price_euro = fields.Str()
    price_bgn = fields.Str()
    phone_status = fields.Str()
    notes = fields.Str()

    class Meta:
        pass

class PhonesInStockViewSchema(Schema):
    brand_name = fields.Str()
    nationality = fields.Str()
    model = fields.Str()
    modification = fields.Str()
    capacity_gb = fields.Int()
    battery_status = fields.Int()
    RAM = fields.Int()
    price = fields.Float()
    processor = fields.Str()
    phone_status = fields.Str()
    notes = fields.Str()

    class Meta:
        pass

class ScreenProtectorsInStockViewSchema(Schema):
    protector = fields.Str()
    count = fields.Int(dump_only=True)

    class Meta:
        pass

class WalletCasesInStockViewSchema(Schema):
    case = fields.Str()
    count = fields.Int(dump_only=True)

    class Meta:
        pass

class ErrorSchema(Schema):
    code = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)

    class Meta:
        pass