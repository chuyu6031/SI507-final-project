import unittest
from final_project_data import *
from model import *

class TestDatabase(unittest.TestCase):

	def test_author_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		# 85 authors
		sql = 'SELECT AuthorName FROM Author'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Airbnb',), result_list)
		self.assertEqual(len(result_list), 85)

		conn.close()

	def test_principle_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		# 99 principles
		sql = 'SELECT Heading FROM Principle'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 99)

		# 85 authors
		sql = 'SELECT AuthorId FROM Principle GROUP BY AuthorId'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 85)

		# 4 principles written by Google (Id=16)
		sql = 'SELECT Heading FROM Principle WHERE AuthorId = 16'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 4)

		conn.close()

	def test_detail_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		# 829 items
		sql = 'SELECT DetailTitle FROM Detail'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 829)

		# 85 authors
		sql = 'SELECT AuthorId FROM Detail GROUP BY AuthorId'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 85)

		# 99 principles
		sql = 'SELECT PrincipleId FROM Detail GROUP BY PrincipleId'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 99)

		conn.close()

class TestFindByAuthor(unittest.TestCase):

	def test_find_by_author(self):
		results = find_principle_by_author(author = 'IBM')
		self.assertEqual(results[0][0], 'IBM 6 UX Guidelines')

		results = find_principle_by_author(author = 'Airbnb')
		self.assertEqual(results[0][4], 2)

class TestFindByKeyword(unittest.TestCase):

	def test_find_by_keyword(self):
		results = find_principle_by_keyword(keyword = 'consistent')
		self.assertEqual(len(results), 9)
		self.assertEqual(results[0][1], 4)
		self.assertEqual(results[4][2], "Asana's Design Principles")
		self.assertEqual(results[7][4], "Facebook Design")


class TestFindByHeadingId(unittest.TestCase):

	def test_find_heading_by_headingId(self):
		result = find_heading_by_headingId(p_id = 4)
		self.assertEqual(result[0],'Principles of product and service design')

	def test_find_principle_by_headingId(self):
		results = find_principle_by_headingId(p_id = 29)
		self.assertEqual(len(results),10)
		self.assertEqual(results[6][0],'Summative Assessment')
		self.assertEqual(results[8][1],'E-learning should be transparent in its ease of use.')


class TestPlotly(unittest.TestCase):

	def test_plotly_author_number(self):
		author_plotly()

unittest.main()