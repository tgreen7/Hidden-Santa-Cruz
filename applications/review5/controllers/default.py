# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time

@auth.requires_login()
def index():
    #db.board.insert(board_title='Cricket', board_id=gluon_utils.web2py_uuid())
    draft_id = gluon_utils.web2py_uuid()
    return dict(draft_id=draft_id)

@auth.requires_signature()
def add_board():
    db.board.insert(board_title="")
    rows = db(db.board).select()
    d = {r.id: {'board_title': r.board_title,
                'editing': r.editing,
                'is_draft': r.is_draft,
                'boardID': r.id}
         for r in rows}
    return response.json(dict(board_dict=d))



def set_edit():
    board=db(db.board.boardID==request.args(0))
    board.update(editing=True)
    rows = db(db.board).select()
    d = {r.id: {'board_title': r.board_title,
                'editing': r.editing,
                'is_draft': r.is_draft,
                'boardID': r.id}
         for r in rows}
    return dict(board_dict=d)

def open_board():
    #db.posts.insert(title="", body="")
    boardID = request.args(0)
    return dict(boardID=boardID)

@auth.requires_signature()
def load_boards():
    """Loads all boards."""
    rows = db(db.board).select()
    d = {r.id: {'board_title': r.board_title,
                'editing': r.editing,
                'is_draft': r.is_draft,
                'boardID': r.id}
         for r in rows}
    return response.json(dict(board_dict=d))

@auth.requires_signature()
def load_posts():
    """Loads all posts for a board."""
    #posts=db(db.posts.boardID==request.vars.boardID).select(db.posts.ALL)
    #db.posts.insert(title='Cricketers', body="this is a test post")
    posts=db(db.posts.boardID==request.vars.boardID).select(db.posts.ALL)
    d = {r.id: {'post_title': r.title,
                'body': r.body,
                'post_id': r.id
                }
         for r in posts}
    return response.json(dict(post_dict=d))

@auth.requires_signature()
def add_post():
    db.posts.insert(title="", body="", boardID=request.vars.boardID)
    posts=db(db.posts.boardID==request.vars.boardID).select(db.posts.ALL)
    d = {r.id: {'post_title': r.title,
                'body': r.body,
                'post_id': r.id}
         for r in posts}
    return response.json(dict(post_dict=d))


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


