from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from apps.user.models import User
from apps.article.models import Article
from apps.recipe.models import Recipe,Videos
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#导入分页
# Create your views here.
def uplike(request):

	# 当前登录用户
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	obj_type = request.GET.get('type')

	if obj_type == 'article':
		# 获取点赞模型，日志或菜谱
		rzId = request.GET.get('rzId')
		obj_id = Article.objects.get(article_id=rzId)
		c = ContentType.objects.get(model = obj_type)
		getId = obj_id.article_id

	elif obj_type == 'recipe':
		rcpId = request.GET.get('rcpId')
		obj_id = Recipe.objects.get(rcp_id=rcpId)
		c = ContentType.objects.get(model = obj_type)
		getId = obj_id.rcp_id

	elif obj_type == 'videos':
		vlogId = request.GET.get('vlogId')
		obj_id = Videos.objects.get(id=vlogId)
		c = ContentType.objects.get(model = obj_type)
		getId = obj_id.id

	like_flag = 0
	likenum = Likes.objects.filter(content_type = c, object_id = getId, user=user).count()	

	if likenum > 0:
	# 	# 已点赞，取消
		like = Likes.objects.get(content_type = c, object_id = getId, user=user)
		if like.is_like == 1:
			like.is_like=0
			like.save()
			msg = '你已取消点赞'
			like_flag = 0
			# 取消赞
			return JsonResponse({'msg':msg, 'like_flag':like_flag})
		else:
			like.is_like=1
			like.save()
			msg = '点赞成功'
			like_flag = 1
			return JsonResponse({'msg':msg, 'like_flag':like_flag})

	else:
	# 	# 新加赞，添加记录
		Likes.objects.create(
				object_id = getId,
				is_like=True,
				content_type=c,
				user=user
			)

		msg = '点赞成功'
		like_flag = 1
	# 	# 点赞成功
		return JsonResponse({'msg':msg, 'like_flag':like_flag})


def upcollect(request):
	
	# 当前登录用户
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	obj_type = request.GET.get('type')

	if obj_type == 'article':
		# 获取点赞模型，日志或菜谱
		rzId = request.GET.get('rzId')
		obj_id = Article.objects.get(article_id=rzId)
		c = ContentType.objects.get(model = obj_type)
		getId = obj_id.article_id

	elif obj_type == 'recipe':
		rcpId = request.GET.get('rcpId')
		obj_id = Recipe.objects.get(rcp_id=rcpId)
		c = ContentType.objects.get(model = obj_type)
		getId = obj_id.rcp_id

	elif obj_type == 'videos':
		vlogId = request.GET.get('vlogId')
		obj_id = Videos.objects.get(id=vlogId)
		c = ContentType.objects.get(model = obj_type)
		getId = obj_id.id

	collect_flag = 0
	collectNum = Collections.objects.filter(content_type = c, object_id = getId, user=user).count()	

	if collectNum > 0:
	# 	# 已点赞，取消
		collect = Collections.objects.get(content_type = c, object_id = getId, user=user)
		if collect.is_collect == 1:
			collect.is_collect=0
			collect.save()
			msg = '你已取消收藏'
			collect_flag = 0
			data = {'msg':msg,'collect_flag':collect_flag}
			# 取消赞
			return JsonResponse(data)
		else:
			collect.is_collect=1
			collect.save()
			msg = '收藏成功'
			collect_flag = 1
			return JsonResponse({'msg':msg,'collect_flag':collect_flag})

	else:
	# 	# 新加赞，添加记录
		Collections.objects.create(
				object_id = getId,
				is_collect=True,
				content_type=c,
				user=user
			)

		msg = '新增收藏成功'
		collect_flag = 1
	# 	# 点赞成功
		return JsonResponse({'msg':msg,'collect_flag':collect_flag})

def myCollect(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	collections = Collections.objects.filter(user=user,is_collect=1).order_by('-create_time')

	if collections.count() == 0:
		resultNum = 0
	else:
		resultNum = 1

	# content = ContentType.objects.get(model='article')
		countAtvt = collections.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(collections,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			collections = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			collections = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			collections = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
		contentList = []
		typelist = []

		for collect in collections:

			getId = collect.object_id
			# print(collect.content_type.id)

			if collect.content_type.id == 12:

				result = Article.objects.get(article_id=getId)
				contentList.append(result.title)
				resultType = '1'
				typelist.append(resultType)
			elif collect.content_type.id == 9:
				result = Recipe.objects.get(rcp_id=getId)
				contentList.append(result.rcp_name)
				resultType = '2'
				typelist.append(resultType)
			elif collect.content_type.id == 27:
				result = Videos.objects.get(id=getId)
				contentList.append(result.title)
				resultType = '3'
				typelist.append(resultType)
			
			# contentList.append(result.title)
			# print(result.content)
		finishreturn = zip(collections,contentList,typelist)

		
			
	return render(request, 'user/myCollect.html', locals())

def delCollect(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	getId = request.GET.get('id')
	collect = Collections.objects.get(id=getId)
	collect.delete()

	collections = Collections.objects.filter(user=user).order_by('-create_time')
	if collections.count() == 0:
		resultNum = 0
	else:
		resultNum = 1

	# content = ContentType.objects.get(model='article')
	contentList = []
	typelist = []

	for collect in collections:

		getId = collect.object_id
		# print(collect.content_type.id)

		if collect.content_type.id == 12:

			result = Article.objects.get(article_id=getId)
			contentList.append(result.title)
			resultType = '1'
			typelist.append(resultType)
		elif collect.content_type.id == 9:
			result = Recipe.objects.get(rcp_id=getId)
			contentList.append(result.rcp_name)
			resultType = '2'
			typelist.append(resultType)
			
	finishreturn = zip(collections,contentList,typelist)

	return render(request, 'user/myCollect.html', locals())
	