from django.shortcuts import render, HttpResponseRedirect
from home_login.views import is_user_login
from manufacturer_manage.models import Manufacturer
from django.forms import ModelForm
from lending_manage.models import Lending
from utils.utils import get_all, add_or_update


class LendingForm(ModelForm):
    class Meta:
        model = Lending
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
def get_all_lendings(request):
    return get_all(request=request, klass=Lending)


def add_lending(request):
    return add_or_update(request=request,
                         form_class=LendingForm,
                         kwargs={'reverse_url': 'lending_related:all_lending_details'})
    # else:
    #     if ManufacturerForm(request.POST).is_valid():
    #         ManufacturerForm(request.POST).save()
    #         return HttpResponseRedirect(reverse('man:all_product_details'))
    #     else:
    #         return render(request, 'products/add.html', {'products': ManufacturerForm(request.POST)})
