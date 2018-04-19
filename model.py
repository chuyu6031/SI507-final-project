import sqlite3
from flask import Flask, render_template, request

# connect to database
DBNAME = 'design.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()


# find principle by author
def find_principle_by_author(author='', DBNAE='design.db'):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	
	author_find = '''
		SELECT p.Heading, p.SourceURL, a.AuthorName
		FROM Principle AS p
			JOIN Author AS a
			ON a.Id = p.AuthorId
		WHERE a.AuthorName LIKE ?
	'''

	author_like = '%' + author + '%'
	params = (author_like,)
	p_result = cur.execute(author_find, params)
	return p_result.fetchall()


# find principle by keyword
def find_principle_by_keyword(keyword='',DBNAME='design.db'):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	keyword_find = '''
		SELECT d.DetailTitle, d.PrincipleId, p.Heading, d.AuthorId, a.AuthorName
		FROM Detail AS d
			JOIN Principle AS p
			ON p.Id = d.PrincipleId
			JOIN Author AS a
			ON a.Id = d.AuthorId
		WHERE DetailTitle LIKE ?
	'''

	keyword_like = '%' + keyword + '%'

	params = (keyword_like, )
	p_result = cur.execute(keyword_find, params)
	return p_result.fetchall()


# find principle by headingId
def find_principle_by_headingId(p_id='',DBNAME='design.db'):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	id_find = '''
		SELECT DetailTitle, DetailContent
		FROM Detail
		WHERE PrincipleId = ?
	'''

	params = (p_id, )
	p_result = cur.execute(id_find, params)
	return p_result.fetchall()




