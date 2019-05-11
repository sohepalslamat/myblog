from datetime import datetime
from random import randrange
from os import path, listdir, remove
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

####################### SETTING ########################
UPLOAD_FOLDER = 'static/images/authors'
ALLOWED_EXTENSIONS = (['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arzaq.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


###########################################################################

############################## MODELS #####################################
class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    inf = db.Column(db.Text)
    # photo_back_url = db.Column(db.Text)
    saying = db.Column(db.Text)
    facebook = db.Column(db.Text)
    twitter = db.Column(db.Text)
    articles = db.relationship('Articles', backref='author')
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    # photo_url = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)
    # date_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # date_time_edit = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.now())
    date_time_edit = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())
    body = db.Column(db.Text)


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False, unique=True)
    author = db.relationship('Authors', backref='photo')


db.create_all()


class operations():
    # This operations which control the tables

    # AUTHORS
    def add_author(self, name, inf='', saying='', facebook='', twitter='', photo_id=None):
        author = Authors(name=name, inf=inf, saying=saying,
                         facebook=facebook, twitter=twitter, photo_id=photo_id)
        db.session.add(author)
        db.session.commit()
        return author.id

    def get_author_by_id(self, id):
        return Authors.query.get(id)

    def get_all_author(self):
        return Authors.query.all()

    def get_author_by_name(self, name):
        return Authors.query.filter(Authors.name == name).first()

    def update_author(self, id, name, inf, saying, facebook, twitter):
        author = self.get_author_by_id(id)
        author.name = name
        author.inf = inf
        author.saying = saying
        author.facebook = facebook
        author.twitter = twitter
        db.session.commit()

    # ARTICLES
    def add_article(self, title, author=None, body=''):
        db.session.add(Articles(title=title, author_id=author, body=body))
        db.session.commit()

    def get_article_by_id(self, id):
        return Articles.query.get(id)

    def get_articles_by_author_id(self, id):
        return Articles.query.filter(Articles.author_id == id).all()

    def get_all_articles(self):
        x = Articles.query.order_by(Articles.date_time.desc()).all()
        return x

    def update_article(self, id, title, body):
        articles = self.get_article_by_id(id)
        articles.title = title
        articles.body = body
        db.session.commit()

    def delete_article(self, id):
        Articles.query.filter_by(id=id).delete()
        db.session.commit()

    # PHOTOS
    def add_photo(self, url):
        photo = Photos(url=url)
        db.session.add(photo)
        db.session.commit()
        return photo.id

    def get_url_photo_by_id(self, id):
        photo = Photos.query.get(id)
        return photo.url

    def update_photo(self, id, url):
        photo = Photos.query.get(id)
        photo.url = url
        db.session.commit()


######################################################################################

o = operations()


################################# FUNCTIONS ############################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'photo_url' not in request.files:
            return redirect(request.url)
        file = request.files['photo_url']
        # if user does not select file, browser also
        # submit a empty part without filename
        name_file = file.filename
        if name_file == '':
            return ''
        if file.filename in listdir(UPLOAD_FOLDER):
            z = randrange(10000)
            name_file = str(z) + file.filename
        if file and allowed_file(file.filename):
            file.filename = name_file
            name_file = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], name_file))
            return app.config['UPLOAD_FOLDER'] + '/' + name_file
#########################################################################


############################# VIEWS #####################################
@app.route('/')
def home():
    context = o.get_all_articles()
    return render_template('index.html', articles=context)

############## articles ###################
@app.route('/articles/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        o.add_article(request.form['title'], request.form['author'],
                      request.form['body'])
        return redirect(url_for('home'))
    elif request.method == 'GET':
        context = o.get_all_author()
        return render_template('add_article.html', authors=context)


@app.route('/articles/delete/<int:id>')
def delete_article(id):
    o.delete_article(id)
    return redirect(url_for('home'))


@app.route('/articles/update/<int:id>', methods=['GET', 'POST'])
def update_article(id):
    if request.method == 'POST':
        o.update_article(id, title=request.form['title'],
                         body=request.form['body'])
        return redirect(url_for('home'))
    elif request.method == 'GET':
        context = o.get_article_by_id(id)
        return render_template('update_article.html', article=context)


@app.route('/articles/<string:author>/<int:id>')
def show_article(id, author):
    context = o.get_article_by_id(id)
    return render_template('show_article.html', article=context)


@app.route('/authors/<int:id>/articles')
def show_articles_by_author(id):
    this_author = o.get_author_by_id(id=id)
    articles = o.get_articles_by_author_id(this_author.id)
    return render_template('show_articles_by_author.html', articles=articles, author=this_author)


############## authors ###################
@app.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        try:
            url_photo = upload_file()
            photo_id = o.add_photo(url=url_photo)
            o.add_author(name=request.form['name'], inf=request.form['inf'], saying=request.form['saying'],
                         facebook=request.form['facebook'], twitter=request.form['twitter'], photo_id=photo_id)
            return redirect(url_for('home'))
        except:
            return redirect(request.url)
    elif request.method == 'GET':
        return render_template('add_author.html')

@app.route('/authors/update/<int:id>', methods=['GET', 'POST'])
def update_author(id):
    if request.method == 'POST':
        try:
            url_photo = upload_file()
            if url_photo != '':
                author = o.get_author_by_id(id)
                photo_id = author.photo.id
                last_url = o.get_url_photo_by_id(photo_id)
                if path.exists(last_url):
                    remove(last_url)
                o.update_photo(id=photo_id, url=url_photo)
            o.update_author(id=id, name=request.form['name'], inf=request.form['inf'], saying=request.form['saying'],
                            facebook=request.form['facebook'], twitter=request.form['twitter'])
            return redirect(url_for('home'))
        except:
            return redirect(request.url)
    elif request.method == 'GET':
        context = o.get_author_by_id(id)
        return render_template('update_author.html', author=context)


app.run()
