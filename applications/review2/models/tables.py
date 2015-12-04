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

db.define_table('boards',
               Field('board_id', required=True),
               Field('name', required=True),
               Field('author_id', db.auth_user, default=auth.user_id),
               Field('created_on','datetime', default=request.now, writable=False),
               )


db.define_table('posts',
               Field('board_id', required=True),
               Field('post_id', required=True),
               Field('post_title'),
               Field('post_description', 'text'),
               Field('author_id', db.auth_user, default=auth.user_id),
               )