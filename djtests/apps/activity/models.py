from django.db import models

# Create your models here.
class FoodActivity(models.Model):
	"""docstring for FoodActivity"""

	name = models.CharField(max_length=128,verbose_name='活动名称')
	abstract = models.TextField(verbose_name='活动详情')
	host_time = models.DateTimeField()
	host_address = models.CharField(max_length=128, null=False)
	participants = models.PositiveIntegerField(default=0)
	chargeMan = models.ForeignKey('store.Stores', on_delete=models.CASCADE)
	contactPhone = models.CharField(max_length=11)
	create_time = models.DateTimeField(auto_now_add=True)
	total_view = models.PositiveIntegerField(default=0)
	remark = models.TextField(verbose_name='备注', null=True, blank=True)

class ActivityApply(models.Model):
	"""docstring for activityApply"""
	activity = models.ForeignKey('FoodActivity', on_delete=models.CASCADE)
	truename = models.CharField(max_length=32)
	mobile = models.CharField(max_length=11)
	username = models.ForeignKey('user.User', on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)