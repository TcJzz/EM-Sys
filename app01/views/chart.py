from django.http import JsonResponse
from django.shortcuts import render, redirect


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    """构造柱状图数据"""
    legend = ["销量", "业绩"]
    series = [
        {
            "name": "销量",
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": "业绩",
            "type": 'bar',
            "data": [20, 15, 38, 10, 12, 15]
        }
    ]
    x_list = [
        '衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series': series,
            'x_list': x_list,
        }
    }

    return JsonResponse(result)
