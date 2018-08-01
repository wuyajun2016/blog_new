import json
import urllib.request
import pdb


class OAuth_Base(object):    # 基类，将相同的方法写入到此类中
    # 初始化，载入对应的应用id、秘钥和回调地址
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def _get(self, url, data):      # get方法
        # urlencode()主要作用就是将url附上要提交的数据,经过urlencode()转换后的data数据为?x=x
        request_url = '%s?%s' % (url, urllib.parse.urlencode(data))
        # 1、urlopen()的data参数默认为None，如果none就以get方式请求；
        # 2、当data参数不为空的时候，urlopen（）提交方式为Post
        response = urllib.request.urlopen(request_url)

        return response.read()

    def _post(self, url, data):    # post方法
        # Post的数据必须是bytes或者iterable of bytes，不能是str，如果是str需要进行encode()编码
        request = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
        response = urllib.request.urlopen(request)
        return response.read()

    # 下面的方法，不同的登录平台会有细微差别，需要继承基类后重写方法
    def get_auth_url(self):   # 获取code
        pass

    def get_access_token(self, code):   # 获取access token
        pass

    def get_open_id(self):    # 获取openid
        pass

    def get_user_info(self):   # 获取用户信息
        pass

    def get_email(self):   # 获取用户邮箱
        pass


# Github类
class OAuth_GITHUB(OAuth_Base):
    def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_url,
            'scope': 'user:email',  # 赋予读取邮箱的权限
            'state': 1,  # 防止跨站点攻击，其实应该是一个随机数
            'allow_signup': True  # 默认Ture就好了
        }
        # 请求github开放的登录接口
        url = 'https://github.com/login/oauth/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'code': code,  # 获取github登录时请求中带的参数code放到这里
            'redirect_url': self.redirect_url,
            'state': 1
        }
        # 请求github开放的获取token接口
        # response返回值类似：b'access_token=ea36760726575d972d36f3c32d05f3785069d112&scope=user%3Aemail&token_type=bearer'
        response = self._post('https://github.com/login/oauth/access_token', params)  # 此处为post方法
        # 通过urllib.parse.parse_qs将reponse转换成如下字典格式：
        # {b'access_token': [b'ea36760726575d972d36f3c32d05f3785069d105'],
        # b'scope': [b'user:email'], b'token_type': [b'bearer']}
        result = urllib.parse.parse_qs(response, True)
        self.access_token = result[b'access_token'][0]
        return self.access_token

    # github不需要获取openid，因此不需要get_open_id()方法
    def get_user_info(self):
        params = {'access_token': self.access_token}
        # 请求github开放的获取用户信息接口(带上token就可以请求成功了)
        response = self._get('https://api.github.com/user', params)
        # json.dumps:dict转成str
        # json.loads:str转成dict
        result = json.loads(response.decode('utf-8'))
        self.openid = result.get('id', '')
        return result

    def get_email(self):
        params = {'access_token': self.access_token}
        # 请求github开放的获取用户邮箱接口(带上token就可以请求成功了)
        response = self._get('https://api.github.com/user/emails', params)
        # response返回的是一个list，所以后面在转换成dict后，取数据时候使用了result[0]['email']
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']
