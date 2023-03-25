from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from apps.store.models import Stores
from apps.user.models import User
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#导入分页
import datetime
from datetime import timedelta
# Create your views here.
def atvtlist(request):
	activities = FoodActivity.objects.all().order_by('-host_time')

	paginator = Paginator(activities,15)
	# 使得全局变量i可以局部使用
	global i
	context = {}
	data = {}
	idLists = []
	nameLists = []
	timeLists = []
	# viewCountLists = []
	imgurlList = []

	time_status_list = []


	now = datetime.datetime.now()
	delta = datetime.timedelta(days=1)

	if request.method == 'GET':
		i = 1
		activitylists = paginator.page(i)#获取当前页码的记录

		for activity in activities:
			timeX = activity.host_time - delta
			if timeX>now:
				# 未到截止时间
				time_status = '1'
			else:
				time_status = '0'
			time_status_list.append(time_status)
			timeLists.append(timeX.strftime('%Y-%m-%d %H:%M:%S'))

		activitiesList = zip(activitylists,time_status_list,timeLists)

	else:
		i += 1

		context['content'] = paginator.page(i)
		for activity in context['content']:
			nameLists.append(activity.name)
			idLists.append(activity.id)
			imgurlList.append(activity.chargeMan.img.url)
			
			timeX = activity.host_time - delta
			
			if timeX>now:
				# 未到截止时间
				time_status = '1'
			else:
				time_status = '0'

			timeLists.append(timeX.strftime('%Y-%m-%d %H:%M:%S'))
			time_status_list.append(time_status)


		data['status']='SUCCESS'

		data['nameLists']=nameLists

		data['idLists']=idLists
		data['timeLists']=timeLists

		data['imgurlList']=imgurlList
		data['time_status_list'] = time_status_list


		# 判断是否有下一页数据
		if paginator.get_page(i).has_next():
			data['has_next'] = 'ok'
		else:
			data['has_next'] = 'no'

		return JsonResponse(data)
		# return render(request, 'activity/atvtlist.html', locals())

		

	
	
	
	return render(request, 'activity/atvtlist.html',locals())

def atvtDetail(request):
	aid = request.GET.get('id')
	activity = FoodActivity.objects.get(id=aid)

	now = datetime.datetime.now()
	delta = datetime.timedelta(days=1)

	if (activity.host_time - delta)>now:
		# 未到截止时间
		time_status = '1'
	else:
		time_status = '0'

	applyNum = ActivityApply.objects.filter(activity=activity.id).count()
	if applyNum < activity.participants:
		u = request.session.get('user_id')
		if u == None:
			apply_flag = '1'
		else:
			uid = User.objects.get(id=u)
			is_apply = ActivityApply.objects.filter(activity=activity.id,username=uid).count()
			if is_apply == 0:
				apply_flag = '1'
			else:
				apply_flag = '0'

	return render(request, 'activity/atvt_detail.html',locals())

def addActivity(request):
	if request.method == 'GET':
		sto = Stores.objects.all()
		return render(request, 'activity/addActivity.html',locals())
	else:
		name = request.POST.get('name')
		abstract = request.POST.get('abstract')
		hostTime = request.POST.get('hostTime')
		hostAddress = request.POST.get('hostAddress')
		participants = request.POST.get('participants')
		chargeMan = request.POST.get('chargeMan')
		contactPhone = request.POST.get('contactPhone')
		remark = request.POST.get('remark')

		store = Stores.objects.get(id=chargeMan)

		FoodActivity.objects.create(
			name=name,
			abstract=abstract,
			host_time=hostTime,
			host_address=hostAddress,
			participants=participants,
			chargeMan=store,
			contactPhone=contactPhone,
			remark=remark,
			
			)

		return HttpResponse('成功！')

def applyActivity(request):
	# 获取前端数据
	truename = request.GET.get('truename')
	phone = request.GET.get('phone')
	atvt_id = request.GET.get('atvt_id')

	# 获取数据库活动表数据
	activity = FoodActivity.objects.get(id=atvt_id)

	# 设置截止报名时间为活动开始前一天
	preOneday = activity.host_time - datetime.timedelta(days=1)
	
	if datetime.datetime.now() > preOneday:
		msg = '报名时间已截止！'
		return JsonResponse({'msg':msg})
	if truename == '' or phone == '':
		msg = '请检查输入内容！'
		return JsonResponse({'msg':msg})
	else:
		
		u = request.session.get('user_id')
		user = User.objects.get(id=u)
		ActivityApply.objects.create(
			truename=truename,
			mobile=phone,
			activity=activity,
			username=user
			)
		msg = '报名成功！'
		return JsonResponse({'msg':msg})

def myActivity(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	applys = ActivityApply.objects.filter(username=user)

	is_apply = ActivityApply.objects.filter(username=user).count()
	if is_apply == 0:
		flag = 0
	else:
		flag = 1

		countAtc = applys.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(applys,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			applys = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			applys = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			applys = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

	return render(request,'activity/myActivity.html',locals())

def ActivityManage(request):
	if request.method == 'GET':
		# activities = FoodActivity.objects.all()
		
		activities = FoodActivity.objects.all().order_by('-host_time')
		countAtvt = activities.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(activities,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			activities = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			activities = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			activities = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
		return render(request,'activity/ad_atvtList.html', locals())


def applyList(request):
	getId = request.GET.get('id')
	getActivity = FoodActivity.objects.get(id=getId)

	applyLists = ActivityApply.objects.filter(activity=getActivity).order_by('id')

	countApply = applyLists.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(applyLists,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		applyLists = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		applyLists = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		applyLists = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

	return render(request, 'activity/applyList.html', locals())

def editActivity(request):
	if request.method == 'GET':
		getId = request.GET.get('id')
		activity = FoodActivity.objects.get(id=getId)
		typeflag = 1
		sto = Stores.objects.all()
		return render(request, 'activity/addActivity.html', locals())

	else:
		atvtID = request.POST.get('atvtID')
		name = request.POST.get('name')
		abstract = request.POST.get('abstract')
		hostTime = request.POST.get('hostTime')
		hostAddress = request.POST.get('hostAddress')
		participants = request.POST.get('participants')
		chargeMan = request.POST.get('chargeMan')
		contactPhone = request.POST.get('contactPhone')
		remark = request.POST.get('remark')

		store = Stores.objects.get(id=chargeMan)

		activity = FoodActivity.objects.get(id=atvtID)
		activity.name = name
		activity.abstract=abstract
		activity.host_time=hostTime
		activity.host_address=hostAddress
		activity.participants=participants
		activity.chargeMan=store
		activity.contactPhone=contactPhone
		activity.remark=remark
		activity.save()

		message = '更新成功！'
		return JsonResponse({'msg':message})

def delActivity(request):
	getId = request.GET.get('id')
	activity = FoodActivity.objects.get(id=getId)
	activity.delete()

	message = '删除成功！'
	return JsonResponse({'msg':message})