import json
import time
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse

from purchase_manage.models import Purchase
from product_manage.models import Product, PurchaseProductRel
from project_manage.models import Project
from utils.utils import get_kwargs, get_bulk


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
    page_number = request.GET.get('page') if request.GET.get('page') is not None else 1
    query_dic = kwargs.get('kwargs').get('query') if kwargs else {}
    #  查询条件
    q = Q()
    if query_dic:
        for query in query_dic:
            q.add(Q(**{query: query_dic[query]}), Q.OR)
    # 查询结果集
    start = time.time()
    purchases = Purchase.objects.all().filter(flag=True).filter(q).values(
        *['id', 'form_number', 'contract_number', 'project__project_name', 'purchase_date', 'demand_person',
          'handle_man'])
    for purchase in purchases:
        rel = PurchaseProductRel.objects.filter(purchase_id=purchase.get('id')).values_list(
            *['quantity', 'product__product_name', 'product__product_model', 'product__unit_price'])
        purchase['rel'] = rel
    # 分页
    end = time.time()
    print('耗时：', end - start, 's')
    paginator = Paginator(purchases, 10)
    page_data = paginator.page(number=page_number)
    return render(request, 'purchases/purchases.html',
                  {'purchases': page_data, 'count': paginator.count})


# 废除
# def reform_data(DATA):
#     """
#     datatype  [{purchase:purchase_obj, rel:[{quantity:val,name:val, model:val,price:val},
#                                             {quantity:val,name:val, model:val,price:val},
#                                             ]
#               }]
#     @param DATA:
#     @return:
#     """
#     return_list = []
#     for purchase in DATA:
#         relation = purchase.purchaseproductrel_set.all()
#         result = {'purchase': purchase}
#         rel_list = []
#         for r in relation:
#             temp = {'product_name': r.product.product_name, 'product_model': r.product.product_model,
#                     'unit_price': r.product.unit_price, 'quantity': r.quantity}
#             rel_list.append(temp)
#         result.update({'rel': rel_list})
#         return_list.append(result)
#     return return_list


# 废除
# def reform_data_2(DATA):
#     return_list = []
#     for purchase in DATA:
#         # temp = {}
#         result = {'purchase': purchase}
#         relation = purchase.purchaseproductrel_set.all()
#         result['product_name'] = [r.product.product_name for r in relation]
#         result['unit_price'] = [r.product.unit_price for r in relation]
#         result['product_model'] = [r.product.product_model for r in relation]
#         result['quantity'] = [r.quantity for r in relation]
#         # result.update({'rel': temp})
#         return_list.append(result)
#     return return_list


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
        kwargs = get_kwargs(klass=Purchase, package_data=package_data)
        # 判断是更新还是新增
        if package_data.get('id') is not None:
            # 先更新purchase表
            this_purchase_id = package_data.get('id')
            Purchase.objects.filter(id=this_purchase_id).update(**kwargs)
            package = transform_data({'purchase_id': this_purchase_id,
                                      'product_id': package_data.get('product'),
                                      'quantity': package_data.get('quantity')
                                      })
            # 对于采购产品关系表更新，包括新增或减少
            increase_or_decrease(this_id=this_purchase_id, klass=Purchase, rel_klass=PurchaseProductRel,
                                 package=package, fields=['product', 'quantity'])
        else:
            # 新增purchase
            # 获取数据包填充过的purchase
            Purchase.objects.create(**kwargs)
            this_purchase_id = Purchase.objects.last().id
            package = transform_data({'purchase_id': this_purchase_id,
                                      'product_id': package_data.get('product'),
                                      'quantity': package_data.get('quantity')
                                      })
            # 新增采购产品关系
            pp_rel_bulk = get_bulk(rel_klass=PurchaseProductRel, args=package)
            print(pp_rel_bulk)
            PurchaseProductRel.objects.bulk_create(pp_rel_bulk)
        print('POST请求完毕')
        print('结束时间-->', time.time())
        return JsonResponse({'status': 'success'})


# 增加产品或减少产品
def increase_or_decrease(this_id, klass, rel_klass, package, fields):
    """
    @param fields:
    @param rel_klass:
    @param klass:
    @param package:
    @param this_id:
    @return:
    """
    # 先取该purchase的之前关系表
    att = f'{rel_klass.__name__.lower()}_set'
    rel_set = klass.objects.filter(id=this_id).first().__getattribute__(att).all()
    # 先比较product列表长度和queryset的长度，判断增加产品还是减少产品
    difference = len(package) - len(rel_set)
    # 增加产品，那么对product列表切片，将切下来的insert
    print('增加', difference)
    if difference > 0:
        # 目前提交数据长于之前，新增关系
        need_to_update = get_bulk(rel_klass=rel_klass, args=package[:len(rel_set)], original=rel_set)
        rel_klass.objects.bulk_update(need_to_update, fields)
        need_to_insert = get_bulk(rel_klass=rel_klass, args=package[-difference:])
        rel_klass.objects.bulk_create(need_to_insert)
    elif difference < 0:
        # 减少产品，那么对queryset切片，将切下来的remove
        # 目前提交数据小于之前，减少关系
        need_to_update = get_bulk(rel_klass=rel_klass, args=package, original=rel_set[:len(package)])
        need_to_remove = rel_set[:-difference]
        rel_klass.objects.bulk_update(need_to_update, fields)
        for rel in need_to_remove:
            rel.delete()
    else:
        # 未增减只更新
        rel_klass.objects.bulk_update(get_bulk(rel_klass=rel_klass, args=package, original=rel_set), fields)


def transform_data(kwargs):
    """
    @param kwargs: 任意字典，单元素（bool，int，str），多元素（list， tuple， set），多元素的长度均相等
           将单元素数据挑出或者长度为1的组合元素挑出， 并列写入字典
           将多元素并且长度大于1的组合元素挑出， 并列写入字典
           多元素形成的字典列长度为单个多元素的长度*多元素种类，最后整理完成list切片长度为[:单个多元素的长度]
    @return: 返回整理的字典列表
    """
    # 多元素种类
    print('transform_data: 整理m2m中m')
    kinds = [key for key, value in kwargs.items() if type(value) not in (int, bool, str) and len(value) > 1]
    # 单元素的转入字典
    single_kv = {key: value for key, value in kwargs.items() if type(value) in (int, str, bool)}
    # 有一种情况就是多元素的长度为1
    if len(kinds) == 0:
        list_val = {key: value[0] for key, value in kwargs.items() if
                    type(value) in (list, tuple, dict)}
        list_val.update(single_kv)
        return [list_val]
    else:
        # 多元素所有项生成字典
        list_val = [{key: val} for key, value in kwargs.items() if
                    type(value) not in (int, str, bool) and len(value) > 1
                    for val in value]
        pre_length = int(len(list_val) / len(kinds))
        for i in range(pre_length):
            for j in range(len(kinds)):
                if j > 0:
                    list_val[i].update(list_val[i + pre_length * j])
            list_val[i].update(single_kv)
        return list_val[:pre_length]
