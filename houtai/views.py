from django.shortcuts import render,redirect
from django import forms
from functools import wraps
from .models import User
from .forms import  DateRangeForm,DateRangeForm1
from django.utils import timezone
from django.views.decorators import csrf
#from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
import pandas as pd
import numpy as np
import json
import pymysql





def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login')
    return inner

def login(request):
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index")
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username,password=password)
        if user:
            #登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
            request.session['is_login']='1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
            request.session['user_id']=user[0].id
            return redirect('/index')
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request,'A_login.html')


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index")
    print(request.method)
    if request.method == "POST":
        register_form = User(request.POST)
        message = "请检查填写的内容！"
        #print(message)
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        invitation = request.POST.get('invitation')
        if invitation != 'cjfk':
            message = "邀请码不正确！"
            return render(request, 'A_register.html', locals())
        if password1 != password:  # 判断两次密码是否相同
            message = "两次输入的密码不同！"
            #print(message)
            return render(request, 'A_register.html', locals())
        else:
            same_name_user = User.objects.filter(username=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名！'
                #print(message)
                return render(request, 'A_register.html', locals())
            same_email_user = User.objects.filter(email=email)
            if same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                #print(message)
                return render(request, 'A_register.html', locals())

            # 当一切都OK的情况下，创建新用户

            new_user = User.objects.create()
            new_user.username = username
            new_user.password = password
            new_user.email = email
            new_user.save()
            print('ok')
            return redirect('/login')  # 自动跳转到登录页面
    register_form = User()
    return render(request, 'A_register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index')
    request.session.flush()

    return redirect('/index')


@check_login
def index1(request):
    user_id1=request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息
    userobj=User.objects.filter(id=user_id1).values()
    return render(request, 'A_index_text_0.html')

def getgame(request):
    #return HttpResponseRedirect('index_0.html')
    return render(request, 'A_index_game.html')
## 每日报表
@check_login
def table(request):
    user_id1 = request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息
    userobj = User.objects.filter(id=user_id1).values()

    if request.method == 'POST':  # 当提交表单时
        form = DateRangeForm(request.POST)
        if form.is_valid():  # 如果提交的数据合法
            start_date = form.cleaned_data['start_date']
            start_date = start_date.strftime("%Y-%m-%d")
            end_date = form.cleaned_data['end_date']
            end_date = end_date.strftime("%Y-%m-%d")
            print(start_date,end_date)
            if start_date >end_date:
                message = '结束时间小于起始时间'
                return render(request, 'A_tables.html',  locals())
    else:
        form = DateRangeForm()
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')

    return render(request, 'A_tables.html',
                  {'user': userobj[0]['username'], 'form': form})

## 迁徙表
@check_login
def table1(request):
    user_id1 = request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息
    userobj = User.objects.filter(id=user_id1).values()

    if request.method == 'POST':  # 当提交表单时
        form = DateRangeForm(request.POST)
        if form.is_valid():  # 如果提交的数据合法
            start_date = form.cleaned_data['start_date']
            start_date = start_date.strftime("%Y-%m-%d")
            end_date = form.cleaned_data['end_date']
            end_date = end_date.strftime("%Y-%m-%d")
            print(start_date,end_date)
            if start_date >end_date:
                message = '结束时间小于起始时间'
                return render(request, 'A_tables_1.html',  locals())
    else:  # 当正常访问时
        form = DateRangeForm()
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y-%m-%d')

    return render(request, 'A_tables_1.html', {'user':userobj[0]['username'],'form': form })

##命中情况
@check_login
def table2(request):
    celue = ['测试']
    user_id1 = request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息
    userobj = User.objects.filter(id=user_id1).values()

    if request.method == 'POST':  # 当提交表单时
        name = request.POST.get('sel_value')
        reservation = request.POST.get('reservation')
        print(reservation)
        rule_code = name.split(' ')[0]
        start_date = reservation.replace(' ','').split('-')[0].replace('/','-')
        start_date = start_date.split('-')[2]+'-'+start_date.split('-')[0]+'-'+start_date.split('-')[1]
        end_date = reservation.replace(' ', '').split('-')[1].replace('/', '-')
        end_date = end_date.split('-')[2] + '-' + end_date.split('-')[0] + '-' + end_date.split('-')[1]
        print(rule_code,start_date,end_date)
    else:  # 当正常访问时
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() + datetime.timedelta(days=-3)).strftime('%Y-%m-%d')
        rule_code ='测试'
        reservation = ""
    return render(request, 'A_tables_2.html', {'user': userobj[0]['username'],'reservation':reservation})
