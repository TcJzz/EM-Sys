from django.shortcuts import render, redirect
from app01 import models
from app01.utils.Pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm,AdminResetModelForm


def admin_list(request):
    # 从浏览器中获取session，检查用户是否登录
    info = request.session.get('info')
    if not info:
        return redirect('/login/')

    # 用户查询功能
    data_dict = {}
    # 有值拿值没值拿字符串
    search = request.GET.get('search', '')
    if search:
        # 将"search"中含有name的数据筛选出来
        data_dict["username__contains"] = search
    # 自己用queryset配置搜索条件，然后传入Pagination类
    queryset = models.Admin.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset)
    username = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "username": username,  # 每一页展示的数据
        'name_search': search,  # 用户查询的内容（用来传回html，显示在搜索框中）
        "page_string": page_string  # 用来生成分页栏
    }

    return render(request, "admin_list.html", context)


def admin_add(request):
    # 添加管理员
    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title, 'action': 'admin/add/'})


def admin_edit(request, nid):
    # 通过url编辑管理员信息
    row_object = models.Admin.objects.filter(id=nid).first()
    # 让标题后面加上当前修改信息的对象的username
    title = '编辑管理员信息' + '-{}'.format(row_object.username)
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        if not row_object:
            return render(request, "error.html", {'error': "该用户不存在"})
        return render(request, "change.html", {'form': form, "title": title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    title = '重置密码' + '-{}'.format(row_object.username)
    if request.method == 'GET':
        form = AdminResetModelForm(instance=row_object)
        if not row_object:
            return render(request, "error.html", {'error': "该用户不存在"})
        return render(request, "change.html", {'form': form, "title": title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})
