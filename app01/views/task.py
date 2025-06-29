import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.form import TaskModelForm


def task_list(request):
    form = TaskModelForm()
    return render(request, 'task_list.html', {"form": form})


@csrf_exempt
def task_add(request):
    print(request.GET)
    print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        # json.dumps()将内容转换为json格式
        return HttpResponse(json.dumps(data_dict))
    print(type(form.errors))
    data_dict = {"status": False, "errors": form.errors}
    # ensure_ascii = False 将
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    # 将form中的错误信息（ErrorDict格式）转换为json格式，传回前端浏览器
    # data_dict = {"status": False, 'error': form.errors.as_json()}
    # return HttpResponse(json.dumps(data_dict))
