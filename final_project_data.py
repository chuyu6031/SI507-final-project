import requests
import json
import sqlite3
from bs4 import BeautifulSoup

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
page_text = requests.get(base_url).text
page_soup = BeautifulSoup(page_text,'html.parser')
page_card = page_soup.find_all(class_='cards-item')

# author insert
insert_table_author = '''
	INSERT INTO Author (AuthorName)
	VALUES (?)
'''

for item in page_card:
	author = item.find(class_='collection-item-author_name').text
	params = (author,)
	cur.execute(insert_table_author, params)
	conn.commit()

# author dictionary
author_dic = {}

author_dic_state = '''
	SELECT *
	FROM Author
'''

author_dic_result = cur.execute(author_dic_state)
for author in author_dic_result:
	author_dic[author[1]] = author[0]


all_p = []

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

	all_p.append(p_dic)

print(all_p[0])

