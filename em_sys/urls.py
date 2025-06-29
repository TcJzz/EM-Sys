"""
URL configuration for em_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import depart, user, admin, login, task, order, chart

urlpatterns = [

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/edit/', depart.depart_edit),
    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/add/modelform/', user.user_add_modelform),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),
    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    # 登录
    path('login/', login.login),
    # 注销
    path('logout/', login.logout),
    # 生成验证码
    path('image/code/', login.image_code),
    # 初试Ajax
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    # 接收用户订单请求，并保存
    path('order/add/', order.order_add),
    # 删除订单
    path('order/delete/', order.order_delete),
    # 在修改订单弹窗中显示内容
    path('order/detail/', order.order_detail),
    # 保存订单编辑的内容
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/',chart.chart_bar),
]
