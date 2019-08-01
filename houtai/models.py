from django.db import models
class User(models.Model):
    username=models.CharField(max_length=16)
    password=models.CharField(max_length=32)
    email = models.EmailField(unique=True)
# Create your models here.
# ## 注册 申请 通过 还款
# class Apply_all(models.Model):
#     date=models.CharField(max_length=16)
#     register=models.IntegerField(max_length=32)
#     apply = models.IntegerField(max_length=32)
#     past = models.IntegerField(max_length=32)
#     order = models.IntegerField(max_length=32)
#
# # 迁徙表
# class Repay_all(models.Model):
#     num=models.CharField(max_length=16)
#     T0=models.IntegerField(max_length=32)
#     T1 = models.IntegerField(max_length=32)
#     T2 = models.IntegerField(max_length=32)
#     T3 = models.IntegerField(max_length=32)
#     T4 = models.IntegerField(max_length=32)
#     T5 = models.IntegerField(max_length=32)
#     T6 = models.IntegerField(max_length=32)
#     T7 = models.IntegerField(max_length=32)
#     T0rate = models.FloatField(max_length=32)
#     T1rate = models.FloatField(max_length=32)
#     T2rate = models.FloatField(max_length=32)
#     T3rate = models.FloatField(max_length=32)
#     T4rate = models.FloatField(max_length=32)
#     T5rate = models.FloatField(max_length=32)
#     T6rate = models.FloatField(max_length=32)
#     T7rate = models.FloatField(max_length=32)


