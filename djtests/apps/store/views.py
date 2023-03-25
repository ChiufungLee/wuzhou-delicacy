from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from apps.activity.models import FoodActivity,ActivityApply
from apps.user.models import User
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger    #导入分页
# Create your views here.
def index(request):
	return HttpResponse('hello')

def storeDetail(request):
	if request.method == 'GET':
		storeId = request.GET.get('id')
		store = Stores.objects.get(id=storeId)

		store.total_view += 1
		store.save(update_fields=['total_view'])

		activity = FoodActivity.objects.filter(chargeMan=store).first()

		if activity == None:
			flag = 0
		# print(activity)
			return render(request, 'store/storeDetail.html', locals())
		else:
			flag = 1
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

			return render(request, 'store/storeDetail.html', locals())

def addStore(request):
	if request.method == 'GET':
		return render(request, 'store/addStore.html',locals())
	else:
		name = request.POST.get('name')
		description = request.POST.get('description')
		introduction = request.POST.get('introduction')
		pic = request.FILES.get('pic')
		discount = request.POST.get('discount')
		phone = request.POST.get('phone')
		ontime = request.POST.get('ontime')
		address = request.POST.get('address')
		longitude = request.POST.get('longitude')
		latitude = request.POST.get('latitude')
		print('{0}{1}'.format(address,name))
		try:
			store = Stores.objects.get(name=name)
			if store.name.exists():
				return HttpResponse('店铺已存在！')
		except:
			# if not store.exists():
			save_path = '%s/stores/%s/%s'%(settings.MEDIA_ROOT, name, pic.name)

			dir_path = '%s/stores/%s/'%(settings.MEDIA_ROOT, name)

			if not os.path.exists(dir_path ):
				os.makedirs(dir_path)

			with open(save_path, 'wb') as f:
				# 3.获取上传文件的内容并写到创建的文件中
				for content in pic.chunks():   # pic.chunks() 上传文件的内容。
					f.write(content)

				# 4.在数据库中保存上传记录
			# store.img = 'stores/%s/%s'%(store.name,pic.name)
			Stores.objects.create(
				name=name,
				tabstract=description,
				introduction=introduction,
				discount=discount,
				address=address,
				phone=phone,
				ontime=ontime,
				longitude=longitude,
				latitude=latitude,
				img='stores/%s/%s'%(name,pic.name)
				)
			# store.save()
			return HttpResponse('上传成功')
		# except:
		#   return HttpResponse('店铺已存在！')

def delStore(request):
	storeId = request.GET.get('id')
	store = Stores.objects.filter(id=storeId)
	store.delete()

	stores = Stores.objects.all().order_by('id')
	countStore = stores.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(stores,3)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		stores = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		stores = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		stores = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	return render(request, 'store/ad_StoreList.html',locals())  

def updateStore(request):
	if request.method == 'GET':
		storeId = request.GET.get('id')
		store = Stores.objects.get(id=storeId)
		return render(request, 'store/updateStore.html',{
			'store':store,
			})
	else:
		storeId = request.POST.get('storeId')
		name = request.POST.get('name')
		tabstract = request.POST.get('tabstract')
		introduction = request.POST.get('introduction')
		pic = request.FILES.get('pic')
		discount = request.POST.get('discount')
		phone = request.POST.get('phone')
		ontime = request.POST.get('ontime')
		address = request.POST.get('address')
		longitude = request.POST.get('longitude')
		latitude = request.POST.get('latitude')

		if pic:
			# 2.创建一个文件(用于保存图片)
			save_path = '%s/stores/%s/%s'%(settings.MEDIA_ROOT, name, pic.name)

			dir_path = '%s/stores/%s/'%(settings.MEDIA_ROOT, name)

			if not os.path.exists(dir_path ):
				os.makedirs(dir_path)

			with open(save_path, 'wb') as f:
				# 3.获取上传文件的内容并写到创建的文件中
				for content in pic.chunks():   # pic.chunks() 上传文件的内容。
					f.write(content)

			store = Stores.objects.get(id=storeId)
			store.name = name
			store.tabstract=tabstract
			store.introduction=introduction
			store.discount=discount
			store.address=address
			store.phone=phone
			store.ontime=ontime
			store.longitude=float(longitude)
			store.latitude=float(latitude)
			store.img='stores/%s/%s'%(name,pic.name)
			store.save()
			return HttpResponse('更新成功！')
		else:
			store = Stores.objects.get(id=storeId)
			store.name = name
			store.tabstract=tabstract
			store.introduction=introduction
			store.discount=discount
			store.address=address
			store.phone=phone
			store.ontime=ontime
			store.longitude=float(longitude)
			store.latitude=float(latitude)
			# store.img='stores/%s/%s'%(name,pic.name)
			store.save()
			return HttpResponse('更新成功！')

def adStoreList(request):
	stores = Stores.objects.all().order_by('id')
	countStore = stores.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(stores,3)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		stores = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		stores = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		stores = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	return render(request, 'store/ad_StoreList.html',locals())

def foodStreet(request):
	stores = Stores.objects.all().order_by('-id')
	activity = FoodActivity.objects.all().order_by('-create_time')[:10]

	paginator = Paginator(stores,10)
	# 使得全局变量i可以局部使用
	global i

	if request.method == 'GET':
		
		i = 1
		storeList = paginator.page(i)#获取当前页码的记录
		return render(request, 'store/food_street.html',locals())
	else:
		i += 1
		context = {}
		idLists = []
		nameLists = []
		abstractLists = []
		timeLists = []
		phoneLists = []
		addressLists = []
		imgurlList = []

		context['content'] = paginator.page(i)
		for stores in context['content']:
				nameLists.append(stores.name)
				abstractLists.append(stores.tabstract)
				idLists.append(stores.id)
				timeLists.append(stores.ontime)
				phoneLists.append(stores.phone)
				addressLists.append(stores.address)
				imgurlList.append(stores.img.url)
				# objLists.append(stores)


		data = {}
		data['status']='SUCCESS'

		data['nameLists']=nameLists
		data['abstractLists']=abstractLists
		data['idLists']=idLists
		data['timeLists']=timeLists
		data['phoneLists']=phoneLists
		data['addressLists']=addressLists
		data['imgurlList']=imgurlList

		# data['stores']=objLists

		# 判断是否有下一页数据
		if paginator.get_page(i).has_next():
			data['has_next'] = 'ok'
		else:
			data['has_next'] = 'no'

		return JsonResponse(data)

