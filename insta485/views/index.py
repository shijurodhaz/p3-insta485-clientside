"""
Insta485 index (main) view.

URLs include:
/
"""
import sqlite3
from operator import itemgetter
import flask
import arrow
import insta485


@insta485.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    context = {}
    posts = []
    context['posts'] = posts

    if flask.request.method == 'POST':

        # Abort if the username is not logged in
        if 'username' not in flask.session:
            return flask.abort(403)
        if 'unlike' in flask.request.form:
            query = '''
            DELETE
            FROM
                likes
            WHERE owner = ? AND postid = ?;
            '''
            insta485.model.query_db(query,
                                    (flask.session['username'],
                                     flask.request.form['postid'],))

        if 'like' in flask.request.form:
            try:
                query = '''
                INSERT INTO
                    likes(owner, postid)
                VALUES(?, ?);
                '''
                insta485.model.query_db(query,
                                        (flask.session['username'],
                                         flask.request.form['postid'],))
            except sqlite3.IntegrityError:
                return flask.abort(403)
        if 'comment' in flask.request.form:
            query = '''
            INSERT INTO
                comments(owner, postid, text)
            VALUES(?, ?, ?);
            '''
            insta485.model.query_db(query, (flask.session['username'],
                                            flask.request.form['postid'],
                                            flask.request.form['text']))
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    context['logname'] = flask.session['username']
    query = '''
    SELECT
    following.username2 AS owner,
    users.filename AS owner_img_url,
    posts.*
    FROM following
    INNER JOIN posts ON following.username1 = ? AND
    following.username2 = posts.owner
    INNER JOIN users ON following.username2 = users.username
    ORDER BY created DESC;
    '''
    following_posts = insta485.model.query_db(query,
                                              (flask.session['username'],))
    query = '''
    SELECT users.username AS owner, users.filename AS owner_img_url, posts.*
    FROM posts
    INNER JOIN users ON posts.owner = users.username AND users.username = ?;
    '''

    user_posts = insta485.model.query_db(query, (flask.session['username'],))

    posts += following_posts + user_posts

    posts.sort(key=itemgetter('postid'), reverse=True)

    for post in posts:
        post['img_url'] = post['filename']
        post['timestamp'] = arrow.get(post['created']).humanize()
        query = '''
        SELECT *
        FROM likes
        WHERE postid = ?
        '''
        likes = insta485.model.query_db(query, (post['postid'],))
        post['likes'] = len(likes)
        for like in likes:
            if like['owner'] == flask.session['username']:
                post['liked'] = True
                break
        query = '''
        SELECT *
        FROM comments
        WHERE postid = ?
        '''
        comments = insta485.model.query_db(query, (post['postid'],))
        post['comments'] = comments

    return flask.render_template("index.html", **context)
