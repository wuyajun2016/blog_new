from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from .oauth_client import OAuth_Base,OAuth_GITHUB
from .models import OAuth_ex, OAuth_type
from django.contrib.auth import login as auth_login
from user.models import User
from django.core.urlresolvers import reverse
import time
import uuid
from .forms import BindEmail
from django.http import HttpResponse
import pdb


def git_login(request):   # 获取code
    oauth_git = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
    url = oauth_git.get_auth_url()
    return HttpResponseRedirect(url)


def git_check(request):
    type = '1'
    request_code = request.GET.get('code')
    oauth_git = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
    try:
        access_token = oauth_git.get_access_token(request_code)   # 获取access token
        time.sleep(0.1)    # 此处需要休息一下，避免发送urlopen的10060错误
    except:  # 获取令牌失败，反馈失败信息
        data = dict()
        data['goto_url'] = '/'
        data['goto_time'] = 10000
        data['goto_page'] = True
        data['message_title'] = '登录失败'
        data['message'] = '获取授权失败，请确认是否允许授权，并重试。若问题无法解决，请联系网站管理人员'
        return render_to_response('blog/response.html', data)
    infos = oauth_git.get_user_info()   # 获取用户信息
    nickname = infos.get('login', '')
    image_url = infos.get('avatar_url', '')
    # oauth_git.openid这样可以直接取到方法中的返回的self.openid
    open_id = str(oauth_git.openid)
    signature = infos.get('bio', '')
    if not signature:
        signature = "无个性签名"
    githubs = OAuth_ex.objects.filter(openid=open_id, oauth_type=type)   # 查询是否该第三方账户已绑定本网站账号
    if githubs:   # 若已绑定，直接登录
        auth_login(request, githubs[0].user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/')
    else:   # 否则尝试获取用户邮箱用于绑定账号
        try:
            email = oauth_git.get_email()
        except:   # 若获取失败，则跳转到绑定用户界面，让用户手动输入邮箱
            url = "%s?nickname=%s&openid=%s&type=%s&signature=%s&image_url=%s" % (reverse('user:bind_email'), nickname,
                                                                                  open_id, type, signature, image_url)
            return HttpResponseRedirect(url)
    users = User.objects.filter(email=email)   # 若获取到邮箱，则查询是否存在本站用户
    if users:   # 若存在，则直接绑定
        user = users[0]
    else:   # 若不存在，则新建本站用户
        while User.objects.filter(username=nickname):   # 防止用户名重复
            nickname = nickname + '*'
        user = User(username=nickname, email=email)
        pwd = str(uuid.uuid1())   # 随机设置用户密码
        user.set_password(pwd)
        user.is_active = True
        user.save()
    oauth_type = OAuth_type.objects.get(id=type)  # 找到oauth_type中的对应type的id（可能有多个登录方式，所以有这表）
    oauth_ex = OAuth_ex(user=user, openid=open_id, oauth_type=oauth_type)
    oauth_ex.save()    # 保存后登陆
    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    data = dict()    # 反馈登陆结果
    data['goto_url'] = '/'
    data['goto_time'] = 10000
    data['goto_page'] = True
    data['message_title'] = '绑定用户成功'
    data['image_url'] = image_url
    data['message'] = u'绑定成功！您的用户名为：<b>%s</b>。您现在可以同时使用本站账号和此第三方账号登录本站了！' % nickname
    return render_to_response('blog/response.html', data)


# 检查是否为登录状态
def check_is_login(request):
    if request.user.is_authenticated():
        user = request.user.username
        returnText = u'''你好,<a href="/blog/user_center">%s</a>''' % (user)
    else:
        returnText = u''' <a href="/login">登录</a>'''
    return HttpResponse(returnText, content_type="application/json")


# 用户中心(进入用户中心时判断下是否已经登录了，如果已经登录了才放行)
# django中使用request.user.is_authenticated()来判断是否已登录
def user_center(request):
    if request.user.is_authenticated():
        user = request.user
        return render_to_response('blog/usercenter.html', locals())
    else:
        return render_to_response('/login.html')


# 看了下，github注册时候邮箱是必填的，所以应当都能获取到，这个方法尚未得到测试
def bind_email(request):   # 使用户手动填写邮箱，绑定本站账号，因此需要一个BindEmail表单
    sex = request.GET.get('sex', request.POST.get('sex', ''))
    openid = request.GET.get('openid', request.POST.get('openid', ''))
    nickname = request.GET.get('nickname', request.POST.get('nickname', ''))
    type = request.GET.get('type', request.POST.get('type', ''))
    signature = request.GET.get('signature', request.POST.get('signature', ''))
    image_url = request.GET.get('image_url', request.POST.get('image_url', ''))
    if request.method == 'POST':
        form = BindEmail(request.POST)
        if form.is_valid():
            openid = form.cleaned_data['openid']
            nickname = form.cleaned_data['nickname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            type = form.cleaned_data['type']
            signature = form.cleaned_data['signature']
            image_url = form.cleaned_data['image_url']
            sex = form.cleaned_data['sex']
            users = User.objects.filter(email=email)
            if users:
                user = users[0]
            else:
                while User.objects.filter(username=nickname):
                    nickname = nickname + '*'
                user = User(username=nickname, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
            oauth_type = OAuth_type.objects.get(id=type)
            oauth_ex = OAuth_ex(user=user, openid=openid, oauth_type=oauth_type)
            oauth_ex.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            data= {}
            data['goto_url'] = '/'
            data['goto_time'] = 10000
            data['goto_page'] = True
            data['message_title'] = '绑定账号成功'
            data['message'] = u'绑定成功！您的用户名为：<b>%s</b>。您现在可以同时使用本站账号和此第三方账号登录本站了！' % nickname
            return render_to_response('blog/response.html', data)
    else:
        form = BindEmail(initial={
            'openid': openid,
            'nickname': nickname,
            'type': type,
            'signature': signature,
            'image_url': image_url,
            'sex': sex,
        })
    return render(request, 'blog/form.html', context={'form': form, 'nickname': nickname, 'type': type})
