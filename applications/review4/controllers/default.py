# import logging
# logger = logging.getLogger("web2py.app.start")
# logger.setLevel(logging.DEBUG)

from gluon import utils as gluon_utils


def reset_table():
    """
    This is for testing purposes only and drops the tables
    """
    db.boards.drop()
    db.posts.drop()


def index():
    """Returns a unique id for the board"""
    board_id = gluon_utils.web2py_uuid()
    return dict(board_id=board_id)


@auth.requires_signature()
def add_board():
    """Adds a board to the database"""
    db.boards.update_or_insert((db.boards.board_id == request.vars.board_id),
                               board_id=request.vars.board_id,
                               board_content=request.vars.board_content,
                               author=auth.user_id)
    return "ok"


@auth.requires_signature()
def delete_boards():
    """Removes the board and the posts associated"""
    idlist = request.vars['list[]']
    if type(idlist) is list:
        for identifier in idlist:
            db(db.posts.board_id == identifier).delete()
            db(db.boards.board_id == identifier).delete()
    elif type(idlist) is str:
        db(db.posts.board_id == idlist).delete()
        db(db.boards.board_id == idlist).delete()
    return "ok"


@auth.requires_signature()
def edit_boards():
    """Allows edit of board name"""
    db(db.boards.board_id == request.vars.board_id).update(board_content=request.vars.board_content)
    return "ok"


def load_boards():
    """Loads all boards for the user."""
    rows = db(db.boards.id >= 0).select()
    d = {r.board_id: {'board_content': r.board_content, 'created': r.created, 'posts': r.posts, 'author': r.author}
         for r in rows}
    return response.json(dict(board_dict=d))


def boards():
    """Returns the boards name, id and a unique post id for when the board is clicked on"""
    board_id = request.args(0)
    board = db(db.boards.board_id == board_id).select(db.boards.board_content)
    for row in board:
        board_name = row.board_content
    post_id = gluon_utils.web2py_uuid()
    return dict(board_id=board_id, post_id=post_id, board_name=board_name)


def load_posts():
    """Loads all posts for the user."""
    rows = db(db.posts.board_id == request.vars.board_id).select()
    d = {r.post_id: {'post_content': r.post_content, 'post_description': r.post_description, 'created': r.created,
                     'board_id': r.board_id, 'author': r.author}
         for r in rows}
    logger.error(d)
    return response.json(dict(post_dict=d))


@auth.requires_signature()
def add_post():
    """Adds a post to the database with initial content and description"""
    db.posts.update_or_insert((db.posts.post_id == request.vars.post_id),
                              post_id=request.vars.post_id,
                              post_content=request.vars.post_content,
                              post_description=request.vars.post_description,
                              board_id=request.vars.board_id,
                              author=auth.user_id)
    db(db.boards.board_id == request.vars.board_id).update(posts=db.boards.posts + 1)
    return "ok"


@auth.requires_signature()
def delete_posts():
    """Deletes post form database using the list passed and decrements the # of posts in the board"""
    idlist = request.vars['list[]']
    if type(idlist) is list:
        for identifier in idlist:
            db(db.posts.post_id == identifier).delete()
            db(db.boards.board_id == request.vars.board_id).update(posts=db.boards.posts - 1)
    elif type(idlist) is str:
        db(db.posts.post_id == idlist).delete()
        db(db.boards.board_id == request.vars.board_id).update(posts=db.boards.posts - 1)
    return "ok"


@auth.requires_signature()
def edit_posts():
    """Edit the post name"""
    db(db.posts.post_id == request.vars.post_id).update(post_content=request.vars.post_content)
    return "ok"


@auth.requires_signature()
def edit_postsd():
    """Edit the post description"""
    db(db.posts.post_id == request.vars.post_id).update(post_description=request.vars.post_description)
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


