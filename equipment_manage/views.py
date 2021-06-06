from django.shortcuts import render

from equipment_manage.models import Equipment
from utils.utils import get_all


def get_all_equips(request):
    values_fields = ['id',
                     'SN',
                     'inbound__material_code',
                     'inbound__in_house_date',
                     'status_code',
                     'inbound__pp_rel__purchase__project__project_name',
                     'inbound__pp_rel__product__product_name',
                     'inbound__pp_rel__product__product_model',
                     ]
    return get_all(request,
                   klass=Equipment,
                   kwargs={
                       'value_field': values_fields, })
