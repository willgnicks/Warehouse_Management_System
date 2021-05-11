from django.forms import ModelForm
from outbound_manage.models import Outbound
from utils.utils import get_all, put_one
from inbound_manage.models import Inbound
from project_manage.models import Project


class OutboundForm(ModelForm):
    class Meta:
        model = Outbound
        fields = '__all__'
        error_messages = {
            'products_name': {'required': '请填入项目名称'},
            'products_model': {'required': '请填入项目编号'},
            'products_type': {'required': '请填入项目编号'},
            'unit_price': {'required': '请填入项目编号'},
            'manufacturer': {'required': '请填入项目编号'},
            'project_code': {'required': '请填入项目编号'},
        }


# Create your views here.
def get_all_outbounds(request):
    return get_all(request=request, klass=Outbound)


def add_outbound(request):
    return put_one(request=request,
                   form_class=OutboundForm,
                   kwargs={'quote_class': [Inbound, Project], 'reverse_url': 'outbound_related:all_outbound_details'})
    # else:
    #     if ManufacturerForm(request.POST).is_valid():
    #         ManufacturerForm(request.POST).save()
    #         return HttpResponseRedirect(reverse('man:all_product_details'))
    #     else:
    #         return render(request, 'products/add.html', {'products': ManufacturerForm(request.POST)})
