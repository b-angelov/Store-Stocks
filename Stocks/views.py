from flask import typing as ft, request, render_template
from flask.views import View

from models import Base
from resources import PhoneDeviceResource, BrandsResource, DeviceTypesResource, ModelsResource, AccessoriesResource, \
    MandatoryAccessoriesResource


class BaseView(View):

    def __init__(self, resource: object, template: str):
        super().__init__()
        self.resource = resource
        self.template = template

    def dispatch_request(self) -> ft.ResponseReturnValue:
        if request.method == "GET":
            return render_template(self.template,items=self.get())

    def get(self):
        return self.resource().apply_filters(request.args).build_result()

class ListPhonesView(BaseView):
    methods = ["GET","POST"]

    def __init__(self):
        super().__init__(PhoneDeviceResource, "phones.html")

    def dispatch_request(self) -> ft.ResponseReturnValue:
        return super().dispatch_request()


class ListBrandsView(BaseView):
    methods = ["GET","POST"]

    def __init__(self):
        super().__init__(BrandsResource, "brands.html")

    def dispatch_request(self):
        return super().dispatch_request()


class ListDeviceTypesView(BaseView):
    methods = ["GET","POST"]

    def __init__(self):
        super().__init__(DeviceTypesResource, "device_types.html")

    def dispatch_request(self):
        return super().dispatch_request()


class ListModelsView(BaseView):
    methods = ["GET","POST"]

    def __init__(self):
        super().__init__(ModelsResource, "models.html")

    def dispatch_request(self):
        return super().dispatch_request()

class ListAccessoriesView(BaseView):
    methods = ["GET","POST"]

    def __init__(self):
        super().__init__(AccessoriesResource, "accessories.html")

    def dispatch_request(self):
        return super().dispatch_request()

class ListMandatoryAccessoriesView(BaseView):
    methods = ["GET","POST"]

    def __init__(self):
        super().__init__(MandatoryAccessoriesResource, "mandatory_accessories.html")

    def dispatch_request(self):
        return super().dispatch_request()
