from . import api
from ..models import Classify
from ..utils import ok


@api.route('classify_product_list')
def classify_product_list():
    classify = Classify.query.filter(Classify.name != '积分商城').all()
    result = []
    for item in classify:
        item_obj = item.to_json()
        item_obj['children'] = [p.to_json() for p in item.product.all()]
        result.append(item_obj)
    return ok(data=result)
