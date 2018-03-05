# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from app.pyuser.forms import *
from django.conf.urls import handler404
from app.pyuser.classes import UserSystem, r
import datetime
from app.pyuser.views import auth
from django.contrib.auth.hashers import check_password

# Create your views here.


def login_sys(request):
    """ 登录界面 """
    login_err =''
    username = request.session.get('username')
    if username:
        return HttpResponseRedirect('/index/')
    if request.method == 'GET':
        lf = LoginForm()
        return render_to_response('login.html', {'lf': lf})

    if request.method == "POST":
        lf = LoginForm(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data.get('password')
            if r.exists('user_%s' % username):
                sessionid = r.get('user_%s' % username)
                if r.exists('sessionid_%s' % sessionid):
                    username_, password_, = r.hmget('sessionid_%s' % sessionid, 'username', 'password')
                    if username_ == username and check_password(password, password_):   #check_password方法用于校验pbkdf2_sha256的密码是否正确
                        r.hincrby('sessionid_%s' % sessionid, 'login_count', 1)  # 登录次数累计
                        r.hset('sessionid_%s' % sessionid, 'last_login_time', datetime.datetime.now())   #添加最近登录
                        #set Cookies
                        request.session['username'] = username
                        res = HttpResponseRedirect('/index/')
                        return res

                    else:
                         login_err = "邮箱或密码错误"
                         return render_to_response('login.html', {'lf': lf, 'login_err': login_err})

            else:        #如果redis中不存在，检验数据库中是否有这个用户
                user = authenticate(username=username, password=password)
                if user is not None:           # 检查数据库中是否有这个用户
                    if user.is_active:
                        login(request, user)                 #记录session，向session中添加SESSION_KEY，便于用户进行跟踪
                        res = HttpResponseRedirect('/index/')
                        uid = {
                            'username': username,
                            'password': user.password,
                            'is_active': 1,
                            'last_login_time': datetime.datetime.now()
                        }
                        user_sys = UserSystem(request, res, uid)
                        if user_sys.set_cookie_and_session():
                            r.set('user_%s' % username, user_sys.sessionid)
                            request.session['username'] = username
                            return res
                    else:
                        login_err = "账号未激活，请先登录邮箱激活账号!"
                        return render_to_response('login.html', {'lf': lf, 'login_err': login_err})
                else:
                    login_err = "邮箱或密码错误"
        else:
            login_err = "邮箱或密码错误"
            return render_to_response('login.html', {'lf': lf, 'login_err': login_err})
    return render_to_response('login.html', {'lf': lf, 'login_err': login_err})


@auth                            # @表示装饰器，相当于执行了index =auth（index）
def index(request):
    username = request.session.get('username')
    return render_to_response('index.html', {'username': username})


def page_not_found(request):
    return render_to_response("404.html")


handler404 = page_not_found
