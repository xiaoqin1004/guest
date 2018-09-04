from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# 首页
def index(request):
    return render(request, 'index.html')


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    else:
        return render(request, "index.html")


# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(event_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)             # 获取第page页的数据
    except PageNotAnInteger:                        # 如果没有第page页，则抛出PageNotAnInteger异常
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:  # 如果超出页数范围，则抛出EmptyPage异常
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'event_manage.html', {'user': username, 'events': contacts})


# 发布会搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)            # 把查询出来的嘉宾列表guest_list放到Paginator类中，划分每页2条数据
    page = request.GET.get('page')                  # 通过GET请求获取当前要显示第几页的数据
    try:
        contacts = paginator.page(page)             # 获取第page页的数据
    except PageNotAnInteger:                        # 如果没有第page页，则抛出PageNotAnInteger异常
        # 如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:                               # 如果超出页数范围，则抛出EmptyPage异常
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username, 'guests': contacts})


# 添加签到
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)

    # 查询手机号在Guest表中是否存在，不存在则提示用户phone error
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error'})

    # 通过手机号和发布会ID两个条件来查询Guest表，如果结果为空，则提示用户event id or phone error
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error'})

    # 通过手机号和发布会ID两个条件来查询Guest表，如果结果不为空，
    # 则判断签到状态是否为True，为True则提示用户user has sign in.
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in.'})
    else:
        # 签到状态为False，提示用户sign in success!
        Guest.objects.filter(phone=phone, event_id=eid).update(sign=1)
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result})


# 退出登录
@login_required
def logout(request):
    auth.logout(request)            # 退出登录
    response = HttpResponseRedirect('/index/')
    return response


