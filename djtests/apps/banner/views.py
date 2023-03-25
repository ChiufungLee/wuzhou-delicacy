from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.banner.models import Banner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#导入分页
# Create your views here.
def uploadCarousel(request):
	return render(request,'banner/uploadCarousel.html')

def listCarousel(request):
	banner = Banner.objects.all().order_by('-imgIndex')
	countAtc = banner.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(banner,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		banner = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		banner = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		banner = paginator.page(paginator.num_pages)
	return render(request,'banner/listCarousel.html',locals())

@csrf_exempt
def editBanner(request):
	if request.method == 'GET':
		pic_id = request.GET.get('id')
		banner = Banner.objects.get(id=pic_id)
		return render(request, 'banner/editBanner.html',{
			'banner':banner,
			})
	else:
		banId = request.POST.get('banId')
		title = request.POST.get('title')
		description = request.POST.get('description')
		pic = request.FILES.get('pic')
		tourl = request.POST.get('tourl')
		imgIndex = request.POST.get('imgIndex')

		if pic:
			# 2.创建一个文件(用于保存图片)
			save_path = '%s/carousel/%s'%(settings.MEDIA_ROOT, pic.name)  # pic.name 上传文件的源文件名
			with open(save_path, 'wb') as f:
				# 3.获取上传文件的内容并写到创建的文件中
				for content in pic.chunks():   # pic.chunks() 上传文件的内容。
					f.write(content)
			banner = Banner.objects.filter(id=banId).update(
				title=title,
				description=description,
				img='carousel/%s'%pic.name,
				url=tourl,
				imgIndex=int(imgIndex)
				)
			return HttpResponse('更新成功！')
		else:
			banner = Banner.objects.filter(id=banId).update(
				title=title,
				description=description,
				# img='carousel/%s'%pic.name,
				url=tourl,
				imgIndex=int(imgIndex)
				)
			return HttpResponse('更新成功！')

def delBanner(request):
	banId = request.GET.get('id')
	banner = Banner.objects.filter(id=banId)
	banner.delete()

	banner = Banner.objects.all().order_by('-imgIndex')

	countAtc = banner.count()
	return render(request,'banner/listCarousel.html', locals())

@csrf_exempt
def upload_handle(request):
	'''上传图片处理'''
	# 1.获取上传文件的处理对象
	title = request.POST.get('title')
	description = request.POST.get('description')
	pic = request.FILES.get('pic')
	tourl = request.POST.get('tourl')
	imgIndex = request.POST.get('imgIndex')
	print(title)
	if imgIndex == "":
		imgIndex = 100
	if tourl == "":
		to_link = '#'
	else:
		to_link = tourl
	# 2.创建一个文件(用于保存图片)
	save_path = '%s/carousel/%s'%(settings.MEDIA_ROOT, pic.name)  # pic.name 上传文件的源文件名
	with open(save_path, 'wb') as f:
		# 3.获取上传文件的内容并写到创建的文件中
		for content in pic.chunks():   # pic.chunks() 上传文件的内容。
			f.write(content)

	# 4.在数据库中保存上传记录
	Banner.objects.create(
		title=title,
		description=description,
		img='carousel/%s'%pic.name,
		url=to_link,
		imgIndex=int(imgIndex)
		)
	# 5.返回
	# data = {}
	# data['msg'] = '上传成功！'
	# msg = '上传成功'
	return HttpResponse('上传成功！')