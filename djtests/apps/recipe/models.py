from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
# from apps.user import models as user_models
# Create your models here.
class Taste(models.Model):
	# 菜品味道表
	# tsid = models.AutoField(primary_key=True)
	tastename = models.CharField(max_length=32)
	remark = models.CharField(max_length=255)

class Category(models.Model):
	# 菜品分类表
	catename = models.CharField(max_length=32)
	remark = models.CharField(max_length=255)

class Recipe(models.Model):
	# 菜谱信息表
	rcp_id = models.AutoField(primary_key=True)
	rcp_name = models.CharField(max_length=64)
	rcp_descript = models.TextField()
	userid = models.ForeignKey('user.User', on_delete=models.CASCADE)
	cateid = models.ForeignKey('Category', on_delete=models.CASCADE)
	tasteid = models.ForeignKey('Taste', on_delete=models.CASCADE)
	rcp_img = models.ImageField(upload_to='recipes/', default='#')
	total_view = models.PositiveIntegerField(default=0)

class RecipeStep(models.Model):
	# 菜谱步骤表,包括菜谱编号，步骤序号，步骤描述等
	rcpId = models.ForeignKey('Recipe', on_delete=models.CASCADE)
	serialNum = models.CharField(max_length=16)
	serialDption = models.CharField(max_length=255)
	stepImg = models.ImageField(upload_to='recipes/', default='#')

class Ingredients(models.Model):
	# 食材信息 食材编号，食材名称，数量，描述等信息
	rcpId = models.ForeignKey('Recipe',on_delete=models.CASCADE)
	name = models.CharField(max_length=32)
	quantity = models.CharField(max_length=32)

@receiver(pre_delete, sender=Recipe)	#sender=你要修改图片字段所在的类
def recipe_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.rcp_img.delete(False)

@receiver(pre_delete, sender=RecipeStep)	#sender=你要修改图片字段所在的类
def step_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.stepImg.delete(False)

class Videos(models.Model):
	"""docstring for ClassName"""
	title = models.CharField(max_length=128)
	desc = models.CharField(max_length=255, blank=True, null=True)
	video = models.FileField(upload_to='videos/')
	cover = models.ImageField(upload_to='videos/')
	view_count = models.PositiveIntegerField(default=0)
	create_time = models.DateTimeField(auto_now=True)
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)

@receiver(pre_delete, sender=Videos)	#sender=你要修改图片字段所在的类
def step_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.video.delete(False)

@receiver(pre_delete, sender=Videos)	#sender=你要修改图片字段所在的类
def step_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.cover.delete(False)