#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render, redirect, HttpResponse
from . import forms
from . import models

# Create your views here.


def checklogin(main_func):
    def wrapper(request):
        if request.session.get('is_login', None):
            print 'login'
            return main_func(request)
        else:
            print 'not login'
            return redirect('/drink/login')
    return wrapper


def register(request):
    registerform = forms.UserForm()
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["username"]
            pwd = form.cleaned_data['password']
            if models.user.objects.filter(username=user):
                return render(request, 'drink/register.html', {'form': registerform, 'status': '用户已注册！'})
            else:
                models.user.objects.create(username=user, password=pwd)
                redirect('/drink/login')
        else:
            return render(request, 'drink/register.html', {'form': registerform, 'status': '请输入正确的格式！',} )

    return render(request, 'drink/register.html', {'form': registerform, })


def login(request):
    loginform = forms.UserForm()
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            checkuser = models.user.objects.filter(username=user)
            if checkuser:
                checkpwd = models.user.objects.filter(username=user).filter(password=pwd)
                if checkpwd:
                    request.session['is_login'] = {'user': user, }
                    return redirect('/drink/index/')
                else:
                    return render(request, 'drink/login.html', {'form':loginform, 'status': '密码错误！'})
            else:
                return render(request, 'drink/login.html', {'form': loginform, 'status': '用户名不存在！'})
        else:
            return render(request, 'drink/login.html', {'form': loginform, 'status': '请输入正确的格式！'})
    return render(request, 'drink/login.html', {'form': loginform })


def index(request):
    user_dict = request.session.get('is_login', None)
    if user_dict:
        return render(request, 'drink/index.html', {'username': user_dict['user']})
    else:
        return redirect('/drink/login')


def logout(request):
    del request.session['is_login']
    return redirect('/drink/login/')

'''
def before_test(request):
    print 'before'

def after_test(request):
    print 'after'

def Filter(before_func,after_func):
    def outer(main_func):
        def warpper(request, *args, **kwargs):
            before_result = before_func(request, *args, **kwargs)
            if(before_result != None):
                return before_result
            main_result = main_func(request, *args, **kwargs)
            if(main_result != None):
                return main_result
            after_result = after_func(request, *args, **kwargs)
            if (after_result != None):
                return after_result
        return warpper
    return outer


@Filter(before_test, after_test)
def test(request):
    return HttpResponse('success')
'''