"""
Insta485 edit view.

URLs include:
/accounts/edit/
"""
import os
import flask
import insta485


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def show_edit():
    """Display edit page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    if flask.request.method == 'POST':
        if not('file' not in flask.request.files or
               flask.request.files['file'].filename == ''):
            query = '''
            SELECT filename FROM users WHERE username = ?
            '''
            prev_file = insta485.model.query_db(query,
                                                [flask.session['username']])

            file = insta485.model.save_file(flask.request.files['file'])
            query = '''
            UPDATE users SET filename = ? WHERE username = ?
            '''
            insta485.model.query_db(query, [file, flask.session['username']])

            os.remove(os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                   prev_file[0]['filename']))
        query = '''
        UPDATE users SET fullname = ?, email = ? WHERE username = ?
        '''
        insta485.model.query_db(query, [flask.request.form['fullname'],
                                        flask.request.form['email'],
                                        flask.session['username']])

    query = '''
    SELECT fullname,email,filename FROM users WHERE username = ?
    '''
    user_info = insta485.model.query_db(query, [flask.session['username']])
    context = {}
    context['logname'] = flask.session['username']
    context['name'] = user_info[0]['fullname']
    context['email'] = user_info[0]['email']
    context['file'] = user_info[0]['filename']
    return flask.render_template("edit.html", **context)
