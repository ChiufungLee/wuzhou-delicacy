from django.db import models
from datetime import datetime
# Create your models here.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class User(models.Model):
	"""用户信息表"""
	sex = (
        ('male', "男"),
        ('female', "女"),
    )
	username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
	password = models.CharField(max_length=256, verbose_name="密码")
	gender = models.CharField(max_length=32, choices=sex, default="男")
	birthday = models.DateField(verbose_name="生日")
	email = models.EmailField(verbose_name="邮箱")
	mobile = models.CharField(max_length=11, verbose_name="手机号")
	address = models.CharField(max_length=255, verbose_name="地址")
	userType = models.CharField(max_length=1, default='0', verbose_name="用户类型")
	has_confirmed = models.BooleanField(default=False, verbose_name="激活状态")
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name="用户头像")


	class Meta:
		db_table = "userinfo"

	def __str__(self):
		return self.username

@receiver(pre_delete, sender=User)	#sender=你要修改图片字段所在的类
def avatar_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.avatar.delete(False)

class ConfirmString(models.Model):
	sendType = (
		("register", "注册"), 
		("forget", "找回密码"),
	)
	code = models.CharField(max_length=256)
	user = models.OneToOneField('User', on_delete=models.CASCADE)
	send_type = models.CharField(verbose_name="验证码类型", max_length=10, choices=sendType)
	c_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.name + ":   " + self.code

	class Metaeta:
		ordering = ["-c_time"]
		verbose_name = "确认码"

# class EmailVerifyRecord(models.Model):
#     # 验证码
#     code = models.CharField(max_length=20, verbose_name=u"验证码")
#     email = models.EmailField(max_length=50, verbose_name=u"邮箱")
#     # 包含注册验证和找回验证
#     send_type = models.CharField(verbose_name=u"验证码类型", max_length=10, choices=(("register",u"注册"), ("forget",u"找回密码")))
#     send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)
#     class Meta:
#         verbose_name = u"邮箱验证码"
#         verbose_name_plural = verbose_name
#     def __unicode__(self):
#         return '{0}({1})'.format(self.code, self.email)
