from django.conf.urls import url
from . import views
from django.conf import settings
from django.views.static import serve


# 请求地址和controller的映射
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),    # (?P<pk>[0-9]+)为命名捕获组，获取匹配的文章id并且传递给视图函数
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    # 作用：
    # 1 在.html中根据url模式，解析出链接
    # 2 访问链接后，找到url路由，将链接中的某参数进行捕获，然后传递给对应视图函数
    # 3 执行视图函数，返回结果，渲染页面
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),   # django上传图片
    url(r'^search/$', views.search, name='search'),
    url(r'^search_list/$', views.search_list, name='search_list'),
    url(r'^loves/(?P<pk>[0-9]+)/$', views.loves, name='loves'),
    url(r'^category/$', views.category_list, name='category_list'),
    url(r'^life/$', views.life, name='life'),
    url(r'^login/$', views.login, name='login'),
]
