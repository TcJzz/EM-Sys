from django import forms
from app01.utils.bootstrap import BootstrapModelForm, BootstrapForm
from app01 import models
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5


class UserModelForm(BootstrapModelForm):
    # 加上用户输入内容的限定条件
    name = forms.CharField(
        min_length=3,
        label="姓名"
    )

    def clean_name(self):
        txt_name = self.cleaned_data['name']
        exist = models.Employee.objects.filter(name=txt_name).exists()
        if exist:
            raise ValidationError("该用户已存在")
        return txt_name

    class Meta:
        model = models.Employee
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 下面这个for循环的name是field中的元素的名字
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


class UserEditModelForm(BootstrapModelForm):
    # 加上用户输入内容的限定条件
    name = forms.CharField(label="姓名")

    def clean_name(self):
        txt_name = self.cleaned_data['name']
        # self.instance.pk就是当前数据对应的id，pk就是primary key
        exist = models.Employee.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exist:
            raise ValidationError("该用户已存在")
        return txt_name

    class Meta:
        model = models.Employee
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        # 让输入的密码变成星号,render_value使出现错误提示之后，输入框不会置空
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            # 让输入的密码变成星号,render_value使出现错误提示之后，输入框不会置空
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data['password']
        md5_pwd = md5(pwd)
        if models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists():
            raise ValidationError("新密码不能与原密码一致")
        return md5(pwd)

    # 使用clean_data()获取页面通过POST发送过来的所有数据
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if password != confirm_password:
            raise ValidationError("密码不一致")
        # 返回的这个值让clean_后的字段名赋上这个值
        return confirm_password


class AdminEditModelForm(BootstrapModelForm):

    def clean_username(self):
        txt_name = self.cleaned_data['username']
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(username=txt_name).exists()
        if exists:
            raise ValidationError("该用户已存在")
        return txt_name

    class Meta:
        model = models.Admin
        fields = [
            "username"
        ]


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        # 让输入的密码变成星号,render_value使出现错误提示之后，输入框不会置空
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            # 让输入的密码变成星号,render_value使出现错误提示之后，输入框不会置空
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data['password']
        md5_pwd = md5(pwd)
        if models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists():
            raise ValidationError("新密码不能与原密码一致")
        return md5(pwd)

    # 使用clean_data()获取页面通过POST发送过来的所有数据
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if password != confirm_password:
            raise ValidationError("密码不一致")
        # 返回的这个值让clean_后的字段名赋上这个值
        return confirm_password


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="姓名",
        # 说明此字段是必填字段
        required=True
    )
    password = forms.CharField(
        label="密码",
        required=True,
        widget=forms.PasswordInput(render_value=True)
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        return md5(pwd)


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Tasks
        fields = [
            "title",
            "level",
            "detail",
            "user"
        ]
        widgets = {
            "detail": forms.TextInput(),
            # "detail": forms.Textarea(),
        }
        # 也可以写成
        # fields = "__all__"


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # 不想让用户输入订单号
        exclude = ["oid","uid"]