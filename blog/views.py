from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Tag, Poll
import markdown
from django.db.models import Q
from django.http import HttpResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import pdb
import socket


# 类似controller层，查询数据库，返回对应数据给前端展示
# 首页
def index(request):
    # category_id = list(Category.objects.filter(name='生活').values('id'))[0].get('id')    # 找出category名称为‘生活’的id，可再用这个id
    # post_list = Post.objects.exclude(category=category_id).order_by('-created_time')      # 再用这个id去过滤出对应该类目的文章
    post_list = Post.objects.filter(life=0).order_by('-created_time')
    # 调用分页方法，取出返回数据传给对应页面
    page_list = page_turn(request, post_list)
    post_count = page_list.get('post_count')
    paginator = page_list.get('paginator')
    page = page_list.get('page')
    currentPage = page_list.get('currentPage')
    totalPage = page_list.get('totalPage')
    post_list = page_list.get('post_list')

    return render(request, 'blog/index.html', locals())


# 详情页
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)    # django get操作，也就封装了一个返回对象为空时候的处理
    # 拿到文章对应的life值（用来过滤是否是生活相关主题）
    glife = Post.objects.filter(pk=pk).values('life')
    get_life = list(glife)[0].get('life')
    # 上一篇/下一篇
    # 取出全部文章，再拿该篇文章跟全部文章的title做比较，以用来判断当前文章处在第一/最后/中间
    if get_life == 1:
        page_list = list(Post.objects.filter(life=1))
    else:
        page_list = list(Post.objects.filter(life=0))
    # pdb.set_trace()
    if post == page_list[0]:
        before_page = None
        after_page = page_list[1]
    elif post == page_list[-1]:
        before_page = page_list[-2]
        after_page = None
    else:
        # index可以用来记录当前文章所在的位置索引
        situ = page_list.index(post)
        before_page = page_list[situ-1]
        after_page = page_list[situ+1]

    post.increase_views()      # 阅读量+1
    # 使用markdown.markdown使文章编写支持markdown语法
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    return render(request, 'blog/detail.html', context={'post': post, 'before_page': before_page, 'get_life': get_life,
                                                        'after_page': after_page})


# 归档跳转(目前没有使用)
# 注意下，这里的created_time 是 Python 的 date 对象
# 另外，created_time__year本来应当是created_time.year，由于这里当作参数故需要使用created_time__year
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 类目
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    # 调用分页方法，取出返回数据传给对应页面
    page_list = page_turn(request, post_list)
    post_count = page_list.get('post_count')
    paginator = page_list.get('paginator')
    page = page_list.get('page')
    currentPage = page_list.get('currentPage')
    totalPage = page_list.get('totalPage')
    post_list = page_list.get('post_list')
    return render(request, 'blog/list.html', locals())


# 搜索
def search(request):
    q = request.GET.get('keyboard')
    # post_list_all = Post.objects.all().order_by('-created_time')
    # if not q:
    #     return render(request, 'blog/index.html', {'post_list': post_list_all})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).filter(life=0)\
        .order_by('-created_time')
    # 调用分页方法，取出返回数据传给对应页面
    page_list = page_turn(request, post_list)
    post_count = page_list.get('post_count')
    paginator = page_list.get('paginator')
    page = page_list.get('page')
    currentPage = page_list.get('currentPage')
    totalPage = page_list.get('totalPage')
    post_list = page_list.get('post_list')

    return render(request, 'blog/index.html', locals())


def category_list(request):
    post_list = Post.objects.filter(life=0).order_by('-created_time')
    # 调用分页方法，取出返回数据传给对应页面
    page_list = page_turn(request, post_list)
    post_count = page_list.get('post_count')
    paginator = page_list.get('paginator')
    page = page_list.get('page')
    currentPage = page_list.get('currentPage')
    totalPage = page_list.get('totalPage')
    post_list = page_list.get('post_list')

    return render(request, 'blog/list.html', locals())


# 搜索
def search_list(request):
    q = request.GET.get('keyboard_list')
    # post_list_all = Post.objects.all().order_by('-created_time')
    # if not q:
    #     return render(request, 'blog/list.html', {'post_list': post_list_all})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).filter(life=0)
    # 调用分页方法，取出返回数据传给对应页面
    page_list = page_turn(request, post_list)
    post_count = page_list.get('post_count')
    paginator = page_list.get('paginator')
    page = page_list.get('page')
    currentPage = page_list.get('currentPage')
    totalPage = page_list.get('totalPage')
    post_list = page_list.get('post_list')

    return render(request, 'blog/list.html', locals())


# 获取用户ip
def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


# 点赞
def loves(request, pk):
    response_data = {}
    # 点击‘点赞’按钮时候先去增加对应文章的点击量
    post_list = get_object_or_404(Post, pk=pk)
    # 根据ip判断是否以及点赞过了
    # ip = get_ip(request)
    # if Poll.objects.filter(ip=ip, blog=post_list).exists():
    #     response_data["success"] = False
    #     response_data["tip"] = '<script>alert("您已点过赞！");window.history.back(-1);"</script>'
    #     return HttpResponse(json.dumps(response_data), content_type="application/json")
    # else:
    #     Poll.objects.create(ip=ip, blog_id=pk)
    post_list.increase_loves()
    # 获取对应文章的点赞量，拿到的是queryset对象
    to_laud = Post.objects.filter(pk=pk).values('loves')
    # ValuesQuerySet对象需要先转换成list,再取出list中的value
    to_laud_value = list(to_laud)[0].get('loves')

    # 测试下如果传递一个较为复杂的json给前端，前端解析：var json = eval(result);alert(json.list[0].fields.loves)
    # serializers.serialize可以这么序列化成json，如果是直接fitler或all的数据
    # response_data['list'] = json.loads(serializers.serialize('json', Post.objects.filter(pk=pk)))

    response_data["success"] = True
    response_data["loves"] = to_laud_value
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# life
def life(request):
    post_list = Post.objects.filter(life=1)
    # 调用分页方法，取出返回数据传给对应页面
    page_list = page_turn(request, post_list)
    post_count = page_list.get('post_count')
    paginator = page_list.get('paginator')
    page = page_list.get('page')
    currentPage = page_list.get('currentPage')
    totalPage = page_list.get('totalPage')
    post_list = page_list.get('post_list')
    return render(request, 'blog/life.html', locals())


def login(request):
    return render(request, 'blog/login.html')


# 分页方法
def page_turn(request, post_list):
    post_count = post_list.count()
    # 生成paginator对象,定义每页显示X条记录
    paginator = Paginator(post_list, 7)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    # 总页数
    totalPage = paginator.num_pages
    try:
        print(page)
        post_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        post_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    page_dict = {'post_count': post_count, 'paginator': paginator, 'page': page, 'currentPage': currentPage,
                 'totalPage': totalPage, 'post_list': post_list}
    return page_dict

