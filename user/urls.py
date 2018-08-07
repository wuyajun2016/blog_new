from django.conf.urls import url
from . import views


# 请求地址和controller的映射
app_name = 'user'
urlpatterns = [
    url(r'git_login', views.git_login, name='git_login'),
    url(r'git_check', views.git_check, name='git_check'),
    url(r'bind_email', views.bind_email, name='bind_email'),   # 通过邮箱将第三方账户绑定到本站账号
    url(r'user_center', views.user_center, name='user_center'),
    url(r'check_is_login', views.check_is_login, name='check_is_login'),
    url(r'nickname_change', views.nickname_change, name='nickname_change'),
]
