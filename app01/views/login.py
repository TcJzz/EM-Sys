from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import LoginForm
from app01.utils.code import check_code
# io 用于生成和调用内存中的内容
from io import BytesIO


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request.POST)
    if form.is_valid():
        # 验证码的校验,获取到code的同时,将code从字典中踢出,以便下面在数据库中根据用户名和密码筛选用户
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        # 从网页中传入的数据是一个字典
        # {"name":"xxx","password":"xxx"}
        # 所以可以直接将获取到的字典用filter在数据库中进行筛选，前提！！！是在LoginForm中定义的字段名和数据库中的字段名一致
        login_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not login_object:
            # 添加错误信息，前面的属性是错误信息出现的位置对应的字段名
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 登录成功
        # 这一段就是通过request_session语句，将键值对' info '= {"name": login_object.username,"password": login_object.password}存贮到浏览器的session中
        request.session['info'] = {"id": login_object.id, "username": login_object.username,
                                   "password": login_object.password}
        # session的内容七天内有效
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/admin/list/')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    # 通过check_code函数生成图片验证码
    img, code_string = check_code()
    # 将创建的图片验证码中的文本存到session中,以便后续获取
    request.session['image_code'] = code_string
    # 给session设置超时,不能让验证码一直有效
    request.session.set_expiry(60)
    # 在内存中创建一个文件，并且将图片写入该文件中
    stream = BytesIO()
    img.save(stream, format='PNG')
    # 从内存中读取图片
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect('/login/')
