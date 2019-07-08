"""
BBS用到的form组件
"""
from django import forms
from django.core.exceptions import ValidationError
from app01 import models


# 定义注册类
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        label="用户名",
        error_messages={
            "max_length": "用户名最大32位",
            "required": "用户名不能为空",
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"}),
        )
    email = forms.EmailField(
        label="邮箱",

        widget=forms.widgets.EmailInput(
            attrs={"class": "form-control"},
        ),
        error_messages={
            "invalid": "邮箱格式错误",
            "required": "邮箱不能为空",
        }
    )
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"}
        ),
        error_messages={
            "min_length": "密码至少6位",
            "required": "密码不能为空",
        }
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"}
        ),
        error_messages={
            "min_length": "密码至少6位",
            "required": "确认密码不能为空",
        }
    )

    # 重写username字段的局部钩子函数，对username字段检验
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            # 用户名已经存在
            self.add_error("username", ValidationError("用户名已经存在"))
        else:
            return username

    # 重写全局的钩子函数,对确认密码做校验
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("两次密码不一致"))


# 定义修改密码类
class ChangePwdForm(forms.Form):
    password = forms.CharField(
        min_length=6,
        label="旧密码",

        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control","placeholder":"请输入旧密码"}
        ),
        error_messages={
            "min_length": "密码至少6位",
            "required": "密码不能为空",
        }
    )
    new_password = forms.CharField(
        min_length=6,
        label="新密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control","placeholder":"请输入新密码"}
        ),
        error_messages={
            "min_length": "密码至少6位",
            "required": "新密码不能为空",
        }
    )

    confirm_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control","placeholder":"请输入确认密码"}
        ),
        error_messages={
            "min_length": "密码至少6位",
            "required": "确认密码不能为空",
        }
    )

    # 重写全局的钩子函数,对确认密码做校验
    def clean(self):
        password = self.cleaned_data.get("new_password")
        re_password = self.cleaned_data.get("confirm_password")
        if re_password and re_password != password:
            self.add_error("confirm_password", ValidationError("两次密码不一致"))
