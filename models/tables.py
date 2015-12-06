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
                Field('created_on', 'datetime', default=request.now, writable=False, readable=False),
                )


#all these tables have id already defined
db.define_table('posts',
                Field('title', 'text'),
                Field('body', 'text'),
                Field('board', db.board, writable=False, readable=False),
                Field('user_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
                Field('created_on', 'datetime', default=request.now, writable=False),
                # searchbar
                format = '%(title)s'
                )
db.posts.id.readable = db.posts.id.writable = False

db.define_table('reviews',
                Field('body','text', label="Review"),
                Field('user_id',db.auth_user,default=auth.user_id, writable=False, readable=False),
                Field('num_stars', 'integer', label="Rating (0-5)", requires=IS_INT_IN_RANGE(0,6)),
                Field('post',db.posts, writable=False, readable=False)
                )

db.reviews.id.writable = db.reviews.id.readable = False

db.define_table('uploads',
                Field('username', 'string'),
                Field('post', db.posts),
                Field('filename', represent = lambda x, row: "None" if x == None else x[:45]),
                Field('up_file', 'upload', uploadseparate=True, requires=IS_NOT_EMPTY()),
                Field('up_date', 'datetime'),
                Field('notes', 'text')
                )




