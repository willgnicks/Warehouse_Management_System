from django.shortcuts import render, HttpResponseRedirect
from home_login.views import is_user_login
from manufacturer_manage.models import Manufacturer
from django.forms import ModelForm
from django.urls import reverse


# class ManufacturerForm(ModelForm):
#     class Meta:
#         model = Manufacturer
#         fields = '__all__'
#         error_messages = {
#             'products_name': {'required': '请填入项目名称'},
#             'products_model': {'required': '请填入项目编号'},
#             'products_type': {'required': '请填入项目编号'},
#             'unit_price': {'required': '请填入项目编号'},
#             'manufacturer': {'required': '请填入项目编号'},
#             'project_code': {'required': '请填入项目编号'},
#         }


# Create your views here.
def get_all_receptions(request):
    if is_user_login(request):
        return render(request, 'receptions/receptions.html')


def add_reception(request):
    if is_user_login(request):
        if request.method == 'GET':
            return render(request, 'receptions/add.html')
        # else:
        #     if ManufacturerForm(request.POST).is_valid():
        #         ManufacturerForm(request.POST).save()
        #         return HttpResponseRedirect(reverse('man:all_product_details'))
        #     else:
        #         return render(request, 'products/add.html', {'products': ManufacturerForm(request.POST)})
