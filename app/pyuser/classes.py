# -*- coding: utf-8 -*-
# 创建令牌环类
from django.conf import settings
import base64
from itsdangerous import URLSafeTimedSerializer as utsr
import redis
import hashlib
import datetime


class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self, useremail):  # 生成令牌环
        serializer = utsr(self.security_key)
        return serializer.dumps(useremail, self.salt)  # 转换为json格式化数据

    def comfirm_validate_token(self, token, expiration=3600):  # 验证令牌环合法
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)  # 解析json数据


# #实例化令牌环类
token_confirm = Token(settings.SECRET_KEY)

r = redis.StrictRedis(host='localhost', port='6379', db=0)


class UserSystem(object):
    def __init__(self, request, response=None, uid=0, **kwargs):
        self.request = request
        self.response = response
        self.uid = uid  # user id
        self.sessionid = None
        self.kwargs = kwargs

    def test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get_user_obj(self):
        """ 判断用户是否已登录  """
        self.sessionid = self.request.COOKIES.get('sessionid', None)      #获取浏览器cookie中的seesion_id
        if r.exists('sessionid:%s' % self.sessionid):
            return r.hget('sessionid:%s' % self.sessionid, 'uid')
        return None

    def set_cookie_and_session(self):
        """ 登录成功后写入cookie和session"""
        self.sessionid = self.request.COOKIES.get('sessionid', None)
        print self.sessionid, 2222222222222222222222222222
        if not self.sessionid:
            # set cookie
            h = hashlib.md5()
            datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            h.update(datetime_str)
            self.response.set_cookie('sessionid', h.hexdigest())
            self.sessionid = h.hexdigest()
        if not r.exists('sessionid_:%s' % self.sessionid):
            # set session
            r.hmset('sessionid_%s' % self.sessionid, self.uid)            # 设置sessionid对应的真实数据
        return True
