from django.db import models

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
class Banner(models.Model):
	"""docstring for Banner"""
	title = models.CharField(max_length=100, verbose_name=u'标题')
	description = models.CharField(max_length=200, verbose_name=u'图片描述',null=True)
	img = models.ImageField(upload_to='carousel/', verbose_name=u'轮播图')
	url = models.URLField(max_length=200, verbose_name=u'访问地址',default='#')
	imgIndex = models.IntegerField(default=100, verbose_name=u'顺序')
		

@receiver(pre_delete, sender=Banner)	#sender=你要修改图片字段所在的类
def banner_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.img.delete(False)