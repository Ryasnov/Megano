from django.http import QueryDict
from django.db.models import QuerySet, Case, When

from products.models import Category, Product


def _fix_data(data: dict) -> dict:
    """Функция для products_filter, удаляющая ненужные элементы из словаря data"""

    for key in data.copy():
        if data[key] is None or data[key] == "NaN":
            data.pop(key)
    return data


def products_filter(querydict: QueryDict) -> dict:
    """Функция фильтрация товаров"""

    delivery = None
    try:
        if eval(querydict.get("filter[freeDelivery").title()):
            delivery = True
    except Exception:
        pass

    data = {
        "title__icontains": querydict.get("filter[name]"),
        "price__lte": querydict.get("filter[maxPrice]"),
        "price__gte": querydict.get("filter[minPrice]"),
        "freeDelivery": delivery,
        "category_id": querydict.get("category"),
        "tags__in": querydict.get("tags[]"),
    }

    data = _fix_data(data=data)
    return data


def products_sort(querydict: QueryDict, query: QuerySet) -> QuerySet:
    """Функция сортировки товаров"""

    reverse = True
    sort = querydict.get("sort")

    if querydict.get("sortType") == "dec":
        sort = "-" + sort

    if "rating" in sort:
        if "-" in sort:
            reverse = False

        rate_list = sorted(
            [(product.id, product.rating) for product in query],
            key=lambda i: i[1],
            reverse=reverse,
        )
        pk_list = [idx for idx, rate in rate_list]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = Product.objects.filter(pk__in=pk_list).order_by(preserved)
    else:
        queryset = query.order_by(sort)

    return queryset
