from django.contrib import admin
from app01 import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
# Register your models here.


#  配置会议室信息表
class RoomConfig(admin.ModelAdmin):
    list_display = ('caption','num')
    list_filter=('num',)
    search_fields = ('caption','num')


# 配置预订信息表
class BookConfig(admin.ModelAdmin):
    list_display = ('user','room','date','time_id')
    list_filter = ('user','room','date','time_id')
    search_fields = ('user','room','date','time_id')


# 配置用户管理表
class UserProfileAdmin(UserAdmin):
    list_display = ('username','last_login','is_superuser','is_staff','is_active','date_joined')
    list_filter = ('last_login', 'is_staff', 'date_joined', 'is_active')
    search_fields = ('username',)
    fieldsets = (
        (None,{'fields':('username','password','first_name','last_name','email')}),

        (gettext_lazy('用户信息'),{'fields':('username','email','tel','avatar')}),

        (gettext_lazy('用户权限'), {'fields': ('is_superuser','is_staff','is_active',
                                                  'groups', 'user_permissions')}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(models.Room,RoomConfig)
admin.site.register(models.UserInfo,UserProfileAdmin)
admin.site.register(models.Book,BookConfig)
