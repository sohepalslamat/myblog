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
        o.add_article(request.form['title'],request.form['photo_url'],request.form['author_name'],
                      request.form['body'])
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('add_article.html')



app.run()