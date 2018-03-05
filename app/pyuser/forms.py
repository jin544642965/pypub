# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
import re


def check_len(pwd):
    """ 校验注册密码的位数"""
    if len(pwd) > 20:
        return False
    elif len(pwd) < 6:
        return False
    return pwd


def check_contain_lett(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def check_contain_num(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def check_all(pwd):
    lenok = check_len(pwd)
    lettok = check_contain_lett(pwd)
    numok = check_contain_num(pwd)
    return (lenok and lettok and numok)


def check_pwd(pwd):
    if check_all(pwd):
        return True
    else:
        raise ValidationError('密码必须由数字和字母组成,并且长度在6-20位之间')


class UserForm(forms.Form):
    username = forms.EmailField(label='电子邮箱:', widget=forms.TextInput(
            attrs={'size': '38', 'class': 'form-control', 'placeholder': "输入电子邮箱"}))
    name = forms.CharField(label='名字', max_length=10,
                           widget=forms.TextInput(
                                   attrs={'size': '38', 'class': 'form-control', 'placeholder': "输入真实名字"}))
    password = forms.CharField(validators=[check_pwd, ], label='密码',
                               widget=forms.PasswordInput(
                                       attrs={'size': '38', 'class': 'form-control',
                                              'placeholder': "输入6-20位字母和数字组成的密码"}))


class LoginForm(forms.Form):
    username = forms.EmailField(label='电子邮箱:', widget=forms.TextInput(attrs={'size': '38', 'class': 'form-control'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'size': '38', 'class': 'form-control'}))


class ResetPwdForm(forms.Form):
    password = forms.CharField(validators=[check_pwd, ], label='密码',
                               widget=forms.PasswordInput(
                                       attrs={'size': '38', 'class': 'form-control',
                                              'placeholder': "输入6-20位字母和数字组成的密码"}))

class ForgetPwdForm(forms.Form):
    username = forms.EmailField(label='电子邮箱:', widget=forms.TextInput(attrs={'size': '38', 'class': 'form-control'}))

