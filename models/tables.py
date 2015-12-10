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



#all these tables have id already defined
db.define_table('posts',
                Field('title', 'text'),
                Field('latitude', 'float',default = 36.974117,readable=False, writable=False),
                Field('longitude', 'float',default=-122.030796,readable=False, writable=False),
                Field('body', 'text'),
                Field('category', 'text', readable=False, writable=False),
                Field('user_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
                Field('avg_rate', 'float', default=0, readable=False, writable=False),
                Field('created_on', 'datetime', default=request.now, requires=IS_DATETIME(str(T('%m/%d/%Y %I:%M%p'))), writable=False),
                # searchbar
                format = '%(title)s'
                )

db.posts.id.readable = db.posts.id.writable = False

db.define_table('reviews',
                Field('body','text', label="Review"),
                Field('user_id',db.auth_user,default=auth.user_id, writable=False, readable=False),
                Field('num_stars', requires=IS_IN_SET([1, 2, 3, 4, 5]), label="Rating"),
                Field('post',db.posts, writable=False, readable=False)
                )

db.reviews.id.writable = db.reviews.id.readable = False

db.define_table('uploads',
                Field('username', 'string'),
                Field('post', db.posts),
                Field('filename', represent = lambda x, row: "None" if x == None else x[:45]),
                Field('up_file', 'upload', autodelete=True, uploadseparate=True, requires=IS_NOT_EMPTY()),
                Field('up_date', 'datetime'),
                Field('notes', 'text')
                )




