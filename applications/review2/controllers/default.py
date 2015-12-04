# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon import utils as gluon_utils
import json
import time

import logging
logger = logging.getLogger("web2py.app.HW5")
logger.setLevel(logging.DEBUG)

@auth.requires_login()
def index():
    draft_id = gluon_utils.web2py_uuid()
    return dict(draft_id=draft_id)

@auth.requires_signature()
def load_boards():
    """Loads all messages for the user."""

    rows = db().select(db.boards.ALL, orderby=db.boards.id)
    d = {r.board_id: {'board_name': r.name,'can_edit': ((True) if (r.author_id == auth.user_id) else False)}
        for r in rows}
    return response.json(dict(board_dict=d))

@auth.requires_signature()
def new_board():
    db.boards.insert(board_id=request.vars.board_id,name=request.vars.name)
    return "ok"

@auth.requires_signature()
def update_board():

    row = db(db.boards.board_id == request.vars.board_id).select().first()
    logger.info("row: %r", row)
    row.update_record(name=request.vars.name)
    return "ok"




@auth.requires_login()
def show_posts():
    board_id = request.args(0)
    board = db(db.boards.board_id==board_id).select()
    board_title = ""
    for result in board:
        board_title = result.name
    return dict(title=board_title,board_id=board_id)

@auth.requires_signature()
def load_posts():
    rows = db(db.posts.board_id == request.vars.board_id).select()
    d = {r.post_id: {'board_id': r.board_id,
                     'post_id' : r.post_id,
                     'post_title': r.post_title,
                     'post_description': r.post_description,
                     'can_edit': ((True) if (r.author_id == auth.user_id) else False)}
        for r in rows}
    return response.json(dict(posts_dict=d))

@auth.requires_signature()
def new_post():
    db.posts.insert(board_id=request.vars.board_id,post_id=request.vars.post_id)
    return "ok"

@auth.requires_signature()
def update_post():
    row = db(db.posts.post_id == request.vars.post_id).select().first()
    logger.info("row: %r", row)
    row.update_record(post_title=request.vars.new_title,post_description=request.vars.new_description)
    return "ok"

@auth.requires_signature()
def delete_posts():
    posts_raw = request.vars.delete_targs
    posts = json.loads(posts_raw)
    for post_id in posts:
        post_id_request = post_id
        entry = db(db.posts.post_id == post_id_request)
        entry.delete()

    return "ok"




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


