"""
Insta485 user (user details).

URLs include:
/u/<user_url_slug>
"""
import flask
import insta485


def handle_post(user_url_slug):
    """Handle POST requests."""
    if 'username' not in flask.session:
        return False

    query = "SELECT *  FROM  following WHERE username1=? AND username2=?"
    record = insta485.model.query_db(query,
                                     (flask.session['username'],
                                      user_url_slug))

    if 'follow' in flask.request.form:
        if (record or flask.session['username'] == user_url_slug) or\
                (not flask.request.form['username'] == user_url_slug):
            return False

        query = "INSERT INTO following(username1, username2) VALUES(?, ?)"
        insta485.model.query_db(query, (flask.session['username'],
                                        user_url_slug))

    if 'unfollow' in flask.request.form:
        if (not record or flask.session['username'] == user_url_slug) or\
                (not flask.request.form['username'] == user_url_slug):
            return False

        query = "DELETE FROM following WHERE username1=? AND username2=?"
        insta485.model.query_db(query, (flask.session['username'],
                                        user_url_slug))

    if 'create_post' in flask.request.form:
        if not flask.session['username'] == user_url_slug:
            return False

        # Protect against idiots trying to upload no file
        if 'file' in flask.request.files:
            file_in = flask.request.files['file']
            filename = insta485.model.save_file(file_in)
            query = "INSERT INTO posts(filename, owner) VALUES(?, ?)"
            insta485.model.query_db(query, (filename, user_url_slug))
    return True


@insta485.app.route('/u/<user_url_slug>/', methods=['GET', 'POST'])
def show_user(user_url_slug):
    """Display / route."""
    context = {}
    if flask.request.method == 'POST':
        if not handle_post(user_url_slug):
            return flask.abort(403)
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    context['username'] = user_url_slug
    context['logname'] = flask.session['username']

    query = "SELECT username2 FROM  following WHERE username1=?"
    context['following'] = len(insta485.model.query_db(query,
                                                       (user_url_slug, )))

    query = "SELECT username1 FROM  following WHERE username2=?"
    context['followers'] = len(insta485.model.query_db(query,
                                                       (user_url_slug, )))
    # Empty string if the user page is that of the logged in
    if user_url_slug == flask.session['username']:
        context['own_page'] = True
        context['following_status'] = ''
    else:
        context['own_page'] = False

        query = "SELECT username2 FROM  following WHERE username1=?"
        people_following = insta485.model.query_db(query,
                                                   (flask.session['username'],
                                                    ))

        following = False

        for row in people_following:
            if row['username2'] == user_url_slug:
                following = True
                break

        if following:
            context['user_follows'] = True
            context['following_status'] = 'following'
        else:
            context['user_follows'] = False
            context['following_status'] = 'not following'

    query = "SELECT fullname FROM users  WHERE username=?"
    user_details = insta485.model.query_db(query, (user_url_slug, ))
    context['fullname'] = user_details[0]['fullname']

    query = "SELECT postid, filename AS img_url FROM posts  WHERE owner=?"
    posts = insta485.model.query_db(query, (user_url_slug, ))

    context['posts'] = posts
    context['total_posts'] = len(posts)

    return flask.render_template("user.html", **context)
