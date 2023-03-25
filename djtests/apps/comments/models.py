from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Comments(models.Model):
	"""docstring for Comment"""
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type','object_id')

	text = models.TextField()
	comment_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey('user.User', related_name='comments', on_delete=models.CASCADE)

	# 方便获取每一条评论下回复数
	root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)

	parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.CASCADE)
	reply_to = models.ForeignKey('user.User', null=True, related_name='replies', on_delete=models.CASCADE)

	def __str__(self):
		return self.text

	class Meta:
		ordering = ['comment_time']
