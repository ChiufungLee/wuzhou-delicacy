from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,Http404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from .models import *
from apps.user.models import User
from apps.likes.models import Likes,Collections
from apps.comments.models import Comments
import json
import datetime
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#导入分页

# Create your views here.
def listArticle(request):
	if request.method == 'GET':
		thisAtc = Article.objects.all().order_by('-created_time')
		countAtc = thisAtc.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(thisAtc,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			thisAtc = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			thisAtc = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			thisAtc = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

		return render(request, "article/listArticle.html", locals())

def addArticle(request):
	if request.method == 'GET':
		atcCate = AtcCategory.objects.all()
		return render(request, "article/addArticle.html", {'atcCate':atcCate})
	else:
		title = request.POST.get('title')
		content = request.POST.get('atcContent')
		abstract = request.POST.get('abstract')
		author = request.POST.get('author')
		atcCategory = request.POST.get('category')
		settop = request.POST.get('settop')
		created_time = datetime.datetime.now()
		if author == "":
			cuser = request.session.get('user_name')
			author = User.objects.get(username=cuser)

		thisAtc = Article.objects.filter(title=title)

		if thisAtc.exists():
			return redirect('/')
		else:
			atcCate = AtcCategory.objects.get(atcCate_name=atcCategory)
			Article.objects.create(
				title=title,
				content=content,
				author=author,
				atc_category=atcCate,
				created_time=created_time,
				is_top=settop
				)
			message = '发布成功！'
			return redirect('/user/admin/')

def editArticle(request):
	if request.method == 'GET':
		atc_id = request.GET.get('articleId')
		article = Article.objects.get(article_id=atc_id)
		atcCate = AtcCategory.objects.all()
		select_val = article.atc_category.atcCate_name
		return render(request, "article/atc_edit.html", locals())
	else:
		atc_id = request.POST.get('hideId')
		title = request.POST.get('title')
		content = request.POST.get('atcContent')
		abstract = request.POST.get('abstract')
		author = request.POST.get('author')
		atcCategory = request.POST.get('category')
		settop = request.POST.get('settop')

		getcate = AtcCategory.objects.get(atcCate_name=atcCategory)
		user = User.objects.get(username=author)
		article = Article.objects.filter(article_id=atc_id).update(
			title=title,
			content=content,
			# abstract=abstract,
			atc_category=getcate.id,
			is_top=settop,
			author_id=user
			)
		# return render(request, "article/listArticle.html", locals())
		return redirect('/user/admin/') 

def delArticle(request):
	if request.method == 'GET':
		atc_id = request.GET.get('articleId')
		article = Article.objects.filter(article_id=atc_id)
		article.delete()

		thisAtc = Article.objects.all().order_by('-created_time')
		countAtc = thisAtc.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(thisAtc,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			thisAtc = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			thisAtc = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			thisAtc = paginator.page(paginator.num_pages)

		return render(request, "article/listArticle.html",locals())

def cateArticle(request):
	category = AtcCategory.objects.all().order_by('id')
	# category = Category.objects.all()

	# thisAtc = Article.objects.all().order_by('-created_time')
	countAtc = category.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(category,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		category = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		category = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		category = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	return render(request, 'article/cateArticle.html', locals())

def addArticleCate(request):
	cateName = request.GET.get('cateName')
	cateDescript = request.GET.get('cateDescript')

	thisCate = AtcCategory.objects.filter(atcCate_name=cateName)

	if thisCate.exists():
		message = '分类已存在！'
		category = AtcCategory.objects.all()
		countAtc = category.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(category,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			category = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			category = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			category = paginator.page(paginator.num_pages)
		return render(request,'article/cateArticle.html', locals())
	else:
		AtcCategory.objects.create(
			atcCate_name=cateName,
			atcCate_remark=cateDescript
			)
		message = '添加成功！'
		category = AtcCategory.objects.all()
		countAtc = category.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(category,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			category = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			category = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			category = paginator.page(paginator.num_pages)
		return render(request,'article/cateArticle.html', locals())

def updateAtcCategory(request):
	cid = request.GET.get('cid')
	cateName = request.GET.get('cateName')
	cateDescript = request.GET.get('cateDescript')
	# print(cateDescript)
	category = AtcCategory.objects.filter(id=cid).update(
		atcCate_name=cateName,
		atcCate_remark=cateDescript,
		)
	message = '更新成功！'
	return HttpResponse(message)

def delAtcCategory(request):
	if request.method == 'GET':
		cateId = request.GET.get('id')
		cate = AtcCategory.objects.filter(id=cateId)
		cate.delete()

		category = AtcCategory.objects.all().order_by('id')
		countAtc = category.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(category,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			category = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			category = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			category = paginator.page(paginator.num_pages)

		return render(request, "article/cateArticle.html",locals())

def foodNews(request):
	article = Article.objects.all().order_by('-created_time')
	countAtc = article.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(article,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		article = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		article = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		article = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	return render(request, 'article/foodNews.html',locals())


		
def article_detail(request):
	if request.method == 'GET':
		u = request.session.get('user_id')

		if u == None:
			message = '请先登录！'
			return render(request,'login/email_confirm.html', {'message':message})
		else:
			user = User.objects.get(id=u)
			userStatu = request.GET.get('u')
			atcID = request.GET.get('article_id')

			# 获取当前文章
			article = Article.objects.get(article_id=atcID)

			article.total_views += 1
			article.save(update_fields=['total_views'])

			
			
			# 资讯
			pre_article = Article.objects.filter(article_id__gt=article.article_id,atc_category=1).order_by('article_id')
			next_article = Article.objects.filter(article_id__lt=article.article_id,atc_category=1).order_by('-article_id')
			#取第1条记录
			if pre_article.count() > 0:
				pre_article = pre_article[0]
			else:
				pre_article = None
				
			if next_article.count() > 0:
				next_article = next_article[0]
			else:
				next_article = None

			# 通知
			pre_tz = Article.objects.filter(article_id__gt=article.article_id,atc_category=2).order_by('article_id')
			next_tz = Article.objects.filter(article_id__lt=article.article_id,atc_category=2).order_by('-article_id')
			#取第1条记录
			if pre_tz.count() > 0:
				pre_tz = pre_tz[0]
			else:
				pre_tz = None
				
			if next_tz.count() > 0:
				next_tz = next_tz[0]
			else:
				next_tz = None

			article_content_type = ContentType.objects.get(model = 'article')
			comments = Comments.objects.filter(content_type=article_content_type, object_id=article.article_id, parent=None).order_by('-comment_time')

			# 如果是管理员查看
			if userStatu == '0':
				return render(request, 'article/ad_AtcDetail.html',locals())
			else:
				return render(request, 'article/atc_detail.html',locals())

def settop(request):
	if request.method == 'GET':
		atc_id = request.GET.get('articleId')
		article = Article.objects.get(article_id=atc_id)
		if article.is_top == '1':
			article.is_top = '0'
			article.save()
		else:
			article.is_top = '1'
			article.save()

	thisAtc = Article.objects.all().order_by('-created_time')
	countAtc = thisAtc.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(thisAtc,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		thisAtc = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		thisAtc = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		thisAtc = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
		
	return render(request, "article/listArticle.html",locals())
	


def searchArticle(request):
	# postData = request.POST
	if request.method == 'GET':
		getTitle = request.GET.get('searchTitle')
		selectType = request.GET.get('selectType')

		if selectType == '1':
			# 标题
			title_search = Article.objects.filter(title__contains=getTitle).order_by('-created_time')
			countAtc = title_search.count()
			paginator = Paginator(title_search,10)
			page = request.GET.get('page',1)
			currentPage=int(page)
			try:
				title_search = paginator.page(page)#获取当前页码的记录
			except PageNotAnInteger:
				title_search = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
			except EmptyPage:
				title_search = paginator.page(paginator.num_pages)
			return render(request, "article/listArticle.html", {'thisAtc':title_search,'countAtc':countAtc})

		elif selectType == '2':

			# getAuthor = User.objects.get(username__contains=getTitle)
			author_search = Article.objects.filter(author__username__contains=getTitle).order_by('-created_time')
		
			countAtc = author_search.count()
			paginator = Paginator(author_search,10)
			page = request.GET.get('page',1)
			currentPage=int(page)
			try:
				author_search = paginator.page(page)#获取当前页码的记录
			except PageNotAnInteger:
				author_search = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
			except EmptyPage:
				author_search = paginator.page(paginator.num_pages)
			return render(request, "article/listArticle.html", {'thisAtc':author_search,'countAtc':countAtc})
			
	
def addTravels(request):
	if request.method == 'GET':
		u = request.session.get('user_id')

		if u == None:
			message = '请先登录！'
			return render(request,'login/email_confirm.html', {'message':message})
		else:
			typeflag = 0
			return render(request, 'article/addTravels.html',{'typeflag':typeflag})
	else:
		# travel_title = request.POST.get('travel_title')
		travel_content = request.POST.get('travel_content')
		tags = request.POST.get('tags')

		if travel_content == '':
			message = '请检查输入内容！'
			return render(request, 'article/addTravels.html', locals())
		else:
			cuser = request.session.get('user_name')
			author = User.objects.get(username=cuser)

			atcCate = AtcCategory.objects.get(atcCate_name='美食日志')

			Article.objects.create(
				title=author.username+'的日志',
				content=travel_content,
				author=author,
				atc_category=atcCate,
				)
			message = '发布成功！'

			return redirect('/article/atcListRizhi/')

def updateTravel(request):
	if request.method == 'GET':
		atcId = request.GET.get('id')
		print(atcId)
		article = Article.objects.get(article_id=atcId)
		typeflag = 1
		return render(request, 'article/addTravels.html',{'article':article,'typeflag':typeflag})
	else:
		atcId = request.GET.get('id')
		travel_title = request.POST.get('travel_title')
		travel_content = request.POST.get('travel_content')
		tags = request.POST.get('tags')

		article = Article.objects.get(article_id=atcId)
		article.title = travel_title
		article.content = travel_content
		article.tags = tags
		article.save()
		message = '更新成功！'

		return render(request, 'article/addTravels.html', locals())

def delTravel(request):
	if request.method == 'GET':
		atcId = request.GET.get('id')
		travel = Article.objects.filter(article_id=atcId)
		travel.delete()

		u = request.session.get('user_id')
		user = User.objects.get(id=u)

		myTravels = Article.objects.filter(author=user.id, atc_category=4).order_by('-created_time')

		if myTravels.count() == 0:
			resultNum = 0
		else:
			resultNum = 1

		return render(request, 'article/myTravels.html', locals())


def uploadimg(request):
	if request.method == 'POST':
		callback = request.GET.get('travel_content')
		atype = request.GET.get('atcType')
		if atype == 'rz':
		# try:
			path = "media/article/rizhi/" + time.strftime("%Y%m%d",time.localtime())
		elif atype == 'atc':
			path = "media/article/zixun/" + time.strftime("%Y%m%d",time.localtime())
		elif atype == 'dp':
			path = "media/stores/" + time.strftime("%Y%m%d",time.localtime())
		f = request.FILES["upload"]
		file_name = path + "_" + f.name
		des_origin_f = open(file_name, "wb+")  
		for chunk in f.chunks():
			des_origin_f.write(chunk)
		des_origin_f.close()
		# except Exception as e:
		# 	print(e)
		# res = "<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+file_name+"', '');</script>"
		# return HttpResponse('res')
		response_data = {}
		response_data['uploaded'] = 1
		response_data['fileName'] = file_name
		response_data['url'] = '/'+file_name
		return JsonResponse(response_data)
	else:
		raise Http404()

def article_zixun(request):
	articles = Article.objects.filter(atc_category=1).order_by('-total_views')[:10]
	atcs = Article.objects.filter(atc_category=1).order_by('-is_top','-created_time')

	countAtc = atcs.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(atcs,20)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		atcs = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		atcs = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		atcs = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
		
	return render(request, 'article/article_zixun.html', locals())

def article_rizhi(request):
	u = request.session.get('user_id')

	if u == None:
		message = '请先登录！'
		return render(request,'login/email_confirm.html', {'message':message})
	else:
		articles = Article.objects.filter(atc_category=4).order_by('-total_views')[:10]
		atcs = Article.objects.filter(atc_category=4).order_by('-created_time')

		# 获取当前登录用户
		u = request.session.get('user_id')
		user = User.objects.get(id=u)

		article_content_type = ContentType.objects.get(model = 'article')
		
		countAtc = atcs.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(atcs,20)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			atcs = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			atcs = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			atcs = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

		usercollist = []
		userlikelist = []
		likecount = []
		commentCount = []
		for atc in atcs:
			try:
				# print(atc.article_id)
				collect = Collections.objects.get(user=user, content_type=12, object_id=atc.article_id)
				
				if collect.is_collect == 1:
					iscollect = 1
					
				else:
					iscollect = 0
					

			except:
				iscollect = 0
			
			
			usercollist.append(iscollect)

			try:
				# print(atc.article_id)
				like = Likes.objects.get(user=user, content_type=12, object_id=atc.article_id)
				
				if like.is_like == 1:
					islike = 1
			
				else:
					islike = 0
				

			except:
				islike = 0
		


			commentNum = Comments.objects.filter(content_type=article_content_type.id, object_id=atc.article_id).count()
			commentCount.append(commentNum)


			userlikelist.append(islike)
			
			likeNum = Likes.objects.filter(content_type=12, object_id=atc.article_id, is_like=1).count()
			likecount.append(likeNum)


		collectList = zip(atcs,usercollist,userlikelist,likecount,commentCount)


		


		return render(request, 'article/article_rizhi.html',locals())

def myTravels(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	myTravels = Article.objects.filter(author=user.id, atc_category=4).order_by('-created_time')
	
	if myTravels.count() == 0:
		resultNum = 0
	else:
		resultNum = 1

		countAtc = myTravels.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(myTravels,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			myTravels = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			myTravels = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			myTravels = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

	return render(request, 'article/myTravels.html',locals())