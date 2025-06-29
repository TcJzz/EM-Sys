"""
自定义分类组件
使用说明：
（在视图函数中）
def user_list(request):

    1、根据实际情况，在views中设置筛选的条件（即queryset），传入参数
    queryset = models.Employee.objects.filter(**data_dict).order_by("id")

    2、实例化分页对象
    page_object = Pagination(request, queryset)

    3、设置字典放入要传回的数据
    context = {
        "employee": page_object.page_queryset,  # 每一页展示的数据
        'name': name,  # 用户查询的内容（用来传回html，显示在搜索框中）
        "page_string": page_object.html()  # 用来生成分页栏
    }

    return render(request, "user_list.html", context)
（在html文件中）
    1、在表格中循环展示数据
    {%for obj in queryset%}
        {{obj.xxx}}
    {%endfor%}
    2、设置分页栏
    <div class="clearfix">
        <nav aria-label="Page navigation" class="clearfix">
            <ul class="pagination">
                {{ page_string }}
            </ul>
        </nav>
    </div>
"""
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_param="page", page_size=10, plus=2):
        """
        :param request:请求的对象
        :param queryset:符合条件的数据（根据这个数据进行分页处理）
        :param page_param:在URL中传递获取分页的参数，例如：/user/list/?page=11
        :param page_size:每页显示多少条数据
        :param plus:在分页栏中，显示当前页的前/后多少页
        """

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True  # 修改django.http.request.QueryDict中的源代码，让url可以进行拼接
        self.query_dict = query_dict  # 获取当前的url

        # 如果page_param对应的键不存在，则默认为"1"
        page = request.GET.get(page_param, "1")
        # 判断用户输入的页码是数字还是字符
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.plus = plus
        self.page_param = page_param

        self.start = (page - 1) * page_size
        self.end = self.start + page_size
        self.page_queryset = queryset[self.start:self.end]  # 每页所展示的数据的对象集

        # 页面总数
        data_counts = queryset.count()
        page_counts, div = divmod(data_counts, page_size)
        if div != 0:
            page_counts += 1
        self.page_counts = page_counts

    def html(self):
        # 初始化一个列表，用于存储分页栏的 HTML 片段
        page_str_list = []

        def build_link(page_num, text=None, active=False, aria_label=None):
            """
            构造单个分页 <li> 标签的 HTML 字符串
            参数：
                page_num: 要跳转的页码
                text: 显示在按钮上的文字或符号
                active: 是否为当前页，高亮显示
                aria_label: 无障碍辅助标签（给上一页 / 下一页按钮用）
            """
            self.query_dict.setlist(self.page_param, [page_num])  # 设置 URL 中的页码参数
            class_attr = ' class="active"' if active else ''  # 当前页高亮
            aria_attr = f' aria-label="{aria_label}"' if aria_label else ''
            span = f'<span aria-hidden="true">{text}</span>' if aria_label else text  # 图标用 span 包裹
            return f'<li{class_attr}><a href="?{self.query_dict.urlencode()}"{aria_attr}>{span}</a></li>'

        # 首页按钮，始终跳转到第 1 页
        page_str_list.append(build_link(1, "首页"))

        # 上一页按钮，页码最小为 1，防止为 0
        prev_page = max(1, self.page - 1)
        page_str_list.append(build_link(prev_page, "&laquo;", aria_label="Previous"))  # "&laquo;"就是向左的符号

        # 中间页码显示范围计算，避免显示负数或超过总页数
        if self.page < ((self.plus * 2 + 1) + 1) / 2:
            # 当前页靠近前面，展示前 self.plus*2+1 个页码
            page_range = range(1, min(self.page_counts + 1, 1 + 2 * self.plus + 1))
        elif self.page <= self.page_counts - self.plus:
            # 当前页在中间位置，左右各显示 self.plus 个页码
            page_range = range(self.page - self.plus, self.page + self.plus + 1)
        else:
            # 当前页靠近末尾，展示最后 self.plus*2 个页码
            start = max(1, self.page_counts - self.plus * 2)
            page_range = range(start, self.page_counts + 1)

        # 中间页码部分，当前页高亮
        for i in page_range:
            page_str_list.append(build_link(i, str(i), active=(i == self.page)))

        # 下一页按钮，最大不能超过总页数
        next_page = min(self.page_counts, self.page + 1)
        page_str_list.append(build_link(next_page, "&raquo;", aria_label="Next"))

        # 尾页按钮，跳转到最后一页
        page_str_list.append(build_link(self.page_counts, "尾页"))

        # 跳转表单，用户可以直接输入页码跳转
        jump_form = """
            <li>
                <form method="get" style="float:left;margin-left:-1px">
                    <input type="text" class="form-control" placeholder="页码" name="page"
                        style="position:relative;float:left;display:inline-block;width:80px;border-radius:0;">
                    <button class="btn btn-default" type="submit" style="border-radius:0">跳转</button>
                </form>
            </li>
        """
        page_str_list.append(jump_form)

        # 使用 mark_safe 防止 HTML 被 Django 自动转义
        return mark_safe(''.join(page_str_list))
