from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
# 文章ID
# 文章标题 
# 摘要
# 文章内容（用ckeditor来维护）
# 文章分类
# 作者
# 发布时间
# 是否置顶

class AtcCategory(models.Model):
	# 菜品分类表
	atcCate_name = models.CharField(max_length=32)
	atcCate_remark = models.CharField(max_length=255)


class Article(models.Model):
	"""docstring for Article"""
	article_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=150, verbose_name="标题")
	content = RichTextUploadingField()
	atc_category = models.ForeignKey('AtcCategory', on_delete=models.SET_NULL, null=True)
	author = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='article_author')
	created_time = models.DateTimeField(auto_now_add=True)
	total_views = models.PositiveIntegerField(default=0)
	is_top = models.CharField(max_length=1,default=0)
	tags = models.CharField(max_length=64, null=True, blank=True)
	