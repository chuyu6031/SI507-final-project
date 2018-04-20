import sqlite3
from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import plotly.offline as offline



# connect to database
DBNAME = 'design.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()


# find principle by author
def find_principle_by_author(author='', DBNAE='design.db'):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	
	author_find = '''
		SELECT p.Heading, p.SourceURL, p.SourceText, a.AuthorName, p.Id
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


# find principle heading by headingId
def find_heading_by_headingId(p_id='',DBNAME='design.db'):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	heading = '''
		SELECT Heading
		FROM Principle
		WHERE Id = ?
	'''

	params = (p_id, )
	p_result = cur.execute(heading, params)
	return p_result.fetchone()



# find principle content by headingId
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



# plot the numbers of author using plotly

def author_plotly(DBNAME='design.db'):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	all_title = '''
		SELECT AuthorName, Count(AuthorName)
		FROM Author
			JOIN Principle
			ON Principle.AuthorId = Author.Id
		GROUP BY AuthorName
		ORDER BY Count(AuthorName) DESC
		'''

	title = cur.execute(all_title)
	titles = title.fetchall()

	x_list = []
	y_list = []

	for item in titles:
		x_list.append(item[0])
		y_list.append(item[1])

	data = [go.Bar(
	            x=x_list[:10],
	            y=y_list[:10]
	    )]

	layout = go.Layout(
	    title = 'The number of authors in Design Principles FTW',
	    xaxis = dict(title="Author Name"),
	    yaxis = dict(title="number"))

	fig = go.Figure(data=data, layout=layout)
	offline.plot(fig)