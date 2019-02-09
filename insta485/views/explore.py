"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485


def handle_post():
    """Handle post requests."""
    if 'username' not in flask.session:
        return flask.abort(403)
    query = '''
            SELECT *
            FROM  following
            WHERE username1 = ? AND username2 = ?
            '''
    record = insta485.model.query_db(query,
                                     [flask.session['username'],
                                      flask.request.form['username']])
    if 'follow' in flask.request.form:
        if (record or flask.session['username'] ==
                flask.request.form['username']):
            assert len(record) == 1
            return False

        query = '''
        INSERT INTO
        following(username1, username2)
        VALUES(?, ?)
        '''
        insta485.model.query_db(query, [flask.session['username'],
                                        flask.request.form['username']])
    if 'unfollow' in flask.request.form:
        if (not record or flask.session['username'] ==
                flask.request.form['username']):
            return False

        query = "DELETE FROM following WHERE username1=? AND username2=?"
        insta485.model.query_db(query, [flask.session['username'],
                                        flask.request.form['username']])
    return True


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Display explore page."""
    context = {}

    if flask.request.method == 'POST':
        if not handle_post():
            flask.abort(403)

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    context['not_following'] = []
    query = "SELECT username2 FROM  following WHERE username1=?"
    following = insta485.model.query_db(query, [flask.session['username']])
    query = "SELECT username FROM  users"
    all_users = insta485.model.query_db(query, [])
    for user in all_users:
        found = False
        for follow in following:
            if user['username'] == follow['username2']:
                found = True
                break
        if not found:
            if user['username'] != flask.session['username']:
                context['not_following'].append({'username': user['username']})

    context['logname'] = flask.session['username']

    for ind in range(0, len(context['not_following'])):
        not_following_prof = context['not_following'][ind]
        query = "SELECT * FROM  following WHERE username1=? AND username2=?"
        is_following = insta485.model.query_db(query,
                                               [flask.session['username'],
                                                not_following_prof
                                                ['username']])
        if len(is_following) == 1:
            context['not_following'][ind]['logname_follows_username'] = True
        else:
            context['not_following'][ind]['logname_follows_username'] = False

        query = "SELECT filename FROM  users WHERE username=?"
        user_pic = insta485.model.query_db(query,
                                           [not_following_prof['username']])
        user_pic = user_pic[0]['filename']
        context['not_following'][ind]['user_img_url'] = user_pic

    return flask.render_template("explore.html", **context)
