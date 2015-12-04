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

# Here is a table for boards and posts
from datetime import datetime
db.define_table('boards',
                Field('board_content', 'text'),
                Field('board_id'),
                Field('posts', 'integer', default='0'),
                Field('created', 'datetime', default=datetime.utcnow()),
                Field('author', db.auth_user, default=auth.user_id),
)

db.define_table('posts',
                Field('post_content', 'text'),
                Field('post_description', 'text'),
                Field('board_id'),
                Field('post_id'),
                Field('created', 'datetime', default=datetime.utcnow()),
                Field('author', db.auth_user, default=auth.user_id)
)
