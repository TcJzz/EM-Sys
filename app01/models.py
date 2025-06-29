from django.db import models


class Admin(models.Model):
    username = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)

    # 当外键连接的时候，返回to_field对应id的name
    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=32)

    # 当别的表的外键to_field="title"的时候，返回这个对象的“title”
    def __str__(self):
        return self.title


class Employee(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')
    # 通过外键将depart和表Department相关联，约束depart列只能用Department中已有的id
    # -to 相关联的表
    # -to_filed 相关表中相关的列
    # django会在生成的表中自动将depart列的名称写为depart_id
    # 如果某个部门被删除
    # 1、将员工删除、联级删除Em
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # 2、将相关的列置空
    depart = models.ForeignKey(verbose_name='部门', to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)

    # 在Django中为表添加约束
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=1)


class Num_manage(models.Model):
    numbers = models.CharField(verbose_name="电话号码", max_length=11)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    level_choice = (
        (1, "普通"),
        (2, "稀有"),
        (3, "超稀有")
    )
    level = models.SmallIntegerField(verbose_name="稀有度", choices=level_choice, default=1)
    state_choice = (
        (1, "已占用"),
        (2, "未占用")
    )
    state = models.SmallIntegerField(verbose_name="占用状态", choices=state_choice, default=2)


class Tasks(models.Model):
    """任务"""
    level_choice = (
        (1, '紧急'),
        (2, '重要'),
        (3, '临时'),
    )
    title = models.CharField(verbose_name="标题", max_length=64)
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=2)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to=Admin, to_field="id", on_delete=models.CASCADE)  # 联级删除


class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=32)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    statu_choices = [
        (1, "已支付"),
        (2, "未支付"),
    ]
    statu = models.SmallIntegerField(verbose_name="状态", choices=statu_choices, default=2)
    uid = models.ForeignKey(verbose_name="管理员id", to=Admin, to_field="id", on_delete=models.CASCADE)
