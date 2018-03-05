# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import *
from django.core.mail import send_mail
from classes import token_confirm, r
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from app.proj.views import ServerError
from app.pyuser.models import UserProfile

# Create your views here.


def auth(func):
    """装饰器 ，登录认证函数"""
    def inner(request, *args, **kwargs):
        v = request.session.get('username')    # 获取session中的username的值 如果为空
        if not v:
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)
    return inner


@auth
def logout_view(request):
    logout(request)                    # 删除cookie中的session
    return  HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        add_role = request.POST.get('add_role')
        if uf.is_valid():
            username = uf.cleaned_data['username']
            name = uf.cleaned_data['name']
            password = uf.cleaned_data['password']
            if User.objects.filter(username=username):
                error = "邮箱已存在，请重新输入"
                return render_to_response('pyuser/register.html', {'uf': uf, 'error': error})
            User.objects.create_user(username=username, last_name=name, password=password, is_active=False)
            user_id_list = User.objects.filter(username=username).values('id')  #查询用户名的id,得到的是一个querySet类型
            id = user_id_list[0].get('id')        #先取出列表中的0号元素，然后从字典中取id字段的值
            UserProfile.objects.create(
                user_role = add_role,
                user_id  = id,
            )
            # create_user方法会对密码进行加密
            token = token_confirm.generate_validate_token(username)  # 生成令牌环
            message = "\n".join([
                u'{0},欢迎使用pypub'.format(username),
                u'请访问该链接,有效期1小时，完成用户验证：',
                '/'.join(["http://58.63.39.168:8001", 'pyuser/active_user', token])
            ])
            send_mail(u'注册用户验证信息', message, 'mike@yy.com', [username])
            return render_to_response('pyuser/activate.html', {'username': username})
        else:
            error = uf.errors
            return render_to_response('pyuser/register.html', {'uf': uf, 'error': error})
    else:
        uf = UserForm()
    return render_to_response('pyuser/register.html', {'uf': uf})


@auth
def reset_password(request):
    username = request.session.get('username')
    if request.method == 'POST':
        rpf = ResetPwdForm(request.POST)
        if rpf.is_valid():
            password = make_password(rpf.cleaned_data['password'], 'pbkdf2_sha256')
            User.objects.filter(username=username).update(password=password)
            sessionid = r.get('user_%s' % username)
            r.hset('sessionid_%s' % sessionid, 'password', password)                    #更新的密码写入redis
            return HttpResponseRedirect('/index/')
        else:
            error = rpf.errors
            return render_to_response("pyuser/reset_password.html",
                                      {'error': error, 'rpf': rpf, 'username': username})
    else:
        rpf = ResetPwdForm()
    return render_to_response('pyuser/reset_password.html', {'rpf': rpf, 'username': username})


def active_user(request, token):
    try:
        username = token_confirm.comfirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已过期')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(u'对不起,您所验证的用户不存在，请重新注册')
    user.is_active = True
    user.save()
    confirm = "验证成功，请进行登录!"
    lf =LoginForm()
    return render_to_response('login.html', {'lf': lf, 'confirm': confirm})


def submit_email(request):
    if request.method == 'POST':
        ff = ForgetPwdForm(request.POST)
        if ff.is_valid():
            username = ff.cleaned_data['username']
            token = token_confirm.generate_validate_token(username)  # 生成令牌环
            message = "\n".join([
                u'{0},欢迎使用pypub'.format(username),
                u'请访问该链接,有效期1小时，完成用户验证：',
                '/'.join(["http://58.63.39.168:8001", 'pyuser/change_pwd', token])
            ])
            send_mail(u'pypub修改密码', message, 'mike@yy.com', [username])
            return HttpResponseRedirect('/')
        else:
            login_err = "邮箱格式不正确"
            return render_to_response('login.html', {'login_err': login_err})
    else:
        ff = ForgetPwdForm()
    return render_to_response('pyuser/sub_email.html')


# 跳转到修改密码页面
def change_pwd(request, token):
    try:
        username = token_confirm.comfirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已过期')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(u'对不起,您所验证的用户不存在，请重新注册')
    rpf = ResetPwdForm()
    return render_to_response('pyuser/change_pwd.html', {'rpf': rpf, 'token': token})  # 传递token值给change_pwd.html页面


# 处理改变密码
def change_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')  # 获取页面的token
        try:
            username = token_confirm.comfirm_validate_token(token)  # 验证token,解密token的值得到用户名
        except:
            return HttpResponse(u'对不起，验证链接已过期')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(u'对不起,您所验证的用户不存在，请重新注册')
        rpf = ResetPwdForm(request.POST)
        if rpf.is_valid():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            password = user.password
            sessionid = r.get('user_%s' % username)
            r.hset('sessionid_%s' % sessionid, 'password', password)
            return HttpResponseRedirect('/')
        else:
            error = rpf.errors
            return render_to_response("pyuser/change_pwd.html", {'error': error, 'rpf': rpf})
    else:
        return HttpResponseRedirect('/')  # 防止用户直接通过change_password进入修改密码

def user_list(request):
    username = request.session.get('username')
    user_list = User.objects.all()
    return render_to_response('pyuser/user_list.html', {'user_list':user_list, 'username': username})

def user_add(request):
    username = request.session.get('username')
    if request.method == 'POST':
        add_user = request.POST.get('add_user')
        add_password = request.POST.get('add_password')
        add_name = request.POST.get('add_name')
        add_role = request.POST.get('add_role')
        try:
            if '' in [add_user, add_password, add_name, add_role]:
                error = u'内容不能为空'
                raise ServerError
        except ServerError:
            pass
        else:
            User.objects.create_user(
                username = add_user,
                password = add_password,
                last_name = add_name,
            )
            user_id_list = User.objects.filter(username=add_user).values('id')  #查询用户名的id,得到的是一个querySet类型
            id = user_id_list[0].get('id')        #先取出列表中的0号元素，然后从字典中取id字段的值
            UserProfile.objects.create(
                user_role = add_role,
                user_id  = id,
            )
            return HttpResponseRedirect('/pyuser/user_list/')
    return render_to_response('pyuser/user_add.html',{ 'username': username, })

def user_del(request):
    username = request.session.get('username')
    id = request.GET.get('id')
    u = User.objects.get(id=id)
    u.delete()
    user_list = User.objects.all()
    return render_to_response('pyuser/user_list.html', {'user_list':user_list, 'username': username})

def user_edit(request):
    username = request.session.get('username')
    id = request.GET.get('id')
    user_list = UserForm.objects.filter(id=id)
    # if request.method == 'POST':
    #     u = User.objects.filter(id=id).update(last_name=name)
    return render_to_response('pyuser/edit_user.html')

