from _datetime import datetime
from main import db

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    inf = db.Column(db.Text)
    #photo_back_url = db.Column(db.Text)
    saying = db.Column(db.Text)
    facebook = db.Column(db.Text)
    twitter = db.Column(db.Text)
    articles = db.relationship('Articles', backref='author')
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text,nullable=False)
    #photo_url = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)
    #date_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #date_time_edit = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    date_time = db.Column(db.DateTime(timezone=True), default=datetime.now())
    date_time_edit = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())
    body = db.Column(db.Text)

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False, unique=True)
    author = db.relationship('Authors', backref='photo')


db.create_all()

class operations():

    def add_author(self, name, inf='', saying='', facebook='', twitter='',photo_id=None):
        author = Authors(name=name, inf=inf, saying=saying,
                         facebook=facebook, twitter=twitter,photo_id=photo_id)
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



    ######

    def add_article(self, title, author=None, body=''):
        db.session.add(Articles(title=title, author_id=author, body=body))
        db.session.commit()

    def get_article_by_id(self, id):
        return Articles.query.get(id)

    def get_articles_by_author_id(self, id):
        return Articles.query.filter(Articles.author_id == id).all()

    def get_all_articles(self):
        x=Articles.query.order_by(Articles.date_time.desc()).all()
        return x

    def update_article(self, id, title, body):
        articles = self.get_article_by_id(id)
        articles.title = title
        articles.body = body
        db.session.commit()

    def delete_article(self,id):
        Articles.query.filter_by(id=id).delete()
        db.session.commit()

    ###############
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

