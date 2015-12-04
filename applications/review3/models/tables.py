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
from datetime import datetime
db.define_table('boards',
                Field('board_name',requires=IS_NOT_EMPTY()),
                Field('counterb'),
                Field('board_uid'),
                Field('modified','datetime',default=datetime.utcnow))

db.define_table('posts',
                Field('author','reference auth_user',default=auth.user_id),
                Field('auth_name'),
                Field('post_uid'),
                Field('b_id'),
                Field('b','reference boards'),
                Field('dayt','boolean'),
                Field('post_name'),
                Field('post_desc'),
                Field('post_del'),
                Field('phone',requires = IS_MATCH('(\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',
                        error_message='e.g. 123-456-7890')),
                Field('modified_on','datetime',default=datetime.utcnow),
                Field('date_display','datetime'))

db.posts.phone.label="Phone Number"
db.boards.counterb.readable = db.boards.counterb.writable = False
db.boards.modified.readable = db.boards.modified.writable = False
db.posts.auth_name.readable = db.posts.auth_name.writable = False
db.posts.dayt.readable = db.posts.dayt.writable = False
db.posts.author.readable = db.posts.author.writable = False
db.posts.modified_on.writable= db.posts.modified_on.readable=False
db.posts.date_display.writable =db.posts.date_display.readable= False
db.posts.id.readable = db.posts.id.writable = False