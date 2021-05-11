from django.forms import ModelForm
from product_manage.models import Product
from utils.utils import get_all, put_one, delete_one
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
            'product_model': {'required': '请输入产品型号'},
            'product_type': {'required': '请填输入产品类型'},
            'unit_price': {'required': '请输入产品单价',
                           'invalid': '请输入正确的价格格式'},
            'manufacturer': {'invalid_choice': '请选择对应的供应商'},
        }


def ajax_all_products(request):
    all_products = Product.objects.all().order_by('product_name')
    js = {'products': list(all_products.values())}
    return JsonResponse(js)


def get_all_products(request):
    return get_all(request=request, klass=Product)


def add_product(request):
    return put_one(request=request, form_class=ProductForm,
                   kwargs={'quote_class': [Manufacturer], 'reverse_url': 'product_related:all_product_details'})


def delete_product(request, pk=1):
    return delete_one(pk=pk, klass=Product, kwargs={'reverse_url': 'product_related:all_product_details'})


"""


    # if request.method == 'GET':
    #     return render(request, 'products/add.html', {'manufacturers': get_manufacturers_list()})
    # else:
    #     if ProductForm(request.POST).is_valid():
    #         ProductForm(request.POST).save()
    #         return HttpResponseRedirect(reverse('product_related:all_product_details'))
    #     else:
    #         return render(request, 'products/add.html',
    #                       {'products': ProductForm(request.POST), 'manufacturers': get_manufacturers_list()})
"""
