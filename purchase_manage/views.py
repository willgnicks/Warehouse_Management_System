import json
import time

from django.core.paginator import Paginator
from django.forms import ModelForm, Form, fields
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse

from purchase_manage.models import Purchase
from product_manage.models import Product, PurchaseProductRel
from project_manage.models import Project
from utils.utils import get_all, put_one, get_pageData


class PurchaseForm(Form):
    form_number = fields.CharField(required=True, error_messages={
        'required': '请填入采购单号',
    })
    contract_number = fields.CharField(required=True, error_messages={
        'required': '请填入合同编号'
    })
    demand_person = fields.CharField(required=True, error_messages={
        'required': '请填写需求人'
    })
    handle_man = fields.CharField(required=True, error_messages={
        'required': '请填写经手人'
    })
    quantity = fields.IntegerField(required=True, error_messages={
        'required': '请填入数量',
        'invalid': '请填入正确数量'
    })
    product = fields.IntegerField(required=True, error_messages={
        'invalid': '请选择需采购的产品',
    })


def check_occupy(request, keyword='form_number'):
    pass


def get_and_update(request, pk=1):
    if request.method == 'GET':
        purchase = Purchase.objects.filter(id=pk).first()
        return render(request, 'purchases/add.html',
                      {'purchase': purchase, 'products': get_products_list(), 'projects': get_projects_list()})
    else:
        pass


def get_products_list():
    return Product.objects.all().order_by('product_name')


def get_projects_list():
    return Project.objects.all().order_by('project_code')


def get_all_purchases(request):
    # query = request.GET.get('query') if request.GET.get("query") is not None else None
    query = 'c'
    kwargs = {}
    if query is not None:
        kwargs['contract_number__contains'] = query
        # kwargs['project__project_name__contains'] = query
        # kwargs['contract_number__contains'] = query
    print(time.time())
    purchases = Purchase.objects.all().filter(flag=True)
    print(purchases.filter(**kwargs))
    page_number = request.GET.get('page') if request.GET.get('page') is not None else 1
    paginator = Paginator(purchases, 10)
    page_data = get_pageData(paginator=paginator, pageNumber=page_number)
    rel_set = []
    for index in range(len(purchases)):
        rel_set.insert(index, purchases[index].purchaseproductrel_set.all())
    for rel in rel_set[0]:
        print(rel.quantity)
    print(time.time())
    return render(request, 'purchases/purchases.html',
                  {'purchases': page_data, 'rel_set': rel_set, 'count': paginator.count})
    # return get_all(request=request, klass=Purchase, kwargs={'purchaseproductrel_set': 'purchaseproductrel_set'})


def add_purchase(request):
    print('请求方式-->', request.method)
    if request.method == 'GET':
        return render(request, 'purchases/add.html', {'products': get_products_list(), 'projects': get_projects_list()})
    else:
        package_data = json.loads(request.POST.get('package_data'))
        print(package_data)
        purchase_fields = Purchase._meta.fields
        purchase = Purchase()
        for i in range(len(purchase_fields)):
            att_name = purchase_fields[i].attname
            att_val = package_data.get(att_name)
            if att_val is not None:
                purchase.__setattr__(att_name, att_val)
        purchase.save()
        this_purchase_id = Purchase.objects.last().id
        pp_rel_bulk = []
        product = package_data.get('product')
        quantity = package_data.get('quantity')
        for index in range(len(product)):
            pp_rel = PurchaseProductRel(purchase_id=this_purchase_id, product_id=product[index],
                                        quantity=quantity[index])
            pp_rel_bulk.append(pp_rel)
        PurchaseProductRel.objects.bulk_create(pp_rel_bulk)
        print('POST请求完毕')
        return JsonResponse({'f': 'for'})

# def add_purchase(request):
#     # modelform表单实力化
#     print(time.time())
#     modelform_instance = PurchaseForm(request.POST)
#     # model = PurProRel(request.POST)
#     # print(model.errors)
#     # 初始化返回字典
#     # 获取引用类list, 无值传空
#     print(modelform_instance.data.getlist('product'))
#     if request.method == 'GET':
#     return render(request, 'purchases/add.html', {'products': get_products_list(), 'projects': get_projects_list()})
# else:
#     if modelform_instance.is_valid():
#         print(modelform_instance.cleaned_data)
#         # print(model.data)
#         this_form = modelform_instance.save(commit=False)
#         print(Purchase.objects.last().id)
#         print(time.time())
#         return HttpResponseRedirect(
#             reverse(
#                 'purchase_related:all_purchase_details'
#             )
#         )
#     else:
#         print({'errors': modelform_instance.errors})
#         return render(request, 'purchases/add.html',
#                       {'products': Product.objects.all(), 'purchases': modelform_instance,
#                        'projects': get_projects_list()})
# return put_one(request=request, form_class=PurchaseForm,
#                kwargs={'quote_class': [Product, Project], 'reverse_url': 'purchase_related:all_purchase_details'})
# class Meta:
#     model = Purchase
#     fields = '__all__'
#     exclude = ['project', 'flag', 'product']
#     error_messages = {
#         'form_number': {'required': '请填入采购单号'},
#         'contract_number': {'required': '请填入合同编号'},
#         'demand_person': {'required': '请填入需求人'},
#         'handle_man': {'required': '请填入经手人'},
#     }

#
# class PurProRel(ModelForm):
#     class Meta:
#         model = PurchaseProductRel
#         fields = '__all__'
#         exclude = ['purchase_date', 'purchase']
#         error_messages = {
#             'quantity': {'required': '不空'}
#        d }
