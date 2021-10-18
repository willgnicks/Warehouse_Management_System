import json
import time
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from equipment_manage.models import Equipment
from inbound_manage.models import Inbound
from django.forms import ModelForm
from product_manage.models import PurchaseProductRel
from project_manage.models import Project
from purchase_manage.models import Purchase
from utils.utils import get_all, add_or_update, get_kwargs, get_bulk, transform_data


class InboundForm(ModelForm):
    class Meta:
        model = Inbound
        fields = '__all__'
        exclude = ['comments', 'flag']
        error_messages = {
            'material_code': {'required': '请填写物料编号'},
            'inbound_rel': {'required': '请填写入库数量'},
            'in_house_date': {'required': '请填写入库日期',
                              'invalid': '请填写正确的日期格式'},
        }


def get_one(request, pk=1):
    start = time.time()
    value_fields = ['id',
                    'material_code',
                    'comments',
                    'pp_rel_id',
                    'pp_rel__purchase_id',
                    'pp_rel__purchase__form_number',
                    'pp_rel__purchase__project__project_name',
                    'pp_rel__product__product_name',
                    'pp_rel__product__product_model',
                    'pp_rel__quantity']
    inbound = Inbound.objects.filter(id=pk, flag=True).values(*value_fields).first()
    equip = Equipment.objects.filter(inbound_id=pk).values_list(*['id', 'SN'])
    inbound['equip'] = equip
    print('后台耗时', time.time() - start, 's')
    return render(request, 'inbounds/add.html',
                  {'inbound': inbound})


# GET获取所有inbounds
def get_all_inbounds(request, **kwargs):
    values_fields = ['id',
                     'material_code',
                     'in_house_date',
                     'comments',
                     'pp_rel__quantity',
                     'pp_rel__product__product_name',
                     'pp_rel__product__product_model',
                     'pp_rel__purchase__form_number'
                     ]
    query_dic = kwargs.get('kwargs').get('query') if kwargs else {}
    return get_all(request, klass=Inbound, kwargs={
        'value_field': values_fields, 'query': query_dic})


# 获取指定采购ID的未入库的pp_rel
def get_rel(request):
    if request.method == 'GET':
        this_id = request.GET.get('purchase_id')
        fields = ['id', 'quantity', 'product__product_name', 'product__product_model']
        queryset = PurchaseProductRel.objects.filter(purchase_id=this_id, flag=False).values(*fields)
        return JsonResponse({'data': list(queryset)})


def add_or_update(request):
    """第一次get请求是返回页面，此时等待post添加
       post请求中如果没有js获取的采购id，那么就是新增，如果有采购id，即为更新
    @param request:
    @return:
    """
    start = time.time()
    print('请求方式-->', request.method)
    if request.method == 'GET':
        print('后台耗时：', time.time() - start, 's')
        return render(request, 'inbounds/add.html',
                      {'purchases': Purchase.objects.filter(inbound_flag=False, flag=1)})
    else:
        # 获取数据包
        package_data = json.loads(request.POST.get('package_data'))
        print(package_data)
        # 先修改中间表中需要入库项的状态为已入库
        PurchaseProductRel.objects.filter(id=package_data.get('pp_rel_id')).update(flag=True)
        # 再查询采购表中该采购的中间表中是否都已经入库了
        # 如果都入库了，那么该采购单入库状态就为已入库，不会再在入库时显示出来
        purchase = package_data.get('purchase')
        if len(PurchaseProductRel.objects.filter(purchase_id=purchase, flag=False)) == 0:
            Purchase.objects.filter(id=purchase).update(inbound_flag=True)
            Project.objects.filter(id=Purchase.objects.filter(id=purchase).first().project_id).update(project_status=2)
        # 先增加inbound
        this_inbound = package_data.get('id')
        # 判断是更新还是新增
        if this_inbound is not None:
            # 先更新inbound
            Inbound.objects.filter(id=this_inbound).update(**get_kwargs(Inbound, package_data))
            # 整理数据
            package = transform_data({
                'inbound_id': this_inbound,
                'SN': package_data.get('equipment_ID'),
            })
            # 查询原数据集
            original = Equipment.objects.filter(inbound_id=this_inbound)
            # 获取equipment的bulk
            equipment_bulk = get_bulk(rel_klass=Equipment, args=package, original=original)
            # 设备bulk_update
            Equipment.objects.bulk_update(equipment_bulk, ['SN'])
        else:
            # 新增inbound
            Inbound.objects.create(**get_kwargs(klass=Inbound, package_data=package_data))
            this_id = Inbound.objects.last().id
            package = transform_data({'inbound_id': this_id,
                                      'SN': package_data.get('equipment_ID'),
                                      })
            # 新增采购产品关系
            equipment_bulk = get_bulk(rel_klass=Equipment, args=package)
            Equipment.objects.bulk_create(equipment_bulk)
        print('POST请求完毕')
        print('后台耗时-->', time.time() - start, 's')
        return JsonResponse({'status': 'success'})


# 删除
def delete_one(request, pk):
    Inbound.objects.filter(id=pk).update(flag=False)
    Equipment.objects.filter(inbound_id=pk).update(flag=False)
    return HttpResponseRedirect(reverse('inbound_related:all_inbounds_details'))


# 搜索
def get_query_inbound(request):
    query_data = request.GET.get('query') if request.GET.get('query') is not None else None
    kwargs = {'material_code__icontains': query_data,
              'pp_rel__product__product_name__icontains': query_data} if query_data is not None else {}
    return get_all_inbounds(request, kwargs={'query': kwargs})


# 查是否已使用
def check_occupy(request, query):
    query_val = request.GET.get('val')
    kwargs = {query: query_val}
    count = Inbound.objects.filter(**kwargs).count()
    data = {'status': '200'} if count == 0 else {'status': '400'}
    return JsonResponse(data)
