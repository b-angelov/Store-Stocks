from flask_smorest import abort

from extensions import db


class BaseValidator:
    pass

class ModelValidators(BaseValidator):

    @staticmethod
    def floatify(func):
        def decorator(*args, **kwargs):
            value,*_ = args
            if not value:
                value = kwargs.get("value", 0)
            value = func(value)
            if isinstance(value, str):
                value = value.replace(",", ".")
            try:
                value = float(value)
            except:
                return 0
            return value
        return decorator

    @staticmethod
    def integerify(func):
        def decorator(*args, **kwargs):
            value,*_ = args
            if not value:
                value = kwargs.get("value", 0)
            value = func(value)
            try:
                value = int(value)
            except:
                return 0
            return value
        return decorator

    @staticmethod
    def sum_ram(func):
        def decorator(*args, **kwargs):
            value,*_ = args
            if not value:
                value = kwargs.get("value", 0)
            value = func(value)
            if isinstance(value, str):
                try:
                    value = int(value)
                except:
                    try:
                        value = sum(*(v for v in value.split('+')))
                    except:
                        value = 0
            return value
        return decorator

class ViewValidators(BaseValidator):

    @staticmethod
    def has_id(func):
        def decorator(self, *args, **kwargs):
            id = args[0] if args else False
            if not id:
                id = kwargs.get("id", False)
            item = self.resource(api=True).with_id(id)
            item = db.session.execute(item.query).scalar_one_or_none()
            if item is None:
                abort(404, "Record with the specified ID was not found.")
            return func(self, item=item, *args, **kwargs)
        return decorator


