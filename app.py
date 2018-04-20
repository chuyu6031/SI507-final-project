from flask import Flask, render_template, request
from flask import Markup
import model


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('homepage.html')

@app.route('/author', methods=['GET', 'POST'])
def author():
	if request.method == 'POST':
		author = request.form['author']
		principle = model.find_principle_by_author(author)
	else:
		author = ''
		principle = model.find_principle_by_author()

	return render_template('author.html', author=author, my_list=principle)


@app.route('/keyword', methods=['GET', 'POST'])
def keyword():
	if request.method == 'POST':
		keyword = request.form['keyword']
		result = model.find_principle_by_keyword(keyword)
	else:
		keyword = ''
		result = model.find_principle_by_keyword()

	return render_template('keyword.html', keyword=keyword, my_list=result)


@app.route('/list/<p_id>', methods=['GET','POST'])
def list(p_id):
	heading = model.find_heading_by_headingId(p_id)
	content = model.find_principle_by_headingId(p_id)
	return render_template('list.html', heading=heading, my_list=content)



@app.route('/plotly')
def plotly():
	return render_template('temp-plot.html')


if __name__ == '__main__':
	app.run(debug=True)
