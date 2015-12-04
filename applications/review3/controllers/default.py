# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

from datetime import datetime, timedelta
from gluon import utils as gluon_utils
import json
#lists of boards
def index():
    board_id=gluon_utils.web2py_uuid()
    user_id=auth.user_id
    return dict(user_id=user_id)

#hw5
def showboard():
    boards=db().select(db.boards.ALL)
    d= {r.id: {'board_name': r.board_name,
                'board_uid':r.id}
        for r in boards}
    return response.json(dict(board_dict=d))

@auth.requires_login()
@auth.requires_signature()
def add_msg():
    db.boards.update_or_insert((db.boards.id == request.vars.id),
                               board_name=request.vars.msg,
                                board_uid=request.vars.id)
    return "ok"

@auth.requires_login()
@auth.requires_signature()
def createboard():
    db.boards.update_or_insert((db.boards.id == request.vars.id),
                               board_name=request.vars.msg,
                               board_uid=request.vars.id)
    return "okay"


#List of posts
def posts():
    board=db(db.boards.id == request.vars.id).select()
    board_id=request.args(0)
    return dict(board=board,board_id=board_id)


def showposts():
    posts= db().select(db.posts.ALL)
    board_id=request.args(0)
    #posts = db(db.posts).select(board_id=request.args(0))
    d= {r.id: {
               'post_uid':r.id,
                'post_name':r.post_name,
                'post_desc':r.post_desc,
                'post_del':r.post_del,
                'author':auth.user_id,
                'b_id':r.b_id
                }
        for r in posts}
    return response.json(dict(post_dict=d,board_id=board_id))

@auth.requires_login()
@auth.requires_signature()
def add_posts():
    db.posts.update_or_insert((db.posts.id == request.vars.id),
                                post_uid=request.vars.id,
                                post_name=request.vars.post_name,
                                post_desc=request.vars.post_desc,
                                post_del=request.vars.post_del,
                                b_id=request.vars.b_id)
    return "ok"

@auth.requires_login()
@auth.requires_signature()
def createpost():
    db.posts.update_or_insert((db.posts.id == request.vars.id),
                                post_uid=request.vars.id,
                                post_name=request.vars.post_name,
                                post_desc=request.vars.post_desc,
                                post_del=request.vars.post_del,
                                b_id=request.vars.b_id)
    return "okay"


@auth.requires_login()
@auth.requires_signature()
def delete_posts():
    items = request.vars.get('items[]') or request.vars.get('items') or []
    if isinstance(items, (str, unicode)):
        items = [items]
        items = [int(i) for i in items]
        db(db.posts.id.belongs(items)).delete()
    return "ok"

#reset everything
@auth.requires_login()
def reset():
    db(db.boards.id>0).delete()
    db(db.posts.id>0).delete()
    db.boards.truncate()
    db.posts.truncate()
    redirect(URL('default','index'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


