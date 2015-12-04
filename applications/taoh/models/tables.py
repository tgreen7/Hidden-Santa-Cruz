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

# This is a table for all users.
db.define_table('people',
    Field('user_id', db.auth_user, default=auth.user_id),
    Field('name', required=True),
    Field('description', 'text'),
    )

db.people.id.readable = False
db.people.user_id.readable = False
db.people.description.represent = lambda v, r: DIV(v, _class="msg_content")


# Table for discussion boards
db.define_table('boards',
                Field('title', 'text', requires=IS_NOT_EMPTY()),
                Field('created_on', 'datetime', writable=False, default=request.now),
                Field('rec_post', 'datetime', writable=False, readable=False)
                )

# Table for posts
db.define_table('posts',
                Field('board_id', db.boards, writable=False, readable=False),
                Field('user_id', 'integer', writable=False, readable=False),
                Field('title', 'text', requires=IS_NOT_EMPTY()),
                Field('body', 'text'),
                Field('created_on', 'datetime', writable=False, default=request.now),
                )
db.posts.id.readable = False

