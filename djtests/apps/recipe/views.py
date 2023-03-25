from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import *
from apps.user.models import User
from apps.likes.models import Likes,Collections
from apps.comments.models import Comments
import os
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#导入分页

# Create your views here.

def listRecipe(request):
	recipes = Recipe.objects.all().order_by('rcp_id')
	countAtc = recipes.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(recipes,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		recipes = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		recipes = paginator.page(1)#如果页码不是整数时,显示第1页的内容
	except EmptyPage:
		recipes = paginator.page(paginator.num_pages)
		#如果页数不在系统的页码列表中时,显示最后一页的内容
	return render(request,'recipe/listRecipe.html', locals())

def listIngres(request):
	ingredients = Ingredients.objects.all().order_by('id')
	countAtc = ingredients.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(ingredients,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		ingredients = paginator.page(currentPage)#获取当前页码的记录
	except PageNotAnInteger:
		ingredients = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		ingredients = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	if paginator.num_pages > 15:
		if currentPage - 7 < 1:
			pageRange = range(1,16)
		elif currentPage + 7 > paginator.num_pages:
			pageRange = range(paginator.num_pages-14,paginator.num_pages+1)
		else:
			pageRange = range(currentPage - 7,currentPage + 8)
	else:
		pageRange = paginator.page_range
	return render(request, 'recipe/recipeIngres.html', locals())

def testadd(request):
	if request.method == 'GET':
		return render(request, 'recipe/add.html')
	else:
		title = request.POST.getlist('title')
		stepImg = request.FILES.getlist('stepImg')
		getuser = request.session.get('user_id')
		k = 1
		for i,j in zip(title,stepImg):
			print(i)
			print(j.name)
			print(k)
			save_path = '%s/recipes/%s/%s'%(settings.MEDIA_ROOT, getuser, str(k)+'.jpg')
			dir_path = '%s/recipes/%s'%(settings.MEDIA_ROOT, getuser)

			if not os.path.exists(dir_path ):
				os.makedirs(dir_path)

			with open(save_path, 'wb') as f:
				for content in j.chunks():   # pic.chunks() 上传文件的内容。
					f.write(content)

			k+=1
		return HttpResponse('hahha ')

def recipeDetail(request):
	if request.method == 'GET':
		# 获取登录用户的session，判断是否登录
		u = request.session.get('user_id')
		if u == None:
			message = '请先登录！'
			return render(request,'login/email_confirm.html', {'message':message})
		else:
			# 获取用户点击时传给后台的菜谱ID
			rcpId = request.GET.get('id')
			# 访问数据库，并将菜谱的浏览量+1
			recipe = Recipe.objects.get(rcp_id=rcpId)
			recipe.total_view += 1
			recipe.save(update_fields=['total_view'])
			# 获取菜谱外键表食材和步骤的信息
			recipeStep = RecipeStep.objects.filter(rcpId=rcpId)
			ingredients = Ingredients.objects.filter(rcpId=rcpId)

			user = User.objects.get(id=u)
			try:
				# 根据登录用户访问点赞表的数据，判断此对象（菜谱）当前登录用户是否进行了点赞操作
				like = Likes.objects.get(user=user, content_type=9, object_id=recipe.rcp_id)
				if like.is_like == 1:
					islike = 1
				else:
					islike = 0
			except:
				islike = 0

			# 显示收藏信息
			try:
				# print(atc.article_id)
				collect = Collections.objects.get(user=user, content_type=9, object_id=recipe.rcp_id)
				
				if collect.is_collect == 1:
					iscollect = 1
				else:
					iscollect = 0
			except:
				iscollect = 0
			# 判断当前详情页对象的点赞数，并访问评论表将相关数据一并返回。
			rcpLikeNum = Likes.objects.filter(content_type=9, object_id=recipe.rcp_id, is_like=1).count()
			recipe_content_type = ContentType.objects.get(model = 'recipe')
			comments = Comments.objects.filter(
				content_type=recipe_content_type,
				object_id=recipe.rcp_id,
				parent=None
				).order_by('-comment_time')

			return render(request, 'recipe/recipeDetail.html', locals())

def addRecipe(request):
	if request.method == 'GET':
		u = request.session.get('user_id')

		if u == None:
			message = '请先登录！'
			return render(request,'login/email_confirm.html', {'message':message})
		else:
		# 	print
			category = Category.objects.all()
			tastes = Taste.objects.all()
			return render(request, 'recipe/addRecipe.html', locals())
	else:
		name = request.POST.get('name')
		description = request.POST.get('description')
		category = request.POST.get('category')
		taste = request.POST.get('taste')
		productPic = request.FILES.get('productPic')
		getuser = request.session.get('user_id')

		getuserRecipe = Recipe.objects.filter(rcp_name=name,userid=getuser).count()
		# print(getuserRecipe)
		if getuserRecipe >= 1:
			message = '你已发表过同名菜谱！一个用户不能发表两个同名菜谱！'
			category = Category.objects.all()
			tastes = Taste.objects.all()
			return render(request, 'recipe/addRecipe.html', locals())

		# 获取外键数据
		rcp_cate = Category.objects.get(catename=category)
		rcp_taste = Taste.objects.get(tastename=taste)
		author = User.objects.get(id=getuser)

		# 保存文件
		save_path = '%s/recipes/%s/%s/%s'%(settings.MEDIA_ROOT, getuser, name, productPic.name)
		dir_path = '%s/recipes/%s/%s'%(settings.MEDIA_ROOT, getuser, name)

		if not os.path.exists(dir_path ):
			os.makedirs(dir_path)

		with open(save_path, 'wb') as f:
			for content in productPic.chunks():   # pic.chunks() 上传文件的内容。
				f.write(content)

		Recipe.objects.create(
			rcp_name=name,
			rcp_descript=description,
			userid=author,
			cateid=rcp_cate,
			tasteid=rcp_taste,
			
			rcp_img='recipes/%s/%s/%s'%(getuser, name, productPic.name)
			# total_view=0
			)

		saveRcp = Recipe.objects.get(rcp_name=name)

		# 保存配料
		ingeName = request.POST.getlist('ingeName')
		ingeQuantity = request.POST.getlist('ingeQuantity')

		for i,j in zip(ingeName,ingeQuantity):
			Ingredients.objects.create(
				name=i,
				quantity=j,
				rcpId=saveRcp
				)

		# 保存菜品步骤
		stepDesp = request.POST.getlist('stepDesp')
		stepImg = request.FILES.getlist('stepImg')
		
		k = 1
		for i,j in zip(stepDesp,stepImg):
			save_path = '%s/recipes/%s/%s/%s'%(settings.MEDIA_ROOT, getuser, name, str(k)+'.jpg')

			with open(save_path, 'wb') as f:
				for content in j.chunks():   # pic.chunks() 上传文件的内容。
					f.write(content)

			RecipeStep.objects.create(
				serialNum=k,
				serialDption=i,
				stepImg='recipes/%s/%s/%s'%(getuser, name, str(k)+'.jpg'),
				rcpId=saveRcp
				)
			k+=1
		message = '发布成功！'

		return render(request, 'login/error.html', locals())

def delRecipe(request):
	rid = request.GET.get('id')
	print(rid)
	recipe = Recipe.objects.filter(rcp_id=rid)
	recipe.delete()

	msg = '删除成功！'
	return JsonResponse({'msg':msg})

def updateRecipe(request):
	if request.method == 'GET':
		rid = request.GET.get('id')
		recipe = Recipe.objects.get(rcp_id=rid)
		category = Category.objects.all()
		tastes = Taste.objects.all()

		ingredients = Ingredients.objects.filter(rcpId=recipe)
		rcpsteps = RecipeStep.objects.filter(rcpId=recipe)
		
		return render(request, 'recipe/updateRecipe.html',locals())
	else:
		rid = request.POST.get('rid')
		name = request.POST.get('name')
		description = request.POST.get('description')
		category = request.POST.get('category')
		taste = request.POST.get('taste')
		productPic = request.FILES.get('productPic')
		getuser = request.session.get('user_id')
		getuserRecipe = Recipe.objects.filter(rcp_name=name,userid=getuser).count()
		# print(getuserRecipe)
		if getuserRecipe > 1:
			message = '你已发表过同名菜谱！一个用户不能发表两个同名菜谱！'
			category = Category.objects.all()
			tastes = Taste.objects.all()
			return render(request, 'recipe/updateRecipe.html', locals())

		# 获取外键数据
		rcp_cate = Category.objects.get(catename=category)
		rcp_taste = Taste.objects.get(tastename=taste)
		author = User.objects.get(id=getuser)

		recipe = Recipe.objects.get(rcp_id=rid)

		if productPic != None:
			# 保存文件
			save_path = '%s/recipes/%s/%s/%s'%(settings.MEDIA_ROOT, getuser, name, productPic.name)
			dir_path = '%s/recipes/%s/%s'%(settings.MEDIA_ROOT, getuser, name)

			with open(save_path, 'wb') as f:
				for content in productPic.chunks():   # pic.chunks() 上传文件的内容。
					f.write(content)

			
			recipe.rcp_name = name
			recipe.rcp_descript = description
			recipe.userid = author
			recipe.cateid = rcp_cate
			recipe.tasteid = rcp_taste
			recipe.rcp_img = 'recipes/%s/%s/%s'%(getuser, name, productPic.name)
			recipe.save()
		else:
			recipe.rcp_name = name
			recipe.rcp_descript = description
			recipe.userid = author
			recipe.cateid = rcp_cate
			recipe.tasteid = rcp_taste
			# recipe.rcp_img = 'recipes/%s/%s/%s'%(getuser, rid, productPic.name)
			recipe.save()


		# 保存配料
		ingeName = request.POST.getlist('ingeName')
		ingeQuantity = request.POST.getlist('ingeQuantity')

		ingre = Ingredients.objects.filter(rcpId=rid)

		print(ingre[0])	
		for k in range(len(ingeName)):
			ingre[k].name = ingeName[k]
			ingre[k].quantity = ingeQuantity[k]
			ingre[k].save()


		

			print(range(len(ingeName)))	
			print(ingeQuantity[k])	


		# 保存菜品步骤
		# stepDesp = request.POST.getlist('stepDesp')
		# stepImg = request.FILES.getlist('stepImg')
		# print()
		# stepRcp = RecipeStep.objects.filter(rcpId=rid)
		# for j in range(len(stepDesp)):
		# 	stepRcp[j].serialNum=j+1
		# 	stepRcp[j].serialDption=stepDesp[j]
		# 	stepRcp[j].stepImg=stepImg[j]
		# 	stepRcp[j].save()

		# 	save_path = '%s/recipes/%s/%s/%s'%(settings.MEDIA_ROOT, getuser, name, str(j+1)+'.jpg')

		# 	with open(save_path, 'wb') as f:
		# 		for content in stepImg[j].chunks():   # pic.chunks() 上传文件的内容。
		# 			f.write(content)


		message = '修改成功！'
		return render(request, 'user/userCenter.html', locals()) 

def adDelRecipe(request):
	if request.method == 'GET':
		rcpId = request.GET.get('id')
		recipe = Recipe.objects.filter(rcp_id=rcpId)
		recipe.delete()

		recipes = Recipe.objects.all().order_by('rcp_id')
		countAtc = recipes.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(recipes,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			recipes = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			recipes = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			recipes = paginator.page(paginator.num_pages)

		return render(request, "recipe/listRecipe.html",locals())

def listCategory(request):
	category = Category.objects.all().order_by('id')
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
	return render(request,'recipe/recipeCategory.html', locals())

def addCategory(request):
	cateName = request.GET.get('cateName')
	cateDescript = request.GET.get('cateDescript')

	thisCate = Category.objects.filter(catename=cateName)

	if thisCate.exists():
		message = '分类已存在！'
		category = Category.objects.all()
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
		return render(request,'recipe/recipeCategory.html', locals())
	else:
		Category.objects.create(
			catename=cateName,
			remark=cateDescript
			)
		message = '添加成功！'
		category = Category.objects.all()
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
		return render(request,'recipe/recipeCategory.html', locals())

def updateCategory(request):
	cid = request.GET.get('cid')
	cateName = request.GET.get('cateName')
	cateDescript = request.GET.get('cateDescript')
	print(cateDescript)
	category = Category.objects.filter(id=cid).update(
		catename=cateName,
		remark=cateDescript,
		)
	message = '更新成功！'
	return HttpResponse(message)


def delCategory(request):
	if request.method == 'GET':
		cateId = request.GET.get('id')
		cate = Category.objects.filter(id=cateId)
		cate.delete()

		category = Category.objects.all().order_by('id')
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

		return render(request, "recipe/recipeCategory.html",locals())

def listTaste(request):
	tastes = Taste.objects.all().order_by('id')

	countAtc = tastes.count()
	# 分页实现
	# 生成paginator对象,定义每页显示10条记录
	paginator = Paginator(tastes,10)
	#从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#把当前的页码数转换成整数类型
	currentPage=int(page)
	try:
		tastes = paginator.page(page)#获取当前页码的记录
	except PageNotAnInteger:
		tastes = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		tastes = paginator.page(paginator.num_pages)
		#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

	return render(request,'recipe/recipeTaste.html', locals())

def addTaste(request):
	tasteName = request.GET.get('tasteName')
	tasteDescript = request.GET.get('tasteDescript')

	thisTaste = Taste.objects.filter(tastename=tasteName)

	if thisTaste.exists():
		message = '分类已存在！'
		tastes = Taste.objects.all().order_by('id')

		countAtc = tastes.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(tastes,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			tastes = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			tastes = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			tastes = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
		return render(request,'recipe/recipeTaste.html', locals())
	else:
		Taste.objects.create(
			tastename=tasteName,
			remark=tasteDescript
			)
		message = '添加成功！'
		tastes = Taste.objects.all().order_by('id')

		countAtc = tastes.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(tastes,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			tastes = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			tastes = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			tastes = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
		return render(request,'recipe/recipeTaste.html', locals())

def updateTaste(request):
	tasteId = request.GET.get('tasteId')
	tasteName = request.GET.get('tasteName')
	tasteDescript = request.GET.get('tasteDescript')
	print(tasteName)
	print(tasteDescript)
	taste = Taste.objects.filter(id=tasteId).update(
		tastename=tasteName,
		remark=tasteDescript,
		)
	message = '更新成功！'
	return HttpResponse(message)

def delTaste(request):
	if request.method == 'GET':
		tasteId = request.GET.get('id')
		taste = Taste.objects.filter(id=tasteId)
		taste.delete()

		tastes = Taste.objects.all().order_by('id')
		countAtc = tastes.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(tastes,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			tastes = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			tastes = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			tastes = paginator.page(paginator.num_pages)

		return render(request, "recipe/recipeTaste.html",locals())

def rcpUcList(request):
	cateId = request.GET.get('cateId')
	
	# 按照浏览次数降序排列
	recipes = Recipe.objects.all().order_by('-total_view')[:15]

	ingredients = Ingredients.objects.all().order_by('rcpId')

	# 使得全局变量i可以局部使用
	global i

	context = {}
	data = {}
	idLists = []
	nameLists = []
	userLists = []
	imgurlList = []


	if cateId == '0':
		
		rcps = Recipe.objects.all().order_by('-rcp_id')

		paginator = Paginator(rcps,75)

		if request.method == 'GET':
			
			i = 1
			rcpList = paginator.page(i)#获取当前页码的记录
			# return render(request, 'store/food_street.html',locals())
			return render(request, 'recipe/recipe_uclist.html',locals())
		else:
			i += 1

			context['content'] = paginator.page(i)
			for recipe in context['content']:
					nameLists.append(recipe.rcp_name)
					idLists.append(recipe.rcp_id)
					imgurlList.append(recipe.rcp_img.url)
					userLists.append(recipe.userid.username)


			
			data['status']='SUCCESS'

			data['nameLists']=nameLists

			data['idLists']=idLists
			data['userLists']=userLists

			data['imgurlList']=imgurlList
			
			# data['stores']=objLists

			# 判断是否有下一页数据
			if paginator.get_page(i).has_next():
				data['has_next'] = 'ok'
			else:
				data['has_next'] = 'no'

			return JsonResponse(data)
	else:

		rcps = Recipe.objects.filter(cateid=cateId)

		paginator = Paginator(rcps,15)

		category = Category.objects.get(id=cateId)

		if request.method == 'GET':
			
			i = 1
			rcpList = paginator.page(i)#获取当前页码的记录
			catename = category.catename
			
			return render(request, 'recipe/recipe_uclist.html',locals())
		else:
			i += 1

			context['content'] = paginator.page(i)
			for recipe in context['content']:
					nameLists.append(recipe.rcp_name)
					idLists.append(recipe.rcp_id)
					imgurlList.append(recipe.rcp_img.url)
					userLists.append(recipe.userid.username)


			data['status']='SUCCESS'

			data['nameLists']=nameLists

			data['idLists']=idLists
			data['userLists']=userLists

			data['imgurlList']=imgurlList
			


			# 判断是否有下一页数据
			if paginator.get_page(i).has_next():
				data['has_next'] = 'ok'
			else:
				data['has_next'] = 'no'

			return JsonResponse(data)
		




	

def foodvlog(request):
	vlogs = Videos.objects.all().order_by('-create_time')

	# rcps = Recipe.objects.all().order_by('-rcp_id')

	paginator = Paginator(vlogs,16)
	# 使得全局变量i可以局部使用
	global i
	context = {}
	data = {}
	idLists = []
	titleLists = []
	timeLists = []
	viewCountLists = []
	imgurlList = []

	if request.method == 'GET':
		i = 1
		vloglists = paginator.page(i)#获取当前页码的记录
		return render(request, 'recipe/foodvlog.html', locals())
	else:
		# 加载更多
		i += 1

		context['content'] = paginator.page(i)

		for vlog in context['content']:
				titleLists.append(vlog.title)
				timeLists.append(vlog.create_time)
				idLists.append(vlog.id)
				imgurlList.append(vlog.cover.url)
				viewCountLists.append(vlog.view_count)
				# print(vlog.create_time.)


		data['status']='SUCCESS'

		data['titleLists']=titleLists

		data['idLists']=idLists
		data['timeLists']=timeLists
		data['viewCountLists']=viewCountLists

		data['imgurlList']=imgurlList
		


		# 判断是否有下一页数据
		if paginator.get_page(i).has_next():
			data['has_next'] = 'ok'
		else:
			data['has_next'] = 'no'

		return JsonResponse(data)

def vlogDetail(request):
	u = request.session.get('user_id')

	if u == None:
		message = '请先登录！'
		return render(request,'login/email_confirm.html', {'message':message})
	else:
		vlogId = request.GET.get('id')

		vlog = Videos.objects.get(id=vlogId)

		vlog.view_count += 1
		vlog.save(update_fields=['view_count'])

		tjVlogs = Videos.objects.all().order_by('-view_count')[:10]

		# recipeStep = RecipeStep.objects.filter(id=rcpId)

		uid = request.session['user_id']
		user = User.objects.get(id=uid)

		try:
			# print(atc.article_id)
			like = Likes.objects.get(user=user, content_type=27, object_id=vlog.id)
			
			if like.is_like == 1:
				islike = 1
			else:
				islike = 0

		except:
			islike = 0

		# 显示收藏信息
		try:
			# print(atc.article_id)
			collect = Collections.objects.get(user=user, content_type=27, object_id=vlog.id)
			
			if collect.is_collect == 1:
				iscollect = 1
			else:
				iscollect = 0
		except:
			iscollect = 0

		vlogLikeNum = Likes.objects.filter(content_type=27, object_id=vlog.id, is_like=1).count()

		

		vlog_content_type = ContentType.objects.get(model = 'videos')
		comments = Comments.objects.filter(content_type=vlog_content_type, object_id=vlog.id, parent=None).order_by('-comment_time')

		return render(request, 'recipe/vlogDetail.html', locals())

def addVlogs(request):
	if request.method == 'GET':
		u = request.session.get('user_id')

		if u == None:
			message = '请先登录！'
			return render(request,'login/email_confirm.html', {'message':message})
		else:
			return render(request, 'recipe/addvlog.html')
	else:
		title = request.POST.get('title')
		desc = request.POST.get('desc')
		vlogVideo = request.FILES.get('vlog')
		coverPic = request.FILES.get('coverPic')

		u = request.session.get('user_id')
		user = User.objects.get(id=u)

		timeStr = time.strftime("%Y%m%d",time.localtime())

		dir_path = '%s/videos/%s/coverPic/'%(settings.MEDIA_ROOT, user.id, )
		# dir_path = '%s/videos/%s/'%(settings.MEDIA_ROOT, user.id, )

		if not os.path.exists(dir_path ):
			os.makedirs(dir_path)

		# 保存视频
		vlog_save_path = '%s/videos/%s/%s'%(settings.MEDIA_ROOT, user.id, timeStr+'_'+vlogVideo.name)

		with open(vlog_save_path, 'wb') as f:
			# 3.获取上传文件的内容并写到创建的文件中
			for content in vlogVideo.chunks():   # pic.chunks() 上传文件的内容。
				f.write(content)

		# 保存图片
		cover_save_path = '%s/videos/%s/coverPic/%s'%(settings.MEDIA_ROOT, user.id, timeStr + '_' + coverPic.name)
		
		with open(cover_save_path, 'wb') as f:
			# 3.获取上传文件的内容并写到创建的文件中
			for content in coverPic.chunks():   # pic.chunks() 上传文件的内容。
				f.write(content)


		

		Videos.objects.create(
			title=title,
			desc=desc,
			video='videos/%s/%s'%(user.id, timeStr + '_' + vlogVideo.name),
			user=user,
			cover='videos/%s/coverPic/%s'%(user.id, timeStr + '_' + coverPic.name),
			)
		message = 'Vlog上传成功！'

		return render(request, 'login/error.html', {'message':message})

def delVlog(request):
	vlogId = request.GET.get('id')
	vlog = Videos.objects.filter(rcp_id=vlogId)
	vlog.delete()

	msg = '删除成功！'
	return JsonResponse({'msg':msg})

def myRecipes(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	myRecipes = Recipe.objects.filter(userid=user.id).order_by('-rcp_id')

	has_recipe = myRecipes.count()
	if has_recipe == 0:
		flag = 0
	else:
		flag = 1

		countAtc = myRecipes.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(myRecipes,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			myRecipes = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			myRecipes = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			myRecipes = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容


	return render(request, 'recipe/myRecipes.html',locals())

def myVlogs(request):
	u = request.session.get('user_id')
	user = User.objects.get(id=u)

	myVlogs = Videos.objects.filter(user=user).order_by('-create_time')

	has_vlogs = myVlogs.count()
	if has_vlogs == 0:
		flag = 0
	else:
		flag = 1

		countAtc = myVlogs.count()
		# 分页实现
		# 生成paginator对象,定义每页显示10条记录
		paginator = Paginator(myVlogs,10)
		#从前端获取当前的页码数,默认为1
		page = request.GET.get('page',1)
		#把当前的页码数转换成整数类型
		currentPage=int(page)
		try:
			myVlogs = paginator.page(page)#获取当前页码的记录
		except PageNotAnInteger:
			myVlogs = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
		except EmptyPage:
			myVlogs = paginator.page(paginator.num_pages)
			#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
			
	return render(request, 'recipe/myVlogs.html',locals())