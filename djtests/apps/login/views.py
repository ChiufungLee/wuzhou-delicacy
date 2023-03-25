from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,Http404
from django.conf import settings
from apps.user import models
from . import forms
import datetime
import hashlib
import json
import time
import os
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from apps.article.models import Article
from apps.recipe.models import Recipe,Videos,Category
from apps.banner.models import Banner
from apps.store.models import Stores
# from apps.user.models import User
# Create your views here.
def index(request):
	# if not request.session.get('is_login', None):
	# 	return redirect('/login/')
	cuser = request.session.get('user_name')
	recipes = Recipe.objects.all()[:16]
	article = Article.objects.filter(atc_category=1).order_by('-is_top','-created_time')[:10]
	tongzhi = Article.objects.filter(atc_category=2).order_by('-is_top','-created_time')[:10]
	banner = Banner.objects.all().order_by('-imgIndex')
	stores = Stores.objects.all().order_by('-id')[:8]
	vlogs = Videos.objects.all().order_by('-create_time')[:12]
	

	if cuser == None:
		return render(request,'login/index.html',{
			# 'user':loginuser,
			'recipes':recipes,
			'articles':article,
			'tongzhi':tongzhi,
			'banner':banner,
			'stores':stores,
			'vlogs':vlogs,
			
			})
	else:
		return render(request,'login/index.html',{
			'user':json.dumps(cuser,ensure_ascii=False).replace('"',''),
			'recipes':recipes,
			'articles':article,
			'tongzhi':tongzhi,
			'banner':banner,
			'stores':stores,
			'vlogs':vlogs,
			})
	# return render(request, 'login/index.html')

def loadAvatar(request):
	u = request.session.get('user_id')

	rcp_category = Category.objects.all()

	data = {}
	cate_name = []
	cate_id = []
	if u == None:
		data['status'] = 'nologin'
		return JsonResponse(data)
	
	try:
		user = models.User.objects.get(id=u)
		avatar = user.avatar.url
		usertype = user.userType
		data['avatar'] = avatar
		data['usertype'] = usertype
	except:
		pass
	for cate in rcp_category:
		cate_id.append(cate.id)
		cate_name.append(cate.catename)

	data['category_id'] = cate_id
	data['category'] = cate_name
	return JsonResponse(data)

def nav(request):
	return render(request, 'login/nav.html')

def search(request):
	u = request.session.get('user_id')

	if u == None:
		message = '请先登录！'
		return render(request,'login/email_confirm.html', {'message':message})
	else:
		keyword = request.GET.get('keyword')
		print(keyword)
		recipes = Recipe.objects.filter(rcp_name__contains=keyword)
		if recipes.count() == 0:
			message = "未查到相关记录！换个说法试试！"
		resultCount = recipes.count()
		# return JsonResponse({'recipes':recipes,'message':message})
		return render(request, 'login/searchResult.html', locals())

def register(request):
	if request.method == 'GET':
		return render(request, 'login/register.html')
	if request.method == 'POST':
		# 获取前台用户输入的表单数据
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		gender = request.POST.get('gender')
		birthday = request.POST.get('birthday')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		address = request.POST.get('address')
		# 验证数据是否符合规则
		if password1 != password2:
			message = '两次输入的密码不同！'
			return render(request, 'login/register.html', locals())
		else:
			same_name_user = models.User.objects.filter(username=username)
			if same_name_user:
				message = '用户名已经存在'
				return render(request, 'login/register.html', locals())
			same_email_user = models.User.objects.filter(email=email)
			if same_email_user:
				message = '该邮箱已经被注册了！'
				return render(request, 'login/register.html', locals())
			# 数据验证通过，在数据库创建新的记录
			new_user = models.User()
			new_user.username = username
			new_user.password = password1
			new_user.gender = gender
			new_user.birthday = birthday
			new_user.email = email
			new_user.mobile = mobile
			new_user.address = address
			new_user.userType = '0'
			new_user.has_confirmed = False
			new_user.save()

			# 生成验证码并发送到用户邮箱
			code = make_confirm_string(new_user)
			send_email(email, code)

			message = "注册成功！请前往邮箱激活账号！3秒后跳转到登录页面。"
			return render(request, 'login/email_confirm.html', locals())

def login(request):
	if request.method == 'GET':
		if request.session.get('is_login', None):  # 不允许重复登录
			return redirect('/')
		else:
			return render(request,'login/login.html')
	else:
		# 获取用户登录信息
		username = request.POST.get('username').strip()
		password = request.POST.get('password')
		# 验证登录合法性
		try:
			user = models.User.objects.get(email=username)
		except:
			message = '用户不存在！'
			return render(request, 'login/login.html', {'message': message})

		if not user.has_confirmed:
			message = '该用户还未经过邮件确认！'
			return render(request, 'login/login.html', locals())
		# 验证通过，为当前登录用户创建session，否则返回错误信息
		if user.password == password:
			request.session['is_login'] = True
			request.session['user_id'] = user.id
			request.session['user_name'] = user.username

			referer = request.META.get('HTTP_REFERER','/')
			return redirect(referer)
		else:
			message = '密码错误！'
			return render(request,'login/login.html',{'message':message})

def logout(request):
	if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
		return redirect("/login/")
	request.session.flush()
	return redirect("/login/")

def hash_code(s, salt='mysite'):
	h = hashlib.sha256()
	s += salt
	h.update(s.encode())
	return h.hexdigest()

# 生成验证码
def make_confirm_string(user):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	code = hash_code(user.username, now)
	models.ConfirmString.objects.create(code=code, user=user, send_type='register')
	return code

def send_email(email, code):

	from django.core.mail import EmailMultiAlternatives

	subject = '来自【梧州美食网】的注册确认邮件'

	text_content = '''感谢注册梧州美食网，这里是梧州本地美食资源的的站点，专注于梧州本地的美食和旅游咨询的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

	html_content = '''
                    <p>感谢注册<b>梧州美食网</b>，
                    这里是梧州美食网的站点，专注梧州本地的美食和旅游咨询的分享！</p>
                    <p>请点击以下链接完成注册确认！</p>
                    <p><a href="http://{}/confirm/?code={}" target=blank>确认注册</a></p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

	msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
	msg.attach_alternative(html_content, "text/html")
	try:
		msg.send()
	except:
		pass

def user_confirm(request):
	code = request.GET.get('code', None)
	message = ''

	try:
		confirm = models.ConfirmString.objects.get(code=code)
	except:
		message = '无效的确认请求！'
		return render(request, 'login/email_confirm.html', locals())

	c_time = confirm.c_time
	now = datetime.datetime.now()
	if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
		confirm.user.delete()
		message = '您的邮件已经过期！请重新注册！'
		return render(request, 'login/email_confirm.html', locals())
	else:
		confirm.user.has_confirmed = True
		# print(confirm.user.has_confirmed)
		confirm.user.save()
		confirm.delete()
		message = '感谢确认，请使用账户登录！'
		return render(request, 'login/email_confirm.html', locals())

@csrf_exempt
def upload_image(request):
	if request.method == 'POST':
		callback = request.POST.get('travel_content')
		atype = request.GET.get('atcType')

		file_obj = request.FILES["upload"]
		file_name = file_obj.name

		time_path = time.strftime('%Y/%m/%d', time.localtime())
		# root_path = os.path.join(settings.MEDIA_ROOT)

		if atype == 'rz':
		# try:
			typePath = 'article/rizhi'
			path = '%s/%s/%s'%(settings.MEDIA_ROOT, typePath, time_path)

			if not os.path.exists(path):
				os.makedirs(path)

		
			save_path = path + "/" + file_name

			with open(save_path,'wb') as f:
				for chunk in file_obj.chunks():
					f.write(chunk)


			response_data = {}
			response_data['uploaded'] = 1
			response_data['fileName'] = file_name
			response_data['url'] = '/media/' + typePath + '/' + time_path + '/' + file_name
			return JsonResponse(response_data)

			# path = os.path.join(settings.MEDIA_ROOT, 'article/zixun/',time_path)
		elif atype == 'zx':
			typePath = 'article/zixun'
			path = '%s/%s/%s'%(settings.MEDIA_ROOT, typePath, time_path)

			if not os.path.exists(path):
				os.makedirs(path)

		
			save_path = path + "/" + file_name

			with open(save_path,'wb') as f:
				for chunk in file_obj.chunks():
					f.write(chunk)


			response_data = {}
			response_data['uploaded'] = 1
			response_data['fileName'] = file_name
			response_data['url'] = '/media/' + typePath + '/' + time_path + '/' + file_name
			return JsonResponse(response_data)


		elif atype == 'sto':
			
			typePath = 'stores'
			print(typePath)
			sto_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
			path = '%s/%s'%(settings.MEDIA_ROOT, typePath)
		# elif atype == 'dp':
		# 	typePath = 'article/store'
		# 	path = '%s/%s/%s'%(settings.MEDIA_ROOT, typePath, time_path)
		# 	path = "media/stores/" + time.strftime("%Y%m%d%H%M%S",time.localtime())

		# print(path)


			if not os.path.exists(path):
				os.makedirs(path)

			
			save_path = path + "/" + sto_time + '_' + file_name

			with open(save_path,'wb') as f:
				for chunk in file_obj.chunks():
					f.write(chunk)
		# file_obj.close()
		# except Exception as e:
		# 	print(e)
		# res = "<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+file_name+"', '');</script>"
		# return HttpResponse('res')
			response_data = {}
			response_data['uploaded'] = 1
			response_data['fileName'] = file_name
			response_data['url'] = '/media/' + typePath + '/' + sto_time + '_' + file_name
			return JsonResponse(response_data)
	else:
		raise Http404()




def toSend_pwdEmail(request):
	u = request.session.get('user_id')
	user = models.User.objects.get(id=u)
	code = make_forget_string(user)
	send_forgetEmail(user.email,code)
	message = "发送成功！请前往邮箱确认。"
	# return render(request, 'login/email_confirm.html', locals())
	return JsonResponse({'message':message})

def make_forget_string(user):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	code = hash_code(user.username, now)
	models.ConfirmString.objects.create(code=code, user=user, send_type='forget')
	return code

def send_forgetEmail(email, code):
	from django.core.mail import EmailMultiAlternatives

	subject = '来自【梧州美食网】的找回密码确认邮件'

	text_content = '''感谢注册【梧州美食网】，这里是梧州美食网的站点，专注于梧州本地的美食和旅游咨询的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

	html_content = '''
                    <p>请保管好你的密码，以便你能更好的使用本网站。</p>
                    <p>这里是梧州美食网的站点，专注梧州本地的美食和旅游咨询的分享！</p>
                    <p>请点击以下链接完成找回确认！</p>
                    <p><a href="http://{}/updataPwd/?code={}" target=blank>修改密码</a></p>
                    <p>此链接有效期为3分钟！</p>
                    '''.format('127.0.0.1:8000', code)

	msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def forget_confirm(request):

	code = request.POST.get('code', None)
	print(code)
	message = ''

	try:
		confirm = models.ConfirmString.objects.get(code=code)
	except:
		message = '无效的确认请求！'
		return render(request, 'login/email_confirm.html', locals())

	c_time = confirm.c_time
	now = datetime.datetime.now()
	if now > c_time + datetime.timedelta(seconds=settings.CONFIRM_DAYS):
		confirm.user.delete()
		message = '您的邮件已经过期！请重新发送！'
		return render(request, 'login/email_confirm.html', locals())
	else:
		password = request.POST.get('password1')

		confirm.user.password = password
		
		confirm.user.save()
		confirm.delete()
		message = '修改成功，请重新登录！'
		request.session.flush()
		return render(request, 'login/email_confirm.html', locals())

def up_pwd_page(request):
	if request.method == 'GET':
		return render(request, 'login/up_pwd_page.html')
	else:
		return render(request, 'login/email_confirm.html', locals())

# 修改密码
def updataPwd(request):
	if request.method == 'GET':
		code = request.GET.get('code', None)
		return render(request, 'login/updataPwd.html', locals())
	else:

		message = '更新成功！'
		return render(request, 'user/userCenter.html', locals())

def about(request):
	return render(request, 'login/about.html')

def my_notifications(request):
	u = request.session.get('user_id','')
	user = models.User.objects.get(id=u)
	return render(request,'login/my_notifications.html', locals())