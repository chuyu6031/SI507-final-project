from flask import Flask, render_template, request
import model

app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(debug=True)