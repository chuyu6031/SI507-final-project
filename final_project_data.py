import requests
import json
import sqlite3
from bs4 import BeautifulSoup


# cache
Cache_name = 'design.json'

try:
	cache_open = open(Cache_name, "r")
	cache_open_str = cache_open.read()
	cache_open.close()
	all_p = json.loads(cache_open_str)
except:
	all_p = []


# build database
DBNAME = 'design.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

drop_table_author = "DROP TABLE IF EXISTS 'Author' "
drop_table_principle = "DROP TABLE IF EXISTS 'Principle' "
drop_table_details = "DROP TABLE IF EXISTS 'Detail' "

cur.execute(drop_table_author)
cur.execute(drop_table_principle)
cur.execute(drop_table_details)
conn.commit()


# create table
create_table_author = '''
	CREATE TABLE IF NOT EXISTS Author (
	Id integer PRIMARY KEY autoincrement,
	AuthorName text)
'''

create_table_principle = '''
	CREATE TABLE IF NOT EXISTS Principle (
	Id integer PRIMARY KEY autoincrement,
	Heading text,
	AuthorId integer,
	SourceText text,
	SourceURL text
	)
'''

create_table_detail = '''
	CREATE TABLE IF NOT EXISTS Detail (
	Id integer PRIMARY KEY autoincrement,
	AuthorId integer,
	PrincipleId integer,
	DetailTitle text,
	DetailContent text)
'''

cur.execute(create_table_author)
cur.execute(create_table_principle)
cur.execute(create_table_detail)
conn.commit()


# data scrawling
base_url = "https://www.designprinciplesftw.com/"

def get_data_from_web(url,p_list):

	page_text = requests.get(url).text
	page_soup = BeautifulSoup(page_text,'html.parser')
	page_card = page_soup.find_all(class_='cards-item')

	for item in page_card:
		p_dic = {}

		heading = item.find(class_='collection-item_heading').text
		p_dic['heading'] = heading

		link = item.find(class_='cards-item_link')
		url = link['href']
		p_dic['link'] = url

		author = item.find(class_='collection-item-author_name').text
		p_dic['author'] = author

		p_url = base_url + url
		p_text = requests.get(p_url).text
		p_soup = BeautifulSoup(p_text,'html.parser')

		source = p_soup.find(class_='collection-source')
		source_txt = source.find('a').text
		source_url = source.find('a')['href']
		p_dic['sourcetext'] = source_txt
		p_dic['sourceurl'] = source_url

		details = p_soup.find(class_='collection-principles_details')
		d_list = details.find_all('li',recursive=False)

		p_dic['detail'] = {}

		for d in d_list:
			title = d.find('h3').text
			p_dic['detail'][title] = ""

			content = d.find_all('p')
			for c in content:
				p_dic['detail'][title] += c.text

		p_list.append(p_dic)

	return p_list


if len(all_p) == 0:
	for i in range(3):
		page_num = i+1
		url = base_url + '?page=' + str(page_num)
		get_data_from_web(url, all_p)

	all_p_json = json.dumps(all_p)
	cache_file = open(Cache_name,"w")
	cache_file.write(all_p_json)
	cache_file.close()


# author table

author_list = []

for principle in all_p:
	if principle['author'] not in author_list:
		author_list.append(principle['author'])


author_insert = '''
	INSERT INTO Author (AuthorName)
	VALUES (?)
'''

for author in author_list:
	param = (author,)
	cur.execute(author_insert, param)
	conn.commit()

author_dic = {}

author_id_state = '''
	SELECT *
	FROM Author
'''

author_id_dic = cur.execute(author_id_state)
for author in author_id_dic:
	author_dic[author[1]] = author[0]



# principle table
principle_insert = '''
	INSERT INTO Principle (Heading, AuthorId, SourceText, SourceURL)
	VALUES (?,?,?,?)
'''

for principle in all_p:
	author_id = author_dic[principle['author']]
	param = (principle['heading'],author_id,principle['sourcetext'],principle['sourceurl'])
	cur.execute(principle_insert, param)
	conn.commit()


principle_dic = {}

principle_id_state = '''
	SELECT Id, Heading
	FROM Principle
'''

principle_id_dic = cur.execute(principle_id_state)
for principle in principle_id_dic:
	principle_dic[principle[1]] = principle[0]



# detail table
detail_insert = '''
	INSERT INTO Detail (AuthorId, PrincipleId, DetailTitle, DetailContent)
	VALUES (?,?,?,?)
'''

for principle in all_p:
	author_id = author_dic[principle['author']]
	principle_id = principle_dic[principle['heading']]
	for detail in principle['detail']:
		title = detail
		content = principle['detail'][detail]
		param = (author_id,principle_id,title,content)
		cur.execute(detail_insert,param)
		conn.commit()
