"""
Insta485 followers view.

URLs include:
/u/<user_url_slug>/followers/
"""
import flask
import insta485


@insta485.app.route('/u/<user_url_slug>/followers/', methods=['GET', 'POST'])
def show_followers(user_url_slug):
    """Display followers page."""
    context = {}

    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            return flask.abort(403)
        query = "SELECT *  FROM  following WHERE username1=? AND username2=?"
        record = insta485.model.query_db(query, [flask.session['username'],
                                                 flask.request.form
                                                 ['username']])
        if 'follow' in flask.request.form:
            if (record or flask.session['username'] ==
                    flask.request.form['username']):
                assert len(record) == 1
                return flask.abort(403)

            query = "INSERT INTO following(username2, username1) VALUES(?, ?)"
            insta485.model.query_db(query, [flask.request.form['username'],
                                            flask.session['username']])

        if 'unfollow' in flask.request.form:
            if (not record or flask.session['username'] ==
                    flask.request.form['username']):
                return flask.abort(403)

            query = "DELETE FROM following WHERE username1=? AND username2=?"
            insta485.model.query_db(query, [flask.session['username'],
                                            flask.request.form['username']])

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    query = "SELECT username1 FROM  following WHERE username2=?"
    context['followers'] = insta485.model.query_db(query, [user_url_slug])
    context['logname'] = flask.session['username']
    for ind in range(0, len(context['followers'])):
        query = "SELECT * FROM  following WHERE username1=? AND username2=?"
        follower = context['followers'][ind]
        is_follower = insta485.model.query_db(query,
                                              [flask.session['username'],
                                               follower['username1']])
        if len(is_follower) == 1:
            context['followers'][ind]['logname_follows_username'] = True
        else:
            context['followers'][ind]['logname_follows_username'] = False
        context['followers'][ind]['username'] = \
            context['followers'][ind]['username1']

        query = "SELECT filename FROM  users WHERE username=?"
        user_pic_q = insta485.model.query_db(query, [follower['username']])
        user_pic = user_pic_q[0]['filename']
        context['followers'][ind]['user_img_url'] = user_pic

    return flask.render_template("followers.html", **context)
