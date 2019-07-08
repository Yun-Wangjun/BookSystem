from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserInfo(AbstractUser):
    tel = models.CharField(max_length=32,verbose_name="电话")
    avatar = models.FileField(upload_to="avatars/", default="avatars/timg.jpg", verbose_name="头像")


class Room(models.Model):
    """会议室表"""
    caption = models.CharField(max_length=32,verbose_name="会议室名称")
    num = models.IntegerField(verbose_name="容纳人数")  # 容纳人数

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "会议室信息"
        verbose_name_plural = verbose_name


class Book(models.Model):
    """会议室预订"""
    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    room = models.ForeignKey(to="Room",on_delete=models.CASCADE)
    date = models.DateField()
    time_choice = (
        (1, "8:00"),
        (2, "9:00"),
        (3, "10:00"),
        (4, "11:00"),
        (5, "12:00"),
        (6, "13:00"),
        (7, "14:00"),
        (8, "15:00"),
        (9, "16:00"),
        (10, "17:00"),
        (11, "18:00"),
        (12, "19:00"),
        (13, "20:00"),
        (14, "21:00"),
        (15, "22:00"),
        (16, "23:00"),
    )

    time_id = models.IntegerField(choices=time_choice)

    def __str__(self):
        return str(self.user)+"预定了"+str(self.room)

    class Meta:
        verbose_name = "预定信息"
        verbose_name_plural = verbose_name
        unique_together = (
            ("room","date","time_id"),  # 这三个字段联合唯一，防止重复预订
        )
