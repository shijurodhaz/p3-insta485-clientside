"""
Insta485 user (user details).

URLs include:
/u/<user_url_slug>
"""
import os
import sqlite3
import flask
import insta485


def return_403():
    """Return 403."""
    return flask.abort(403)


def handle_post(postid_slug):
    """Handle POST requests."""
    file_deleted = False
    if 'username' not in flask.session:
        return False, file_deleted
    if 'uncomment' in flask.request.form:
        commentid = flask.request.form['commentid']
        query = "SELECT * FROM comments WHERE owner=? AND commentid=? "
        results = insta485.model.query_db(query,
                                          (flask.session['username'],
                                           commentid))
        if not results:
            return False, file_deleted

        assert len(results) == 1
        query = "DELETE  FROM comments WHERE owner=? AND commentid=? "
        insta485.model.query_db(query,
                                (flask.session['username'], commentid))

    if 'delete' in flask.request.form:
        postid = flask.request.form['postid']

        query = "SELECT * FROM posts WHERE owner=? AND postid=? "
        results = insta485.model.query_db(query,
                                          (flask.session['username'],
                                           postid))
        if not results or not postid == postid_slug:
            return False, file_deleted
        assert len(results) == 1
        filename = results[0]['filename']
        file_path = os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                 filename)
        os.remove(file_path)
        query = "DELETE  FROM posts WHERE owner=? AND postid=? "
        insta485.model.query_db(query,
                                (flask.session['username'], postid))
        file_deleted = True

    postid = postid_slug

    if 'like' in flask.request.form:
        try:
            query = '''
            INSERT INTO
                likes(owner, postid)
            VALUES(?, ?);
            '''
            insta485.model.query_db(query,
                                    (flask.session['username'], postid,))
        except sqlite3.IntegrityError:
            return False, file_deleted

    if 'unlike' in flask.request.form:
        query = '''
        DELETE
        FROM
            likes
        WHERE owner = ? AND postid = ?;
        '''
        insta485.model.query_db(query, (flask.session['username'],
                                        postid,))
    if 'comment' in flask.request.form:
        if not flask.request.form['postid'] == postid:
            return False, file_deleted
        query = '''
        INSERT INTO
            comments(owner, postid, text)
        VALUES(?, ?, ?);
        '''
        insta485.model.query_db(query,
                                (flask.session['username'],
                                 flask.request.form['postid'],
                                 flask.request.form['text']))
    return True, file_deleted


@insta485.app.route('/p/<postid_slug>/', methods=['GET', 'POST'])
def show_post(postid_slug):
    """Display / route."""
    if flask.request.method == 'POST':
        no_error, file_deleted = handle_post(postid_slug)
        if not no_error:
            return_403()
        if file_deleted:
            return flask.redirect(flask.url_for('show_index'))

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    query = '''
            SELECT
            owner,
            postid,
            filename AS img_url
            FROM posts WHERE postid=?
            '''
    context = insta485.model.query_db(query, (postid_slug,))[0]
    if context['owner'] == flask.session['username']:
        context['own_post'] = True
    else:
        context['own_post'] = False

    context['logname'] = flask.session['username']

    query = "SELECT filename AS owner_img_url FROM users  WHERE username=?"
    user_info = insta485.model.query_db(query, (context['owner'],))

    context['owner_img_url'] = user_info[0]['owner_img_url']

    query = "SELECT *  FROM likes  WHERE postid=?"
    like_info = insta485.model.query_db(query, (postid_slug,))

    context['likes'] = len(like_info)
    context['liked'] = False

    for like_row in like_info:
        if like_row['owner'] == flask.session['username']:
            context['liked'] = True

    query = "SELECT *  FROM comments  WHERE postid=?"
    comments = insta485.model.query_db(query, (postid_slug,))

    context['comments'] = comments

    for comment in comments:
        if comment['owner'] == flask.session['username']:
            comment['own_comment'] = True
        else:
            comment['own_comment'] = False

    return flask.render_template("post.html", **context)
