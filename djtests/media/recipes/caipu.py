import requests
from bs4 import BeautifulSoup
import re
import pymysql

def getHTMLText(url):
	my_headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
		# 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		# 'Accept-Encoding' : 'gzip',
		# 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
	}
	try:
		r = requests.get(url,headers=my_headers)
		r.raise_for_status()
		# r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

def getRecipeList(html,cplist):
	soup = BeautifulSoup(html,'html.parser')
	recipe_div = soup.find('div',attrs={'class':'normal-recipe-list'})
	recipe_ul = recipe_div.find('ul',attrs={'class':'list'})
	# print(recipe_div.findall('a'))
	# reg = r'<p class="name"><a data-click-tracking-url="" data-expose-tracking-url="" href="(.*?)" target="_blank"></a>'
	# pattern = re.compile(reg)
	# print(recipe_ul)
	# link_a = re.findall()
	for li in recipe_ul.find_all('li'):
	# 	# a = 'https://www.xiachufang.com/recipe/' + a
	# 	# cplist.append(a)
		a = li.a.attrs['href']
		cplist.append(a)
		# break
	# cplist)
	return list(set(cplist))


def getRecipeInfo(cplist):
	ings_name_list = []
	ings_num_list = []
	step_text_list = []
	step_img_list = []
	db = pymysql.connect(host="localhost",user="root",password="Sa123456",db="dbmysite",port=3306,charset='utf8mb4')
	for a in cplist:
		# print(a)
		link_a = 'https://www.xiachufang.com' + a
		rcp_doc = getHTMLText(link_a)
		soup = BeautifulSoup(rcp_doc,'html.parser')
		rcp_name = soup.find('h1',attrs={'class':'page-title','itemprop':'name'}).string.strip()
		# rcp_desc = soup.find('div',attrs={'class':'mt30'}).string
		try:
			# rcp_desc = soup.find('div',attrs={'class':'mt30'}).string
			rcp_desc = re.findall(r'<div class="desc mt30" itemprop="description">.*?</div>',rcp_doc, re.S)[0]
			
		except:
			rcp_desc = '试试吧'
		


		rcp_img = soup.find('div',attrs={'class':'cover image expandable block-negative-margin'})
		rcp_cover = rcp_img.img.attrs['src'].split('@')[0]
		filename = rcp_cover.split('/')[-1]

		r = requests.get(rcp_cover)
		# print(filename)
		with open(filename,'wb') as f:
			f.write(r.content)
		# break
		print('封面图保存成功！')
		save_cover_url = 'recipes/' + filename

		sql = """INSERT INTO recipe_recipe(rcp_name,rcp_descript,cateid_id,tasteid_id,userid_id,rcp_img,total_view) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
		ings_sql = "INSERT INTO recipe_ingredients(quantity,name,rcpId_id) VALUES(%s, %s, %s)"
		step_sql = "INSERT INTO recipe_recipestep(serialNum,serialDption,rcpId_id,stepImg) VALUES(%s, %s, %s, %s)"
		# print(save_cover_url)
		# break
		try:
			
			para = (rcp_name,rcp_desc,'1','2','1',save_cover_url,0)
			with db.cursor() as curs:
			# cursor = db.cursor()
				curs.execute(sql,para)
				print('菜谱创建成功！')
				last_id = curs.lastrowid
				

				ings_list = soup.find_all('tr',attrs={'itemprop':'recipeIngredient'})

				for ings in ings_list:
					
					if ings.find('a'):
						
						ings_name = ings.find('a').string
					else:
						ings_name = ings.find('td',attrs={'class':'name'}).string.strip()

					ings_num = ings.find('td',attrs={'class':'unit'}).string.strip()
					# print(ings_name)
					
					curs.execute(ings_sql,(ings_num,ings_name,last_id))
					print('食材保存成功！')

				# 分类
				step_list = soup.find_all('li',attrs={'class':'container','itemprop':'recipeInstructions'})
				i = 0
				for step in step_list:
					step_text = step.find('p').string
					step_img = step.find('img').attrs['src'].split('@')[0]
					i = i + 1

					step_img_fname = step_img.split('/')[-1]
					step_img_r = requests.get(step_img)

					# print(filename)
					with open(step_img_fname,'wb') as f:
						f.write(step_img_r.content)
					# break

					# print(step_text)
					curs.execute(step_sql,(i,step_text,last_id,'recipes/'+step_img_fname))
					print('步骤保存成功！')
				db.commit()


			print('操作完成！')
		except:
			print('出错啦！')
		# finally:
			
		# 	db.close()

		


		# print(rcp_cover)


			# step_text_list.append(step_text)
			# step_img_list.append(step_img)
			# print(step_text)




def addWzmsRecipe(url,post_data):
	signin_url = 'http://122.51.235.11/login/'

	session_requests = requests.Session()
	my_headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding' : 'gzip',
		'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
	}
	result = session_requests.get(signin_url, headers=my_headers)
	# r.raise_for_status()
	# r.encoding = r.apparent_encoding
	# print(result.text)
	# reg = 
	pattern = re.compile(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">')
	token = pattern.findall(result.text)[0]
	my_data = {
		'username':'admin@163.com',
		'password':'123456',
		'csrfmiddlewaretoken':token
	}
	repo = session_requests.post(signin_url,data=my_data)


	
	r = session_requests.get(url)
	# print(r.text)
	pattern = re.compile(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">')
	add_token = pattern.findall(r.text)[0]
	post_data['csrfmiddlewaretoken'] = add_token
	add_post = session_requests.post(url,data=post_data)
	print(add_post.status_code)


if __name__ == '__main__':
	# 汤 20130  烘焙51761  凉菜20137  甜品20135  西餐40079  小吃40073  40076家常菜
	cplist_url = 'https://www.xiachufang.com/category/40076/'
	add_url = 'http://122.51.235.11/recipe/addRecipe/'
	# creat_url = 'https://www.xiachufang.com/explore/created/'
	rcp_list = []
	html = getHTMLText(cplist_url)
	# print(html)
	recipe_lists = getRecipeList(html,rcp_list)
	getRecipeInfo(recipe_lists)
	# addWzmsRecipe(add_url,post_data)