import json
import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import ModelForm, Form, fields
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse

from purchase_manage.models import Purchase
from product_manage.models import Product, PurchaseProductRel
from project_manage.models import Project
from utils.utils import get_all, add_or_update, get_pageData, get_kwargs, get_bulk


# 搜索
def get_query_purchase(request):
    print(request.GET)
    query_data = request.GET.get('query') if request.GET.get('query') is not None else None
    kwargs = {'form_number__contains': query_data,
              'contract_number__contains': query_data} if query_data is not None else {}
    return get_all_purchases(request, kwargs={'query': kwargs})


# 查是否已使用
def check_occupy(request, query):
    query_val = request.GET.get('val')
    kwargs = {query: query_val}
    purchase = Purchase.objects.filter(**kwargs)
    data = {'status': 'available', 'component': query} if purchase.count() == 0 else {'status': 'unavailable',
                                                                                      'component': query}
    return JsonResponse(data)


# 删除
def delete_one(request, pk):
    Purchase.objects.filter(id=pk).update(flag=False)
    return HttpResponseRedirect(reverse('purchase_related:all_purchase_details'))


# 根据主键获取该采购
def get_one(request, pk=1):
    purchase = Purchase.objects.filter(id=pk).first()
    return render(request, 'purchases/add.html',
                  {'purchase': purchase, 'products': get_products_list(), 'projects': get_projects_list(),
                   'title': '修改订单'})


# 产品列表
def get_products_list():
    return Product.objects.all().order_by('product_name')


# 项目列表
def get_projects_list():
    return Project.objects.all().order_by('project_code')


# 获取所有采购
def get_all_purchases(request, **kwargs):
    """
    @param request:
    @return:
    """
    # 查询条件
    query_dic = kwargs.get('kwargs').get('query') if kwargs else {}
    q = Q()
    if query_dic:
        for query in query_dic:
            q.add(Q(**{query: query_dic[query]}), Q.OR)
    print(time.time())
    # 查询结果集
    purchases = Purchase.objects.all().filter(flag=True).filter(q)
    page_number = request.GET.get('page') if request.GET.get('page') is not None else 1
    # 分页
    paginator = Paginator(purchases, 10)
    page_data = get_pageData(paginator=paginator, pageNumber=page_number)
    # 取多对多关系
    rel_set = []
    for index in range(len(purchases)):
        rel_set.insert(index, purchases[index].purchaseproductrel_set.all())
    print(time.time())
    return render(request, 'purchases/purchases.html',
                  {'purchases': page_data, 'rel_set': rel_set, 'count': paginator.count})


# 添加或更新
def add_or_update(request):
    """第一次get请求是返回页面，此时等待post添加
       post请求中如果没有js获取的采购id，那么就是新增，如果有采购id，即为更新
    @param request:
    @return:
    """
    print('开始时间-->', time.time())
    print('请求方式-->', request.method)
    if request.method == 'GET':
        return render(request, 'purchases/add.html',
                      {'title': '新增采购', 'products': get_products_list(), 'projects': get_projects_list()})
    else:
        # 获取数据包
        package_data = json.loads(request.POST.get('package_data'))
        print(package_data)
        product = package_data.get('product')
        quantity = package_data.get('quantity')
        kwargs = get_kwargs(klass=Purchase, package_data=package_data)
        # 判断是更新还是新增
        if package_data.get('id') is not None:
            # 先更新purchase表
            this_purchase_id = package_data.get('id')
            Purchase.objects.filter(id=this_purchase_id).update(**kwargs)
            # 对于采购产品关系表更新，包括新增或减少
            increase_or_decrease(this_purchase_id, product, quantity)
        else:
            # 新增purchase
            # 获取数据包填充过的purchase
            Purchase.objects.create(**kwargs)
            this_purchase_id = Purchase.objects.last().id
            # 新增采购产品关系
            pp_rel_bulk = get_bulk(this_purchase_id, product, quantity)
            PurchaseProductRel.objects.bulk_create(pp_rel_bulk)

        print('POST请求完毕')
        print('结束时间-->', time.time())

        return JsonResponse({'status': 'success'})


# 增加产品或减少产品
def increase_or_decrease(this_purchase_id, product, quantity):
    """
    @param this_purchase_id:
    @param product:
    @param quantity:
    @return:
    """
    # 先取该purchase的之前关系表
    rel_set = Purchase.objects.filter(id=this_purchase_id).first().purchaseproductrel_set.all()
    # 先比较product列表长度和queryset的长度，判断增加产品还是减少产品
    difference = len(product) - len(rel_set)
    # 增加产品，那么对product列表切片，将切下来的insert
    if difference > 0:
        # 目前提交数据长于之前，新增关系
        need_to_update = get_bulk(this_purchase_id, product[:len(rel_set)], quantity[:len(rel_set)], rel_set)
        need_to_insert = get_bulk(this_purchase_id, product[-difference:], quantity[-difference:])
        PurchaseProductRel.objects.bulk_update(need_to_update, ['product_id', 'quantity'])
        PurchaseProductRel.objects.bulk_create(need_to_insert)
    elif difference < 0:
        # 减少产品，那么对queryset切片，将切下来的remove
        # 目前提交数据小于之前，减少关系
        need_to_update = get_bulk(this_purchase_id, product, quantity, rel_set)
        need_to_remove = rel_set[:-difference]
        PurchaseProductRel.objects.bulk_update(need_to_update, ['product_id', 'quantity'])
        for rel in need_to_remove:
            rel.delete()
    else:
        # 未增减只更新
        PurchaseProductRel.objects.bulk_update(get_bulk(this_purchase_id, product, quantity, rel_set),
                                               ['product_id', 'quantity'])
