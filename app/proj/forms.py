# -*- coding: utf-8 -*-
from django import forms


# class ProjectForm(forms.Form):
#     project_name = forms.CharField(widget=forms.Tex tInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "请输入项目名称"}), required=True)
#     # env = forms.CharField(widget=forms.TextInput(
#     #         attrs={'size': '20', 'class': 'form-control'}), required=True)
#     env_select = (
#         (1, '线上环境'),
#         (2, '测试环境'),
#         (3, '预发布环境'),
#     )
#     env = forms.IntegerField(required=True, widget=forms.Select(choices=env_select, attrs={'class': 'form-control'}))
#     # submit_method = forms.CharField(widget=forms.TextInput(
#     #         attrs={'size': '20', 'class': 'form-control'}), required=True)
#     repo_address = forms.CharField(max_length=100, widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "git@github.com:pypub/pupub.git"}), required=True)
#     username = forms.CharField(widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "用户名"}), max_length=20)
#     password = forms.CharField(widget=forms.PasswordInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "密码"}), max_length=20)
#     repertory = forms.CharField(max_length=100, widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "/data/www/deploy"}), required=True)
#     # repertory = forms.CharField(widget=forms.URLField())
#     excludes_file = forms.CharField(widget=forms.Textarea(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': ".git \n.svn"}))
#     www_user = forms.CharField(widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "www"}), required=True)
#     web_path = forms.CharField(widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "/data/wwwroot/dttx.com"}), required=True)
#     deploy_releases = forms.CharField(widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "/data/release"}), required=True)
#     releases_num = forms.IntegerField(widget=forms.TextInput(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "10"}), required=True)
#     servers = forms.CharField(widget=forms.Textarea(
#             attrs={'size': '20', 'class': 'form-control', 'placeholder': "10.0.0.100 \n10.0.0.101:8888"}), required=True)
#     # online_method = forms.ChoiceField(choices=(('1', 'branch'), ('2', 'tag'), ('3', '无trunk/无branches')),
#     #         widget=forms.RadioSelect(attrs={'class': 'radio', 'checked': 'checked'}), required=True)
#     radio_display = [('display:online', 'display:online', 'display:none')]


