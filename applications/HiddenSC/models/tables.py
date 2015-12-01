#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

from datetime import datetime, timedelta
from gluon.tools import prettydate

# This is a table for all users.
db.define_table('people',
    Field('user_id', db.auth_user, default=auth.user_id),
    Field('name', required=True),
    Field('description', 'text'),
    )

db.people.id.readable = False
db.people.user_id.readable = False
db.people.description.represent = lambda v, r: DIV(v, _class="msg_content")



db.define_table('board',
                Field('title'),
                Field('created_on', 'datetime'),
                )
db.board.created_on.default = datetime.utcnow()
db.board.created_on.readable = db.board.created_on.writable = False
now = datetime.utcnow()
yesterday = now - timedelta(days=1)


#all these tables have id already defined
db.define_table('posts',
                Field('title'),
                Field('body', 'text'),
                Field('board', db.board),
                Field('user_id', 'integer'),
                Field('post_day', 'datetime'),
                Field('user_id_2', db.auth_user, default = auth.user_id),
                Field('image', 'upload'),
                Field('image1', 'upload')
                )
db.define_table('uploads',

    Field('up_file', 'upload', uploadseparate=True, requires=IS_NOT_EMPTY()),
                )


db.posts.board.readable = db.posts.board.writable = False
db.posts.user_id.readable = db.posts.user_id.writable = False
db.posts.user_id_2.readable = db.posts.user_id_2.writable = False
db.posts.post_day.readable = db.posts.post_day.writable = False
db.posts.post_day.default = datetime.utcnow()





