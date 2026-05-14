from flask import Blueprint

from api_views import blp, PhonesAPIView, BrandsAPIView, DeviceTypesAPIView, ModelsAPIView, AccessoriesAPIView, \
    MandatoryAccessoriesAPIView, PhonesItemAPIView, BrandsItemAPIView, DeviceTypesItemAPIView, ModelsItemAPIView, \
    MandatoryAccessoriesItemAPIView, AccessoriesItemAPIView, PhonesDistinctBrandsAPIView, PhonesDistinctModelsAPIView
from resources import PhoneDeviceResource, BrandsResource
from views import ListPhonesView, ListBrandsView, ListDeviceTypesView, ListModelsView, ListAccessoriesView, \
    ListMandatoryAccessoriesView

routes_bp = Blueprint('routes_bp', __name__)
base = lambda x,base,*args: f"{base}/{x}/" + ('/'.join(args) + '/' if args else '')
api = lambda x: base(x,'/api')

@routes_bp.route('/')
def hello_world():  # put application's code here
    return PhoneDeviceResource.get_items()

routes_bp.route('/phones/')(ListPhonesView.as_view("phones_list_view"))
routes_bp.route('/brands/')(ListBrandsView.as_view("brands_list_view"))
routes_bp.route('/device_types/')(ListDeviceTypesView.as_view("device_types_list_view"))
routes_bp.route('/models/')(ListModelsView.as_view("models_list_view"))
routes_bp.route('/accessories/')(ListAccessoriesView.as_view("accessories_list_view"))
routes_bp.route('/mandatory_accessories/')(ListMandatoryAccessoriesView.as_view("mandatory_accessories_list_view"))

blp.add_url_rule(api('/phones/'),view_func=PhonesAPIView.as_view("phones_list_api_view"))
blp.add_url_rule(api('/phones/brands/'),view_func=PhonesDistinctBrandsAPIView.as_view("phones_distinct_brands_list_api_view"))
blp.add_url_rule(api('/phones/models/'),view_func=PhonesDistinctModelsAPIView.as_view("phones_distinct_models_list_api_view"))
blp.add_url_rule(api('/phones/<int:id>'),view_func=PhonesItemAPIView.as_view("phones_item_api_view"))
blp.add_url_rule(api('/brands/'),view_func=BrandsAPIView.as_view("brands_list_api_view"))
blp.add_url_rule(api('/brands/<int:id>'),view_func=BrandsItemAPIView.as_view("brands_item_api_view"))
blp.add_url_rule(api('/device_types/'),view_func=DeviceTypesAPIView.as_view("device_types_list_api_view"))
blp.add_url_rule(api('/device_types/<int:id>'),view_func=DeviceTypesItemAPIView.as_view("device_types_item_api_view"))
blp.add_url_rule(api('/models/'),view_func=ModelsAPIView.as_view("models_list_api_view"))
blp.add_url_rule(api('/models/<int:id>'),view_func=ModelsItemAPIView.as_view("models_item_api_view"))
blp.add_url_rule(api('/mandatory_accessories/'),view_func=MandatoryAccessoriesAPIView.as_view("mandatory_accessories_list_api_view"))
blp.add_url_rule(api('/mandatory_accessories/<int:id>'),view_func=MandatoryAccessoriesItemAPIView.as_view("mandatory_accessories_item_api_view"))
blp.add_url_rule(api('/accessories/'),view_func=AccessoriesAPIView.as_view("accessories_list_api_view"))
blp.add_url_rule(api('/accessories/<int:id>'),view_func=AccessoriesItemAPIView.as_view("accessories_item_api_view"))

