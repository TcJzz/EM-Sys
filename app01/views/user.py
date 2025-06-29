from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from app01.utils.form import UserModelForm, UserEditModelForm
from app01.utils.Pagination import Pagination


def user_list(request):
    # 用户查询功能
    data_dict = {}
    # 有值拿值没值拿字符串
    name = request.GET.get('name', '')
    if name:
        # 将"name"中含有name的数据筛选出来
        data_dict["name__contains"] = name
    # 自己用queryset配置搜索条件，然后传入Pagination类
    queryset = models.Employee.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset)
    employee = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "employee": employee,  # 每一页展示的数据
        'name': name,  # 用户查询的内容（用来传回html，显示在搜索框中）
        "page_string": page_string  # 用来生成分页栏
    }

    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices': models.Employee.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    ctime = request.POST.get("ctime")
    gender = request.POST.get("gender")
    dp = request.POST.get("dp")

    models.Employee.objects.create(name=name, password=password, age=age, account=account, create_time=ctime,
                                   gender=gender,
                                   depart_id=dp)

    return redirect("/user/list/")


def user_add_modelform(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add_modelform.html", {"form": form})
    # 校验是否所有数据都填写
    form = UserModelForm(request.POST)
    if form.is_valid():
        # form.save直接将获取到的数据保存到UserModelForm中定义的表中
        form.save()
        return redirect("/user/list/")
    else:
        # form是从用户那得到的信息，里面包含错误信息form.errors
        return render(request, "user_add_modelform.html", {"form": form})


def user_edit(request, nid):
    # 从数据库中获得nid对应的数据，然后实例化对象
    if request.method == "GET":
        row_object = models.Employee.objects.filter(id=nid).first()
        form = UserEditModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    row_object = models.Employee.objects.filter(id=nid).first()
    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.Employee.objects.filter(id=nid).delete()
    return redirect("/user/list/")
