from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

# 此blog_tags.py文件下存放模板标签

register = template.Library()


# 目前没有用到
# 获取前5篇文章,并使用@register.simple_tag方式注册到为模板函数（django的规定）
# 这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.filter(life=0).order_by('-created_time')[:num]


# 获取点击率最高的前5篇文章
@register.simple_tag
def get_click_post(num=5):
    return Post.objects.filter(life=0).order_by('-views')[:num]


# 获取文章的创建日期（这个dates会返回一个创建时间的列表，且为date对象），精确到月份，并按照倒叙排列
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 获取分类
@register.simple_tag
def get_category():
    return Category.objects.filter(post__life=0)


# 获取分类以及对应分类下的文章数量
# 在前端调用{{ category.num_posts }}即可获得对应分类下的文章数量
@register.simple_tag
def get_category_article_nums():
    return Category.objects.filter(post__life=0).annotate(num_posts=Count('post'))
