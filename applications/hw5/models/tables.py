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
                Field('author', db.auth_user, default=auth.user_id),
                Field('title', 'text'),
                Field('created_on', 'datetime'),
                Field('message_id'), # To uniquely identify drafts and messages.
                Field('is_draft', 'boolean', default=False),

                )


db.define_table('post',
             Field('author', db.auth_user, default=auth.user_id),
             Field('message_content', 'text'),
             Field('is_draft', 'boolean', default=False),
             Field('message_id'), # To uniquely identify drafts and messages.
             Field('editing', 'boolean',default=False)
            )

db.define_table('posts',
             Field('author', db.auth_user, default=auth.user_id),
             Field('title', 'text'),
             Field('body', 'text'),
             Field('is_draft', 'boolean', default=False),
             Field('marked', 'boolean', default=False),
             Field('message_id'), # To uniquely identify drafts and messages.
             Field('editing', 'boolean',default=False),
             Field('editingBody', 'boolean',default=False),
             Field('post', 'integer')
            )




now = db.board.created_on.default = datetime.utcnow()
yesterday = now - timedelta(days=1)







