# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
# from app.pyuser.views import auth
from models import ProjectConf
from django.http import HttpResponseRedirect

def auth(func):
    """装饰器 ，登录认证函数"""
    def inner(request, *args, **kwargs):
        v = request.session.get('username')    # 获取session中的username的值 如果为空
        if not v:
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)
    return inner

class ServerError(Exception):
   pass


@auth
def proj_conf(request):
    username = request.session.get('username')  # 获取cookie的变量username的值
    project_list = ProjectConf.objects.order_by("id").all()
    return render_to_response('proj/conf.html', {'username': username, 'project_list': project_list})



@auth
def proj_add(request):
    username = request.session.get('username')
    submit_method = ["branch", "tag"]

    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        env = request.POST.get('env')
        repo_address = request.POST.get('repo_address')
        p_username = request.POST.get('p_username')
        p_password = request.POST.get('p_password')
        repertory = request.POST.get('repertory')
        excludes_file = request.POST.get('excludes_file')
        www_user = request.POST.get('www_user')
        web_path = request.POST.get('web_path')
        deploy_releases = request.POST.get('deploy_releases')
        releases_num = request.POST.get('releases_num')
        servers = request.POST.get( 'servers')
        submit_method = request.POST.get("submit_method")

        try:
            if '' in [project_name, repo_address, env, repertory, www_user, web_path, deploy_releases, releases_num, servers]:
                error = u'内容不能为空'
                raise ServerError
        except ServerError:
            pass
        else:
            ProjectConf.objects.create(project_name=project_name,
                                       env=env,
                                       repo_address=repo_address,
                                       p_username=p_username,
                                       p_password=p_password,
                                       repertory=repertory,
                                       excludes_file=excludes_file,
                                       www_user=www_user,
                                       web_path=web_path,
                                       deploy_releases=deploy_releases,
                                       releases_num=releases_num,
                                       servers=servers,
                                       submit_method=submit_method
                                       )
            return HttpResponseRedirect('/proj/conf/')
    return render_to_response('proj/add.html', {'username': username, 'submit_method': submit_method})

@auth
def proj_edit(request):
    username = request.session.get('username')
    id=request.GET.get('id')
    submit_method = ["branch", "tag"]
    project_list = ProjectConf.objects.filter(id=id)
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        env = request.POST.get('env')
        repo_address = request.POST.get('repo_address')
        p_username = request.POST.get('p_username')
        p_password = request.POST.get('p_password')
        repertory = request.POST.get('repertory')
        excludes_file = request.POST.get('excludes_file')
        www_user = request.POST.get('www_user')
        web_path = request.POST.get('web_path')
        deploy_releases = request.POST.get('deploy_releases')
        releases_num = request.POST.get('releases_num')
        servers = request.POST.get( 'servers')
        submit_method = request.POST.get("submit_method")
        try:
            if '' in [project_name, repo_address, env, repertory, www_user, web_path, deploy_releases, releases_num, servers]:
                error = u'内容不能为空'
                raise ServerError
        except ServerError:
            pass
        else:
            ProjectConf.objects.filter(id=id).update(
                   project_name=project_name,
                   env=env,
                   repo_address=repo_address,
                   p_username=p_username,
                   p_password=p_password,
                   repertory=repertory,
                   excludes_file=excludes_file,
                   www_user=www_user,
                   web_path=web_path,
                   deploy_releases=deploy_releases,
                   releases_num=releases_num,
                   servers=servers,
                   submit_method=submit_method
                   )
            return HttpResponseRedirect('/proj/conf/')
    return render_to_response('proj/edit.html', {'username': username, 'project_list': project_list, 'submit_method': submit_method })

def proj_del(request):
    id = request.GET.get('id')
    p = ProjectConf.objects.get(id=id)
    p.delete()
    return HttpResponseRedirect('/proj/conf/')

def proj_copy(request):
    username = request.session.get('username')
    id=request.GET.get('id')
    pl = ProjectConf.objects.get(id=id)

    ProjectConf.objects.create(project_name=pl.project_name,
                           env=pl.env,
                           repo_address=pl.repo_address,
                           p_username=pl.p_username,
                           p_password=pl.p_password,
                           repertory=pl.repertory,
                           excludes_file=pl.excludes_file,
                           www_user=pl.www_user,
                           web_path=pl.web_path,
                           deploy_releases=pl.deploy_releases,
                           releases_num=pl.releases_num,
                           servers=pl.servers,
                           submit_method=pl.submit_method
                           )
    return HttpResponseRedirect('/proj/conf/')

def proj_member(request):
    username = request.session.get('username')
    id = request.GET.get('id')

    return render_to_response('proj/member.html',{ 'id' : id })