from django.shortcuts import render, HttpResponseRedirect
from home_login.views import is_user_login
from inbound_manage.models import Inbound
from django.forms import ModelForm
from purchase_manage.models import Purchase
from utils.utils import get_all, add_or_update


class InboundForm(ModelForm):
    class Meta:
        model = Inbound
        fields = '__all__'
        exclude = ['comments']
        error_messages = {
            'material_code': {'required': '请填写物料编号'},
            'quantity': {'required': '请填写入库数量',
                         'invalid': '请填写正确的入库数量'},
            'equipment_ID': {'required': '请填写设备ID'},
            'in_house_date': {'required': '请填写入库日期',
                              'invalid': '请填写正确的日期格式'},
            'status': {'required': '请填写设备状态'},
            'purchase_belong': {
                'invalid_choice': '请选择入库对应的采购订单'},
            'product_belong': {
                'invalid_choice': '请选择入库对应的采购产品'},
        }


# Create your views here.
def get_all_inbounds(request):
    return get_all(request=request, klass=Inbound)


def add_inbound(request):
    return add_or_update(request=request, klass=Inbound, form_class=InboundForm,
                         kwargs={'quote_class': [Purchase], 'reverse_url': 'inbound_related:all_inbounds_details'})
