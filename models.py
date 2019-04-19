from time import strftime

from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, CharField, DateTimeField

from db import con_db

con = con_db()
dtb = SqliteDatabase(con.database,pragmas={'foreign_keys': 1})


class Authors(Model):
    name = CharField(max_length=70)
    inf = TextField(null=True)
    photo_url = TextField(null=True)
    photo_back_url = TextField(null=True)
    saying = TextField(null=True)
    facebook = TextField(null=True)
    twitter = TextField(null=True)

    class Meta:
        database = dtb


class Articles(Model):
    title = TextField()
    #photo_url = TextField(null=True)
    author = ForeignKeyField(Authors)
    date_time = DateTimeField(formats=['%d-%b-%Y'],default=strftime('%Y-%m-%d %H:%M:%S'))
    date_time_edit = DateTimeField(null=True,default=None)
    body = TextField()

    class Meta:
        database = dtb


dtb.connect()
dtb.create_tables([Authors, Articles])


class operations:
    def add_author(self, name, inf='',
                   photo_url='https://sandbox-uploads.imgix.net/u/1555162859-11025120fb71ec169dadf040509941ea?w=600'
                   , saying='', facebook='', twitter=''):
        Authors.create(name=name, inf=inf, photo_url=photo_url,
                       saying=saying, facebook=facebook, twitter=twitter)
        dtb.commit()

    def get_author_by_id(self, id):
        return Authors.get_by_id(id)


    def get_all_author(self):
        return Authors.select()

    def get_author_by_name(self, name):
        return Authors.get(Authors.name == name)

    def get_auther_name_by_id(self,id):
        return Authors.get_by_id(id).name



    ############

    def add_article(self, title , author=None , body=''):

        Articles.create(title=title,author=author,body=body)
        dtb.commit()


    def get_article_by_id(self,id):
        return Articles.get_by_id(id)

    def get_articles_by_author(self,author):
        x=self.get_author_by_name(author)
        return Articles.select().where(Articles.author == x)

    def get_all_articles(self):
        return Articles.select().order_by(Articles.date_time.asc())

    def update_article(self,id,title, body):
        query = Articles.update(title = title,body=body,date_time_edit= strftime('%Y-%m-%d %H:%M:%S')).where(Articles.id==id)
        query.execute()

    def delete_article(self,id):
        Articles.delete_by_id(id)


