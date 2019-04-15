from flask import Flask,render_template,request,url_for,redirect
from models import operations
app = Flask(__name__)

o=operations()

@app.route('/')
def home():
    context = o.get_all_articles()
    return render_template('index.html',articles = context)

@app.route('/articles/add',methods=['GET','POST'])
def add_article():
    if request.method == 'POST':
        o.add_article(request.form['title'],request.form['photo_url'],request.form['author'],
                      request.form['body'])
        return redirect(url_for('home'))
    elif request.method == 'GET':
        context = o.get_all_author()
        return render_template('add_article.html',authors= context)

@app.route('/authors/add',methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        o.add_author(request.form['name'],request.form['inf'],request.form['photo_url'],request.form['photo_back_url'],
                     request.form['saying'],request.form['facebook'],request.form['twitter'])
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('add_author.html')

@app.route('/articles/delete/<int:id>')
def delete_article(id):
    o.delete_article(id)
    return redirect(url_for('home'))

@app.route('/articles/update/<int:id>',methods=['GET','POST'])
def update_article(id):
    if request.method == 'POST':
        o.update_article(id,title=request.form['title'],photo_url=request.form['photo_url'],
                         body=request.form['body'])
        return redirect(url_for('home'))
    elif request.method == 'GET':
        context= o.get_article_by_id(id)
        return render_template('update_article.html',article = context)



app.run()