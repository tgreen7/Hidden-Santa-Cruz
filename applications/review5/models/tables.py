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

db.define_table('board',
             Field('board_title', 'string'),
             Field('editing', 'boolean', default=False),
             Field('is_draft', 'boolean', default=False),
             Field('board_id', 'string') # To uniquely identify drafts and messages.
            )

db.define_table('posts',
              Field('title','string'),
              Field('body','text'),
              Field('boardID', 'string'))
