from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Likes(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	is_like = models.BooleanField(default=False)
	create_time = models.DateTimeField(auto_now=True)

class Collections(models.Model):
	"""docstring for Collections"""
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	is_collect = models.BooleanField(default=False)
	create_time = models.DateTimeField(auto_now=True)

