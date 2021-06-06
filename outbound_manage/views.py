from django.forms import ModelForm
from outbound_manage.models import Outbound
from utils.utils import get_all, add_or_update
from inbound_manage.models import Inbound
from project_manage.models import Project

"""
    出库先给已经入库的项目选项，然后再给该项目采购入库的产品选项，该项目的入库产品多笔，那么就给当前的物料编号和设备ID的一一对应

"""


class OutboundForm(ModelForm):
    class Meta:
        model = Outbound
        fields = '__all__'
        exclude = ['flag', 'outbound_date']
        error_messages = {
            'contract_number': {'required': '请填入项目名称'},
            'form_number': {'required': '请填入项目编号'},
            'project_FK': {'required': '请填入项目编号'},
            # 'unit_price': {'required': '请填入项目编号'},
            'quantity': {'required': '请填入项目编号'},
            'request_person': {'required': '请填入项目编号'},
        }


# Create your views here.
def get_all_outbounds(request):
    return get_all(request=request, klass=Outbound)


def add_outbound(request):
    return add_or_update(request=request,
                         klass=Outbound,
                         form_class=OutboundForm,
                         kwargs={'quote_class': [Inbound, Project],
                                 'reverse_url': 'outbound_related:all_outbound_details'})
