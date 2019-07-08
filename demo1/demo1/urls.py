"""demo1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 用户登录
    url(r'^login/',views.acc_login),
    # 展示预订信息
    url(r'^index/',views.index),
    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', views.get_geetest),
    # media相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 处理预订请求
    url(r'^book/',views.book),
    # 首页
    url(r'^home/',views.home),
    # 注销
    url(r'^logout/',views.acc_logout),
    # 用户注册
    url(r'^reg/',views.reg),
    # 临时测试
    url(r'^test/',views.test),
    # 修改密码
    url(r'^change_password/',views.change_password),

    # about
    url(r'^about/',views.about),


]
