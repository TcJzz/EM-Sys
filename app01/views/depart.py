from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from app01.utils.form import UserModelForm, UserEditModelForm
from app01.utils.Pagination import Pagination


def depart_list(request):
    """部门列表"""
    department = models.Department.objects.all()

    return render(request, 'depart_list.html', {'departments': department})


def depart_add(request):
    if request.method == "GET":
        return render(request, "depart_add.html")
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        if nid:
            models.Department.objects.filter(id=nid).delete()
            return redirect("/depart/list/")
        return render(request, "depart_delete.html")
    title = request.POST.get("title")
    models.Department.objects.filter(title=title).delete()
    return redirect("/depart/list/")


def depart_edit(request):
    if request.method == "GET":
        otitle = request.GET.get("otitle")
        if otitle:
            return render(request, "depart_edit.html", {"otitle": otitle})
        return render(request, "depart_edit.html")
    o_title = request.POST.get("title_origin")
    n_title = request.POST.get("title_new")

    exit = models.Department.objects.filter(title=o_title).update(title=n_title)

    if exit:
        models.Department.objects.filter(title=o_title).update(title=n_title)
        return redirect("/depart/list/")