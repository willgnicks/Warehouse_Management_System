import time
from datetime import datetime
import string
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, Model

from product_manage.models import PurchaseProductRel


def get_kwargs(klass, package_data):
    """
    将数据包中的数据和类字段形成一对一字典
    @param klass: 需要实例化的模型
    @param package_data: 该模型数据
    @return:
    """
    print('get_kwargs: 整理m2m中one')
    obj_fields = klass._meta.fields
    kwargs = {}
    # 对值不为空的字段填充
    for i in range(len(obj_fields)):
        att_name = obj_fields[i].attname
        att_val = package_data.get(att_name)
        if att_val is not None:
            kwargs[att_name] = att_val
        # else:
        #     kwargs[att_name] = None
    return kwargs


def get_pageData(paginator, pageNumber):
    return paginator.page(pageNumber)


def get_bulk(rel_klass, args, original=None):
    """
           1.args' length equals length of original queryset
           2.if original queryset is None means that this is a create action, no need to modify models' data
    @param rel_klass: m2m middle model
    @param args: m2m model key-value dict list
    @param original: queryset
    @return:
    """
    print('get_bulk: 获取bulk')
    if original:
        for index in range(len(args)):
            original[index].__dict__.update(**args[index])
        return original
    else:
        pp_rel_bulk = []
        for kwargs in args:
            pp_rel = rel_klass(**kwargs)
            pp_rel_bulk.append(pp_rel)
        return pp_rel_bulk


def get_model_name(klass):
    return klass.__name__.lower() + 's'


def get_model_name_from_modelform(klass):
    # python 3.9以上可以使用removesuffix('form')代替[:-4]
    return klass.__name__.lower()[:-4] + 's'


# 获取所有模型数据
def get_all(request, klass, **kwargs):
    """
    :param request:
    :param klass:   传入检索的类名 用来生成该类的queryset和生成render所需的template路径
    :param kwargs:   {query:query_dic,rel:rel_val} query（查询的条件）和rel（其他需要返回的关系类名）的写法固定，query_set和rel_val根据需要检索的不同而不同
    :return:  返回klass对应的template的render，调用该方法返回render即可
    """
    # 获取实参类的类名
    class_name = get_model_name(klass=klass)
    template_url = f'{class_name}/{class_name}.html'
    print(time.time())
    # 获取查询的内容，根据查询的内容生成q，如果q为空，即没有任何where条件
    query_dic = kwargs.get('kwargs').get('query') if kwargs else {}
    q = Q()
    if query_dic:
        for query in query_dic:
            q.add(Q(**{query: query_dic[query]}), Q.OR)
    # 生成结果集
    values_fields = kwargs.get('kwargs').get('value_field') if kwargs.get('kwargs') is not None else None
    print(values_fields)
    queryset = klass.objects.all().filter(flag=True).filter(
        q).values(*values_fields) if values_fields is not None else klass.objects.all().filter(flag=True).filter(q)
    # 生成分页器
    paginator = Paginator(queryset, 10)
    # 获取当前页面值
    page_number = request.GET.get('page') if request.GET.get('page') is not None else 1
    # 获取页面数据
    page_data = get_pageData(paginator, pageNumber=page_number)
    # 获取关系类名
    rel_val = kwargs.get('kwargs').get('rel') if kwargs else None
    rel_set = []
    # 如果有关系，那么返回该关系的结果集
    if rel_val is not None:
        for index in range(len(queryset)):
            print(queryset[index].unit_price)
            rel_set.insert(index, queryset[index].__getattribute__(rel_val))
    print(class_name, '&', template_url)
    print(time.time())
    return render(request,
                  template_url,
                  {
                      'count': paginator.count,
                      class_name: page_data,
                      rel_val: rel_set
                  }
                  )


# 更新或增加
def add_or_update(request, klass, form_class, **kwargs):
    """
    :param request:
    :param klass:
    :param form_class: 传入添加的modelform类名
    :param kwargs: {quote_class:[quote_class_list], title: title_val, reverse_url: url_val}
                   quote_class: 需要额外查询的类名列表
                   reverse_url: redirect的url，app_name:name
    :return:
    """
    # 获取表单类中的模型类名
    print(time.time())
    model_name = get_model_name_from_modelform(form_class)
    # put方法的html路径
    template_url = f'{model_name}/add.html'
    print(template_url)
    # 获取引用类列表, 无值只传title
    quote_class_list = kwargs.get('kwargs').get('quote_class')
    quote_dic = {}
    # 根据列表循环将引用类类名和该类的queryset形成键值对
    if quote_class_list is not None:
        quote_dic = {get_model_name(k): k.objects.all() for k in quote_class_list}
        # for k in quote_class_list:
        #     quote_dic[get_model_name(k)] = k.objects.all()
    # print(quote_dic)
    if request.method == 'GET':
        # 第一次get请求页面， 此时为新增的页面
        print(time.time())
        return render(request, template_url, quote_dic)
    else:
        print(request.method)
        # 第一次post请求，根据id的值来判断是新增还是更新
        # 如果有id，那么就是update
        # 如果没有id，那么就是save
        modelform_instance = form_class(request.POST)
        return_dic = {model_name: modelform_instance}
        # 如果id有那么下次还是将id的实例回显
        this_id = request.POST.get('id')
        print(this_id)
        if this_id:
            obj = klass.objects.filter(id=this_id).first()
            return_dic[model_name[:-1]] = obj
            print(obj)
            modelform_instance = form_class(request.POST, instance=obj)
        # 表单验证通过
        if modelform_instance.is_valid():
            modelform_instance.save()
            return HttpResponseRedirect(
                reverse(
                    kwargs.get('kwargs').get('reverse_url')
                )
            )
        # 验证不通过
        else:
            for key in quote_dic:
                return_dic[key] = quote_dic.get(key)
            print(return_dic)
            print(time.time())
            return render(request, template_url, return_dic)


# 删除模型
def delete_one(pk, klass, **kwargs):
    klass.objects.filter(id=pk).update(flag=False)
    return HttpResponseRedirect(
        reverse(
            kwargs.get('kwargs').get('reverse_url')))


# 根据pk获取模型
def get_one(request, klass, **kwargs):
    """
    @param request:
    @param klass: 参数包括主键 模型名 引用模型名 标题
                  主键 模型名 标题不能为空
    @param kwargs: {id:pk,title:title_val,quote_class:quote_class_list}
                   id: 主键
                   title: 页面回显标题
                   quote_class: 引用类列表
    @return:
    """
    # template url
    class_name = get_model_name(klass=klass)
    routine = f'{class_name}/add.html'
    # pk
    pk = kwargs.get('kwargs').get('pk')
    obj = klass.objects.filter(id=pk).first()
    # quote classes data
    quote_class_list = kwargs.get('kwargs').get('quote_class')
    return_dic = {class_name[:-1]: obj}
    if quote_class_list is not None:
        for klass in quote_class_list:
            return_dic[get_model_name(klass)] = klass.objects.all()
    return render(request, routine, return_dic)
