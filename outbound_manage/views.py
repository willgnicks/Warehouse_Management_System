from concurrent import futures
import json

from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from equipment_manage.models import Equipment
from outbound_manage.models import Outbound
from utils.utils import get_all, add_or_update, get_kwargs, get_bulk, transform_data, get_one
from inbound_manage.models import Inbound
from project_manage.models import Project
from django.views.decorators.http import require_http_methods

"""
    出库先给已经入库的项目选项，然后再给该项目采购入库的产品选项，该项目的入库产品多笔，那么就给当前的物料编号和设备ID的一一对应

"""


class OutboundForm(ModelForm):
    class Meta:
        model = Outbound
        fields = '__all__'
        exclude = ['flag', 'outbound_date']
        error_messages = {
            'contract_number': {'required': '请填写销售合同号'},
            'form_number': {'required': '请填写表单号'},
            'project_FK': {'required': '请填入项目编号'},
            # 'unit_price': {'required': '请填入项目编号'},
            'quantity': {'required': '请填入项目编号'},
            'demand_person': {'required': '请填写需求人姓名'},
        }


@require_http_methods(['GET'])
def get_one_outbound(request, pk):
    print(pk)
    pool = ThreadPoolExecutor(max_workers=5)
    def query(pk):
        return Outbound.objects.filter(flag=1, id=pk)

    future = pool.submit(query, pk)
    def return_render(result):
        return result
    # future.add_done_callback(return_render(future.result))
    print('-->', future.result)
    return JsonResponse({'s':'s'})


def get_all_outbounds(request):
    value_field = ['id',
                   'form_number',
                   'contract_number',
                   'demand_person',
                   'project__project_name',
                   'equipment__inbound__material_code',
                   'equipment__inbound__pp_rel__product__product_name',
                   'equipment__inbound__pp_rel__product__product_model',
                   'equipment__SN',
                   'outbound_date',

                   ]
    return get_all(request=request, klass=Outbound, kwargs={'value_field': value_field})


def add_outbound(request):
    if request.method == 'GET':
        equipments = Equipment.objects.filter(flag=1, status_code=0).values(
            *['id', 'SN', 'inbound__material_code', 'inbound__pp_rel__product__product_name',
              'inbound__pp_rel__product__product_model'])
        projects = Project.objects.filter(flag=1, project_status=2).values(*['id', 'project_name'])
        return render(request, 'outbounds/add.html', locals())
    else:
        package_data = json.loads(request.POST.get('package_data'))
        print(package_data)
        this_outbound = package_data.get('id')
        print(this_outbound)
        if this_outbound is not None:
            pass
        else:
            Outbound.objects.create(**get_kwargs(klass=Outbound, package_data=package_data))
            Project.objects.filter(id=package_data.get('project_id')).update(project_status=3)
            this_id = Outbound.objects.order_by('id').last().id
            for pk in package_data.get('equipment'):
                Equipment.objects.filter(id=pk).update(outbound_id=this_id, status_code=1)
        return JsonResponse({'status': '200'})
