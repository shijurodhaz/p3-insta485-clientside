"""
Insta485 delete (account deletion).

URLs include:
/accounts/delete/
"""
import os
import flask
import insta485


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    if flask.request.method == 'POST':
        query = '''
        SELECT filename FROM users WHERE username = ?
        '''
        user_pic = insta485.model.query_db(query, [flask.session['username']])
        os.remove(os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                               user_pic[0]['filename']))

        query = '''
        SELECT filename FROM posts  WHERE owner = ?
        '''
        user_posts = insta485.model.query_db(query,
                                             [flask.session['username']])

        for post in user_posts:
            os.remove(os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                   post['filename']))

        query = '''
        DELETE FROM users WHERE username = ?
        '''
        insta485.model.query_db(query, [flask.session['username']])
        flask.session.clear()
        return flask.redirect(flask.url_for('show_create'))
    context = {}
    context['logname'] = flask.session['username']
    return flask.render_template("delete.html", **context)
