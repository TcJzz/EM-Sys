from django.http import JsonResponse
from django.shortcuts import render
from app01.utils.form import OrderModelForm
from datetime import datetime
import random
from app01 import models
from app01.utils.Pagination import Pagination
from django.views.decorators.csrf import csrf_exempt


def order_list(request):
    form = OrderModelForm(data=request.GET)
    data_dict = {}
    title = request.GET.get('title', '')
    if title:
        data_dict['title__contains'] = title
    queryset = models.Order.objects.filter(**data_dict).order_by('-id')
    page_object = Pagination(request, queryset)
    order = page_object.page_queryset
    page_string = page_object.html()
    context = {
        "order": order,
        "title": title,
        "page_string": page_string,
        "form": form,
    }
    if request.method == 'GET':
        return render(request, "order_list.html", context)


def order_add(request):
    print("order_add后台接收到的信息是：")
    print("info.in:" + str(request.session.get('info').get('id')))
    """ajax请求创建订单"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # instance后面的字段名必须是数据库中字段名的真实字段名（例如uid的真实字段名是uid_id,因为uid是外键）
        form.instance.uid_id = request.session['info']['id']
        # 创建订单的时候自动生成订单号添加到数据库中
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 直接把当前登录的管理员当作该订单的管理员
        form.save()
        # return HttpResponse(json.dumps({"status":True}))
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'errors': form.errors})


def order_delete(request):
    delete_id = request.GET.get('dlt_id')
    print(delete_id)
    delete_obj = models.Order.objects.filter(id=delete_id).first()
    print(delete_obj)
    if not delete_obj:
        return JsonResponse({'status': False, "error": "数据不存在1"})
    models.Order.objects.filter(id=delete_id).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def order_detail(request):
    order_id = request.GET.get('edt_id')
    order_obj = models.Order.objects.filter(id=order_id).first()
    if not order_obj:
        return JsonResponse({"status": False, "errors": "数据不存在2"})
    result = {
        "status": True,
        "data": {
            "title": order_obj.title,
            "price": order_obj.price,
            "statu": order_obj.statu,
        }
    }
    return JsonResponse(result)


def order_edit(request):
    order_id = request.GET.get('edt_id')
    order_obj = models.Order.objects.filter(id=order_id).first()
    if not order_obj:
        return JsonResponse({"status": False, "errors": "订单不存在"})
    form = OrderModelForm(data=request.POST, instance=order_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, "errors": form.errors})