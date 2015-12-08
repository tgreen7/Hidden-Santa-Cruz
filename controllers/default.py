# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def deleteposts():
    db(db.posts.id > 0).delete()
    db(db.uploads.id > 0).delete()

def deletereviews():
    db(db.reviews.id>0).delete()

def map():
    return dict(postlist = [])

def index():
    return dict(board_list = [])

def show_boards():
    return dict()

# search posts
def post_selector():
    if not request.vars.keyword: return ''

    post_title = []
    rows = db(db.posts).select()
    for row in rows:
       post_title.append(str(row.title))

    print post_title

    #query = db.posts.title.contains(request.vars.keyword)
    #posts = db(query).select(orderby=db.posts.title)
    post_start = request.vars.keyword.lower()
    selected = [m for m in post_title if (post_start) in m.lower()]
    return DIV(*[DIV(k,
                     _onclick="jQuery('#keyword').val('%s')" % k,
                     _onmouseover="this.style.backgroundColor='#c2c2d6',"
                                  "this.style.cursor='pointer'",
                     _onmouseout="this.style.backgroundColor='white'",
                     ) for k in selected],
               _class="search_list"
               )


def load_posts_rating():
    post_category = request.args(0)
    # print post_board_id
    posts = db(db.posts.category == post_category).select(orderby=~db.posts.avg_rate)

    star_dict = {}
    anti_star_dict = {}
    half_star_dict = {}

    for post in posts:
        if (post.avg_rate - int(post.avg_rate)) >= 0.5:
            half_star_dict[post.id] = True
            anti_star_dict[post.id] = range(0, int(4 - int(post.avg_rate)))
        else:
            anti_star_dict[post.id] = range(0, int(5 - int(post.avg_rate)))
            half_star_dict[post.id] = False

        star_dict[post.id] = range(0, int(post.avg_rate))

    return response.json(dict(post_list=posts.as_list(), star_dict=star_dict, anti_star_dict=anti_star_dict, half_star_dict=half_star_dict))

def load_posts_recent():
    category = request.args(0)
    # print post_board_id
    posts = db(db.posts.category == category).select(orderby=~db.posts.created_on)

    star_dict = {}
    anti_star_dict = {}
    half_star_dict = {}

    for post in posts:
        if (post.avg_rate - int(post.avg_rate)) >= 0.5:
            half_star_dict[post.id] = True
            anti_star_dict[post.id] = range(0, int(4 - int(post.avg_rate)))
        else:
            anti_star_dict[post.id] = range(0, int(5 - int(post.avg_rate)))
            half_star_dict[post.id] = False

        star_dict[post.id] = range(0, int(post.avg_rate))


    return response.json(dict(post_list=posts.as_list(), star_dict=star_dict, anti_star_dict=anti_star_dict, half_star_dict=half_star_dict))

def show_posts():
    post_category = request.args(0)

    post_list = db(db.posts.category == post_category).select()

    for post in post_list:
        # update the average review
        count = db(db.reviews.post == post.id).count()
        if count == 0:
            break

        reviews = db(db.reviews.post == post.id).select()
        total = 0

        for i in reviews:
            total += i.num_stars
        dub = float('%.2f' % (total / float(count)))
        db.posts(post.id).update_record(avg_rate=dub)

    post_list = db(db.posts.category == post_category).select(orderby=~db.posts.avg_rate)
    return dict(post_list=post_list, post_category=post_category)

@auth.requires_login()
def add_posts():
    logger.info("My session is: %r" % session)
    form = SQLFORM(db.posts)

    category = request.args(0)

    form.vars.category = category
    form.vars.user_id = auth.user_id

    if form.process().accepted:
        session.flash = T('the data was inserted')
        redirect(URL('default','show_posts', args=[category])) #might change to index
    return dict(form=form)

@auth.requires_login()
def posts_edit():
    posts = db.posts(request.args(0))
    if(auth.user_id != posts.user_id):
         redirect(URL('default', 'show_posts', args=[posts.category]))
         session.flash = T('Not permitted for this user')
    else:
        form = SQLFORM(db.posts, record=posts, upload = URL('download'))
        if form.process().accepted:
            session.flash = T('The data was edited')
            redirect(URL('default', 'show_posts', args=[posts.category]))
        return dict(form=form)

#delete post
@auth.requires_login()
def delete_post():
    post = db.posts(request.args(0))
    if (auth.user_id != post.user_id):
        redirect(URL('default', 'show_posts', args=request.args(1)))
        session.flash = T('Not permitted for this user')

    else:
        db(db.posts.id == post).delete()
        redirect(URL('default','show_posts', args=request.args(1)))


def post_page():
    post_id = request.args(0)
    board = db.posts(post_id).category
    post = db.posts[post_id]
    title = post.title
    body = post.body
    reviews = db(db.reviews.post == post_id).select()
    num_rev = db(db.reviews.post == post_id).count()
    # print "numrev" + str(num_rev)

    images = db(db.uploads.post == post_id).select()
    return dict(post = post, reviews=reviews, num_rev=num_rev, title=title, body= body, images = images, board=board)

# upload images
def upload_images():
    import datetime
    form = FORM(LABEL("File(s):"), INPUT(_name='up_files', _type='file', _multiple='', requires=IS_NOT_EMPTY()),  BR(),INPUT(_type='submit'))
    if form.accepts(request.vars, formname="form"):
        files = request.vars['up_files']
        if not isinstance(files, list):
            files = [files]
        for f in files:
            print f.filename
            up_file = db.uploads.up_file.store(f, f.filename)
            i = db.uploads.insert(notes=request.vars.notes, up_file=up_file, filename=f.filename, post = request.args(0), up_date= datetime.datetime.now())
            db.commit()
        redirect(URL('post_page',args=request.args(0)))
    return dict(form=form)

@auth.requires_login()
def add_review():
    form = SQLFORM(db.reviews)
    form.vars.post = request.args(0)
    form.vars.user_id = auth.user_id
    if form.process().accepted:
        session.flash = T('the data was inserted')
        redirect(URL('default','post_page', args=request.args(0)))
    return dict(form=form)


def load_reviews():
    post_board_id = request.args(0)
    rows = db(db.reviews.post == post_board_id).select()

    def get_name(user_id):
        test = db(db.auth_user.id == user_id).select()
        firstname = ""
        lastname = ""
        for i in test:
            firstname = i.first_name
            lastname =  i.last_name
        return firstname + " " + lastname

    d = {r.id: {'body': r.body,
                'user_id': r.user_id,
                'user': get_name(r.user_id),
                'num_stars':r.num_stars,
                'star_list': range(0,r.num_stars),
                'anti_star_list': range(0, 5-r.num_stars),
                'post_id':r.post
                }

         for r in rows}
    return response.json(dict(review_dict=d))

@auth.requires_login()
def delete_review():
    rev_id = request.vars.get("rev_id")
    db(db.reviews.id == rev_id).delete()
    redirect(URL('default', 'post_page', args= request.vars.get("post")))


@auth.requires_login()
def edit_review():
    rev_id = request.args(0)
    post_id = request.args(1)
    user_id = request.args(2)


    if int(auth.user_id) != int(user_id):
        session.flash = T('Not permitted for this user')
        redirect(URL('default', 'post_page', args=[post_id]))

    form = SQLFORM(db.reviews, record=rev_id)

    if form.process().accepted:
        session.flash = T('The data was edited')
        redirect(URL('default', 'post_page', args=[post_id]))
    return dict(form=form)


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



