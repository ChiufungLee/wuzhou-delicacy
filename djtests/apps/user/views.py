#coding=utf-8 
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User,ConfirmString
from apps.comments.models import Comments 
from django.conf import settings
import json
import time
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#导入分页

def admin(request):
	cuser = request.session.get('user_name')
	try:
		log_user = User.objects.get(username=cuser)
		# if log_user.exists():
		if log_user.userType == '1':
			return render(request, 'user/manage_index.html',{
				# 'article_form':article_form
				# 'articleContent':Article.content,
				'user':cuser,
				})
		else:
			message = '非管理员不能登录后台！'
			return render(request,'login/error.html',locals())	
	except:
		message = '非管理员不能登录后台！'
		return render(request,'login/email_confirm.html',locals())
	


def login(request):
	if request.method == 'GET':
		return render(request,'user/login.html')
	else:
		email = request.POST.get('username').strip()
		password = request.POST.get('password')
		print(email)
		try:
			user = User.objects.get(email=email)
		except:
			message = '用户不存在！'
			return render(request, 'login/login.html', {'message': message})

		if user.password == password:
			request.session['user']=user.username
			return redirect('/')

		else:
			message = '密码错误！'
			return render(request,'user/login.html',{'message':message})


def logout(request):
	request.session.clear()
	return redirect("/user/login/")

def islog(request):
	loginuser = "未登录"
	cuser = request.session.get('user_id')

	if cuser == None:
		return render(request,'login/base.html',{'user':loginuser})
	else:
		us = User.objects.get(id=cuser)
		print(us.id)
		return render(request,'login/base.html',{'us':us})
		
def register(request):
	if request.method == "GET":
		return render(request,"user/register.html")
	else:
		
		username = request.POST.get('username')
		password = request.POST.get('password')

		nuser = AccountInfo.objects.filter(email=username)
		if nuser:
			# msg = "failed"
			flag = 0
			return JsonResponse({"flag":flag})
			# return HttpResponse({"flag":flag})
		else:
			AccountInfo.objects.create(email=username,password=password)
			# return JsonResponse({"status": True,"msg":"注册成功！"})
			return HttpResponse("注册成功！")

def userList(request):
	userList = User.objects.all().order_by('-id')
	# print(userList)
	# userinfoList = []
	# for user in userList:
	# 	user_obj = User.objects.filter(accountId_id=user)
	# 	print(user_obj)
	# 	userinfoList.extend(user_obj)
	# accountList = userList.user_set.all()
	
	countUser = userList.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(userList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		userList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		userList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		userList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'user/userList.html', locals())

def updataUser(request):
	if request.method == 'POST':
		user_id = request.POST.get('uid')
		username = request.POST.get('username')
		gender = request.POST.get('gender')
		birthday = request.POST.get('birthday')
		email = request.POST.get('email')
		mobile = request.POST.get('phone')
		address = request.POST.get('address')
		avatar = request.FILES.get('avatar')

		if avatar == None:
			user = User.objects.get(id=user_id)
			user.username = username
			user.gender = gender
			user.birthday = birthday
			user.email = email
			user.mobile = mobile
			user.address = address
			user.save()
			message = '更新成功！'
			return render(request, 'user/userCenter.html', locals())

		else:
			file_name = avatar.name

			
			root_path = os.path.join(settings.MEDIA_ROOT,'avatars',user_id)
			print(root_path)

		

			if not os.path.exists(root_path):
				os.makedirs(root_path)

			
			timetag = time.strftime("%Y%m%d",time.localtime())
			save_path = root_path + "/" + timetag + '_' + file_name

			with open(save_path,'wb') as f:
				for chunk in avatar.chunks():
					f.write(chunk)

			user = User.objects.get(id=user_id)
			user.username = username
			user.gender = gender
			user.birthday = birthday
			user.email = email
			user.mobile = mobile
			user.address = address
			user.avatar = 'avatars/%s/%s_%s'%(user_id, timetag, file_name)
			user.save()
			message = '更新成功！'
			return render(request, 'user/userCenter.html', locals())

def searchUser(request):
	keyword = request.GET.get('keyword')

	userList = User.objects.filter(username__contains=keyword).order_by('-id')

	countUser = userList.count()
	paginator = Paginator(userList,10)
	page = request.GET.get('page',1)
	currentPage=int(page)
	try:
		userList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		userList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		userList = paginator.page(paginator.num_pages)

	return render(request, 'user/userList.html', locals())

def delUser(request):
	userId = request.GET.get('userId')
	user = User.objects.filter(id=userId)
	user.delete()

	userList = User.objects.all().order_by('-id')
	countUser = userList.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(userList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		userList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		userList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		userList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	return render(request,'user/userList.html', locals())

def adminUpdataUser(request):
	if request.method == 'GET':
		userId = request.GET.get('userId')
		userInfo = User.objects.get(id=userId)
		# userInfo = User.objects.get(email_id=user)
		return render(request, "user/editUser.html", locals())
	else:
		# atc_id = request.POST.get('hideId')
		# title = request.POST.get('title')
		# content = request.POST.get('atcContent')
		# abstract = request.POST.get('abstract')
		# author = request.POST.get('author')
		# atcCategory = request.POST.get('category')
		# settop = request.POST.get('settop')
		# print(title)
		# print(author)
		# user = User.objects.get(username=author)
		# article = Article.objects.filter(article_id=atc_id).update(
		# 	title=title,
		# 	content=content,
		# 	abstract=abstract,atc_category=atcCategory,
		# 	is_top=settop,
		# 	author_id=user
		# 	)
		# return render(request, "article/listArticle.html", locals())
		return redirect('/user/admin/') 

def adminManage(request):
	if request.method == 'GET':
		userId = request.GET.get('id')
		user = User.objects.get(id=userId)
		if user.userType == '1':
			user.userType = '0'
			user.save()

		else:
			user.userType = '1'
			user.save()

	userList = User.objects.all().order_by('-id')
	# userinfoList = []
	# for user in userList:
	# 	user_obj = User.objects.filter(accountId_id=user)
	# 	print(user_obj)
	# 	userinfoList.extend(user_obj)
	countUser = userList.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(userList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		userList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		userList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		userList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'user/userList.html', locals())

def toActive(request):
	
	userId = request.GET.get('id')
	user = User.objects.get(id=userId)

	if user.has_confirmed == False:
		user.has_confirmed = True
		user.save()
	else:
		user.has_confirmed = False
		user.save()

	userList = User.objects.all().order_by('-id')

	countUser = userList.count()
	paginator = Paginator(userList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		userList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		userList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		userList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'user/userList.html', locals())

def userConfirm(request):
	confirmList = ConfirmString.objects.all().order_by('-c_time')
	
	countConfirm = confirmList.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(confirmList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		confirmList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		confirmList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		confirmList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'user/userConfirm.html', locals())

def delConfirm(request):
	confirmId = request.GET.get('id')
	confirm = ConfirmString.objects.filter(id=confirmId)
	confirm.delete()

	confirmList = ConfirmString.objects.all().order_by('-c_time')
	
	countConfirm = confirmList.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(confirmList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		confirmList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		confirmList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		confirmList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'user/userConfirm.html', locals())

def userCenter(request):
	return render(request, 'user/userCenter.html')

def userInfo(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)
	return render(request, 'user/userInfo.html', locals())


def commentsList(request):
	commentsList = Comments.objects.all().order_by('-comment_time')
	
	countComments = commentsList.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(commentsList,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		commentsList = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		commentsList = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		commentsList = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'user/commentsList.html', locals())


def delComment(request):
	commentId = request.GET.get('id')
	comment = Comments.objects.filter(id=commentId)
	comment.delete()

	message = '删除成功！'
	return JsonResponse({'msg':message})