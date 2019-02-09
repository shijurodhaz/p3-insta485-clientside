"""
Insta485 following view.

URLs include:
/u/<user_url_slug>/following/
"""
import flask
import insta485


@insta485.app.route('/u/<user_url_slug>/following/', methods=['GET', 'POST'])
def show_following(user_url_slug):
    """Display following page."""
    context = {}

    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            return flask.abort(403)
        query = "SELECT *  FROM  following WHERE username2=? AND username1=?"
        record = insta485.model.query_db(query, [flask.request.form
                                                 ['username'],
                                                 flask.session['username']])
        if 'follow' in flask.request.form:
            if (record or flask.session['username'] ==
                    flask.request.form['username']):
                return flask.abort(403)

            query = "INSERT INTO following(username1, username2) VALUES(?, ?)"
            insta485.model.query_db(query, [flask.session['username'],
                                            flask.request.form['username']])

        if 'unfollow' in flask.request.form:
            if (not record or flask.session['username'] ==
                    flask.request.form['username']):
                return flask.abort(403)

            query = "DELETE FROM following WHERE username2=? AND username1=?"
            insta485.model.query_db(query, [flask.request.form['username'],
                                            flask.session['username']])

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    query = "SELECT username2 FROM  following WHERE username1=?"
    context['following'] = insta485.model.query_db(query, [user_url_slug])
    context['logname'] = flask.session['username']
    for ind in range(0, len(context['following'])):
        following = context['following'][ind]
        query = "SELECT * FROM  following WHERE username1=? AND username2=?"
        is_following = insta485.model.query_db(query,
                                               [flask.session['username'],
                                                following['username2']])
        if len(is_following) == 1:
            context['following'][ind]['logname_follows_username'] = True
        else:
            context['following'][ind]['logname_follows_username'] = False
        context['following'][ind]['username'] = following['username2']

        query = "SELECT filename FROM  users WHERE username=?"
        user_pic_q = insta485.model.query_db(query, [following['username']])
        user_pic = user_pic_q[0]['filename']
        context['following'][ind]['user_img_url'] = user_pic

    return flask.render_template("following.html", **context)
