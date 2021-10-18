import time

from django.forms import ModelForm
from lending_manage.models import Lending
from utils.utils import get_all, add_or_update
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse
from django.core import serializers


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
@require_http_methods(['GET'])
def get_all_lending(request):
    # response = {}
    # start = time.time()
    # try:
    #     lending = Lending.objects.all().filter(flag=1)
    #     response['lendings'] = json.loads(serializers.serialize('json', lending))
    #     response['msg'] = 'success'
    #     response['error_num'] = 0
    # except Exception as e:
    #     response['msg'] = str(e)
    #     response['error_num'] = 1
    # print(time.time() - start)
    # return JsonResponse(response)
    return get_all(request=request, klass=Lending)


# 新增借测只能借测在库的设备
@require_http_methods(['GET', 'POST'])
def add_lending(request):
    return add_or_update(request=request,
                         klass=Lending,
                         form_class=LendingForm,
                         kwargs={'reverse_url': 'lending_related:all_lending_details'})
    # else:
    #     if ManufacturerForm(request.POST).is_valid():
    #         ManufacturerForm(request.POST).save()
    #         return HttpResponseRedirect(reverse('man:all_product_details'))
    #     else:
    #         return render(request, 'products/add.html', {'products': ManufacturerForm(request.POST)})
