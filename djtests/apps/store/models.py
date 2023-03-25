from django.db import models
from django.conf import settings

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
class Stores(models.Model):
	"""docstring for Stores"""
	# 店铺名,摘要,商家简介,地址,电话,营业时间,经度,纬度
	def upload_path(instance, filename):
		return '/'.join([settings.MEDIA_ROOT, instance, filename])

	name = models.CharField(max_length=64,verbose_name='店铺名称', unique=True)
	tabstract = models.CharField(max_length=255, null=True, blank=True, verbose_name='店铺概要')
	introduction = models.TextField(verbose_name='简介')
	img = models.ImageField(upload_to=upload_path)
	discount = models.CharField(max_length=200, null=True, blank=True, verbose_name='优惠信息')
	address = models.CharField(max_length=255, verbose_name='地址')
	phone = models.CharField(max_length=11, verbose_name='手机号')
	ontime = models.CharField(max_length=128, verbose_name='营业时间')
	longitude = models.FloatField(verbose_name='经度')
	latitude = models.FloatField(verbose_name='纬度')
	total_view = models.PositiveIntegerField(default=0)

@receiver(pre_delete, sender=Stores)	#sender=你要修改图片字段所在的类
def store_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.img.delete(False)
		



		