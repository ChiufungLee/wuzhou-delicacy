from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comments
from apps.user.models import User
from apps.recipe.models import Recipe
# Create your views here.

def update_comment(request):
	u = request.session.get('user_id')
	referer = request.META.get('HTTP_REFERER','/')
	data = {}
	if u == None:
		data['message'] = '用户未登录！'
		data['status'] = 'ERROR'
		return JsonResponse(data)
	else:
		user = User.objects.get(id=u)
		# 获取前台用户提交的评论表单内容
		text = request.POST.get('comment_text','')
		content_type = request.POST.get('content_type','')
		object_id = int(request.POST.get('object_id',''))

		reply_comment_id = int(request.POST.get('reply_comment_id',''))

		if text == '':
			data['status'] = 'ERROR'
			data['message'] = '评论内容为空！'
			return JsonResponse(data)
		else:
			# 判断评论对象
			if content_type == 'recipe':
				c = ContentType.objects.get(model = content_type).model_class()
				model_obj = c.objects.get(rcp_id=object_id)

			elif content_type == 'article':
				c = ContentType.objects.get(model = content_type).model_class()
				model_obj = c.objects.get(article_id=object_id)

			elif content_type == 'videos':
				c = ContentType.objects.get(model = content_type).model_class()
				model_obj = c.objects.get(id=object_id)
			# 在数据库保存评论的数据记录
			comment = Comments()
			comment.user = user
			comment.text = text
			comment.content_object = model_obj

			# 判断评论类型，为0则是新评论，否则（大于0）则为回复别人的评论
			if reply_comment_id < 0:
				data['status'] = 'ERROR'
				data['message'] = '评论出错！'
				return JsonResponse(data)
			elif reply_comment_id == 0:
				parent = None

			elif Comments.objects.filter(id=reply_comment_id).exists():
				parent = Comments.objects.get(id=reply_comment_id)
				comment.root = parent.root if not parent.root is None else parent
				comment.parent = parent
				comment.reply_to = parent.user

			comment.save()
			
			# 返回数据
			data = {}
			data['status'] = 'SUCCESS'

			data['username'] = comment.user.username
			data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
			data['text'] = comment.text
			data['avatar_url'] = comment.user.avatar.url
			if not parent is None:
				data['reply_to'] = comment.reply_to.username
				data['reply_user_avatar'] = comment.reply_to.avatar.url
			else:
				data['reply_to'] = ''
			data['id'] = comment.id
			data['root_id'] = comment.root.id if not comment.root is None else ''
			return JsonResponse(data)
