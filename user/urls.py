from django.conf.urls import url
from . import views


# 请求地址和controller的映射
app_name = 'user'
urlpatterns = [
    url(r'git_login', views.git_login, name='git_login'),
    url(r'git_check', views.git_check, name='git_check'),
    url(r'bind_email', views.bind_email, name='bind_email'),   # 通过邮箱将第三方账户绑定到本站账号
]
