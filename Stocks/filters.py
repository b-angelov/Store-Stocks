from decimal import Decimal


class BaseFilters:
    def __init__(self, app:object=object, filter_list:dict={}):
        self.filter_list = filter_list
        self.app = app


class JinjaFilters(BaseFilters):

    def __init__(self, app:object=object, filter_list={}):
        if not filter_list:
            filter_list = {
                "norm_price": self.normalize_price,
                "currency_sign": self.currency_sign,
            }
        super().__init__(app,filter_list)

    def reg_in_jinja_filter(self):
        for name,func in self.filter_list.items():
            self.app.jinja_env.filters[name] = func

    @staticmethod
    def normalize_price(value:float|Decimal|str)->str:
        if isinstance(value, str):
            value = value.replace(",",".")
            value = Decimal(value)
        if hasattr(value, "normalize"):
            value = value.normalize()
        return f"{round(value,2):.2f}"

    @staticmethod
    def currency_sign(value, code:str="EUR")->str:
        currencies = {
            "USD": "$",
            "EUR": "€",
            "BGN": "лв.",
            "GBP": "£"
        }
        return f"{value}{currencies.get(code.upper(), '')}"

