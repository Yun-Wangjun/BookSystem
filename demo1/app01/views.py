from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from geetest import GeetestLib
from django.contrib.auth.decorators import login_required
from app01 import models
from app01 import forms
import json
import datetime
# Create your views here.


def acc_login(request):
    if request.method == "POST":
        print(request.POST)
        res = {"status": 0, "msg": ""}
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print("####################", result)
        if result:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                res["msg"] = "/index/"
            else:
                res["status"] =1
                res["msg"] = "认证失败,请检查用户名及密码是否正确"
        else:
            res["status"] = 1
            res["msg"] = "验证码错误"
        print("**************", res)
        return JsonResponse(res)
    return render(request, 'login.html')


@login_required(login_url="/login/")
def index(request):

    date = datetime.datetime.now().date()
    # 如果没有指定日期，默认使用当天日期
    book_date = request.GET.get("book_date",date)
    print('日期：', request.GET.get("book_date"))
    print("book_date",book_date)
    # 获取会议室时间段列表
    time_choice = models.Book.time_choice
    print(time_choice)
    # 获取会议室列表
    room_list = models.Room.objects.all()
    # 获取会议室预订信息
    book_list = models.Book.objects.filter(date=book_date)
    htmls=''
    for room in room_list:
        htmls += '<tr><td>{}({})</td>'.format(room.caption,room.num)
        for time in time_choice:
            # 判断该单元格是否被预订
            flag = False
            for book in book_list:
                if book.room.pk == room.pk and book.time_id == time[0]:
                    # 单元格被预定
                    flag = True
                    break
            if flag:
                # 判断当前登录人与预订会议室的人是否一致，一致使用info样式
                if request.user.username == book.user.username:
                    htmls += '<td class="info item"  room_id={} time_id={}>{}</td>'.format(room.pk, time[0],book.user.username)
                else:
                    htmls += '<td class="success item"  room_id={} time_id={}>{}</td>'.format(room.pk, time[0],
                                                                                         book.user.username)

            else:
                htmls += '<td class="item"  room_id={} time_id={}></td>'.format(room.pk,time[0])
        htmls += "</tr>"
    return render(request,'index.html',{"time_choice":time_choice,"htmls":htmls,})


@login_required(login_url="/login/")
def book(request):
    if request.method == "POST":
        choose_date = request.POST.get("choose_date")
        print("choose_date:", choose_date)
        # 获取会议室时间段列表
        time_choice = models.Book.time_choice
        try:
            # 向数据库修改会议室预订记录
            post_data = json.loads(request.POST.get("post_data"))
            if not post_data["ADD"] and not post_data["DEL"]:
                res = {"status":2, "msg":""}
                return HttpResponse(json.dumps(res))
            user = request.user
            print(type(post_data), post_data)
            # 添加新的预订信息
            book_list = []
            for room_id, time_id_list in post_data["ADD"].items():
                for time_id in time_id_list:
                    book_obj = models.Book(user=user, room_id=room_id, time_id=time_id, date=choose_date)
                    book_list.append(book_obj)
            models.Book.objects.bulk_create(book_list)

            # 删除旧的预订信息
            from django.db.models import Q
            remove_book = Q()
            for room_id,time_id_list in post_data["DEL"].items():
                temp = Q()
                for time_id in time_id_list:
                    temp.children.append(("room_id", room_id))
                    temp.children.append(("time_id", time_id))
                    temp.children.append(("user_id", request.user.pk))
                    temp.children.append(("date", choose_date))
                    remove_book.add(temp, "OR")
            if remove_book:
                models.Book.objects.filter(remove_book).delete()
                for time in post_data["DEL"][room_id]:
                    models.Book.objects.filter(user=user, room_id=room_id, time_id=time, date=choose_date).delete()
            res = {"status": 1, "msg": ''}
        except Exception as e:
            res = {"status": 0, "msg": str(e)}
        return HttpResponse(json.dumps(res))


def acc_logout(request):
    logout(request)
    return redirect("/login/")


def reg(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print('request.POST'.center(80, '#'))
        print(request.POST)
        print('request.POST'.center(80, '#'))
        avatar_img = request.FILES.get("avatar")
        print(avatar_img)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            print(form_obj.cleaned_data)
            try:
                models.UserInfo.objects.create_user(**form_obj.cleaned_data,avatar=avatar_img)
            except Exception as e:
                print(e)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
            # 生成一个form对象
    form_obj = forms.RegForm()
    print(form_obj.fields)
    return render(request,'reg.html',{"form_obj": form_obj})


def home(request):
    # 获取当前用户的预订信息
    date = datetime.datetime.now().date()
    print(date,type(date))
    user = request.user
    if user.is_authenticated():
        book_ret = models.Book.objects.filter(user=user, date__gte=date).count()
    else:
        book_ret = None
    print(book_ret)
    return render(request,'home.html',{"book_ret":book_ret})
# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


@login_required(login_url="/login/")
def change_password(request):
    user = request.user
    username = user.username
    if request.method == "POST":
        msg = ''
        form_obj = forms.ChangePwdForm(request.POST)
        if form_obj.is_valid():
            old_password = form_obj.cleaned_data['password']
            new_password = form_obj.cleaned_data["new_password"]
            user_obj = models.UserInfo.objects.filter(username=username).first()
            ret = user_obj.check_password(old_password)

            print(old_password)
            print(form_obj.cleaned_data)
            if not ret:
                form_obj.add_error("password", "旧密码错误")
            else:
                #  旧密码正确
                user_obj.set_password(new_password)
                user_obj.save()
                msg = "/login/"
        return render(request, 'change_password.html', {"username":username,"msg":msg,"form_obj":form_obj})
        print(request.POST)
    form_obj = forms.ChangePwdForm()
    return render(request,'change_password.html',{"username":username,"form_obj":form_obj})


def test(request):
    return render(request,'轮播图.html')


def about(request):
    return render(request,'about.html')
