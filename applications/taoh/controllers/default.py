# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#import datetime and date
from datetime import datetime
from datetime import date
from datetime import timedelta

def index():
    """
    Allows a person to register in the system, if they are not registered already.
    """
    # If the person is registered, we store the person id in session.person_id.
    db.people.name.label = "What's your name?"
    logger.info("Session: %r" % session)
    row = db(db.people.user_id == auth.user_id).select().first()
    db.people.user_id.readable = db.people.user_id.writable = False
    form = SQLFORM(db.people, record=row)
    if form.process().accepted:
        session.flash = "Welcome, %s!" % form.vars.name
        redirect(URL('default', 'people'))
    return dict(form=form)

#delete boards
# def reset():
#   db(db.boards.id > 0).delete()

def test():
    """
    Allows a person to register in the system, if they are not registered already.
    """
    # If the person is registered, we store the person id in session.person_id.
    db.people.name.label = "What's your name?"
    logger.info("Session: %r" % session)
    row = db(db.people.user_id == auth.user_id).select().first()
    db.people.user_id.readable = db.people.user_id.writable = False
    form = SQLFORM(db.people, record=row)
    if form.process().accepted:
        session.flash = "Welcome, %s!" % form.vars.name
        redirect(URL('default', 'people'))
    return dict(form=form)

#delete posts
def reset_posts():
    db(db.people.id > 0).delete()
    db(db.posts.id > 0).delete()

def show_boards():
    board_list = db(db.boards).select(limitby=(0,20), orderby=~db.boards.rec_post)
    board_post_array = []
    yesterday = datetime.utcnow() - timedelta(days=1)
    for board in board_list:
        print board.rec_post
        count = db((db.posts.board_id==board.id) & (db.posts.created_on > yesterday)).count()
        board_post_array.append(count)
    return dict(board_list=board_list, board_post_array = board_post_array)

def show_posts():
    board_id_of_post = request.args(0)
    post_list = db(db.posts.board_id==board_id_of_post).select(limitby=(0,20), orderby=~db.posts.created_on)
    return dict(post_list=post_list, board_id_of_post=board_id_of_post)

@auth.requires_login()
def create_board():
    form=SQLFORM(db.boards)
    if form.process().accepted:
        session.flash = T('The data was inserted')
        redirect(URL('show_boards'))
    return dict(form=form)

@auth.requires_login()
def delete_post():
    post = db.posts(request.args(0))
    if post.user_id != auth.user_id:
        session.flash = T('Incorrect User')
        redirect(URL('default','show_posts', args = [request.args(1)]))
    db(db.posts.id == request.args(0)).delete()
    redirect(URL('default','show_posts', args = [request.args(1)]))

@auth.requires_login()
def edit_post():
    post = db.posts(request.args(0))
    if post is None:
        session.flash = T('Post doesn\'t exist')
        redirect(URL('default', 'show_posts'))
    if post.user_id != auth.user_id:
        session.flash = T('Incorrect User')
        redirect(URL('default', 'show_posts', args=[post.board_id]))
    form = SQLFORM(db.posts, record=post)
    if form.process().accepted:
        session.flash = T('The data was edited')
        redirect(URL('default', 'show_posts', args=[post.board_id]))
    return dict(form=form)


@auth.requires_login()
def create_post():
    form=SQLFORM(db.posts)
    form.vars.board_id = request.args(0)
    form.vars.user_id = auth.user_id
    if form.process().accepted:
        session.flash = T('The data was inserted')
        board = db.boards(request.args(0))
        board.update_record (rec_post = request.now)
        redirect(URL('show_posts', args=request.args(0)))
    return dict(form=form)


def store_message(form):
    form.vars.msg_id = str(db2.textblob.insert(mytext = form.vars.msg_id))


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


