from manufacturer_manage.models import Manufacturer
from django.forms import ModelForm
from utils.utils import get_all, put_one


class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        exclude = ['flag']
        error_messages = {
            'manufacturer_name': {'required': '请输入供应商名称'},
            'manufacturer_linkman': {'required': '请输入供应商联系人'},
            'manufacturer_contact': {'required': '请输入联系人联系方式'},
            'is_cooperated': {'required': '请选择合作状态'},
            'cooperation_begin_date': {'required': '请选择开始合作日期', 'invalid': '请输入正确的日期格式'},
        }


# Create your views here.
def get_all_manufacturers(request):
    return get_all(request=request, klass=Manufacturer)


def add_manufacturer(request):
    return put_one(request=request, form_class=ManufacturerForm,
                   kwargs={'reverse_url': 'manufacturer_related:all_manufacturer_details'})
