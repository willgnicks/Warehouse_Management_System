from django.forms import ModelForm
from django.shortcuts import render

from product_manage.models import Product
from utils.utils import get_all, add_or_update, delete_one, get_pageData, get_one
from manufacturer_manage.models import Manufacturer
import json
from django.http import JsonResponse


# Create your views here.
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['flag', 'purchase']
        error_messages = {
            'product_name': {'required': '请输入产品名称'},
            'product_model': {'required': '请输入产品型号',
                              'unique': '该型号已存在'},
            'product_type': {'required': '请填输入产品类型'},
            'unit_price': {'required': '请输入产品单价',
                           'invalid': '请输入正确的价格格式'},
            'manufacturer': {'invalid_choice': '请选择对应的供应商'},
        }


def get_one_product(request, pk):
    return get_one(request, Product, kwargs={'pk': pk, 'title': '修改产品详情', 'quote_class': [Manufacturer]})


def ajax_all_products(request):
    all_products = Product.objects.all().order_by('product_name')
    js = {'products': list(all_products.values())}
    return JsonResponse(js)


def get_all_products(request):
    return get_all(request=request, klass=Product, kwargs={'rel': 'manufacturer'})


def get_query_products(request):
    query_data = request.GET.get('query') if request.GET.get('query') is not None else None
    kwargs = {'product_name__icontains': query_data,
              'product_model__icontains': query_data} if query_data is not None else {}
    return get_all(request=request, klass=Product, kwargs={'rel': 'manufacturer', 'query': kwargs})


def add_product(request):
    return add_or_update(request=request, klass=Product, form_class=ProductForm,
                         kwargs={'quote_class': [Manufacturer],
                                 'title': '新增产品',
                                 'reverse_url': 'product_related:all_product_details'})


def delete_product(request, pk):
    return delete_one(pk=pk, klass=Product, kwargs={'reverse_url': 'product_related:all_product_details'})
