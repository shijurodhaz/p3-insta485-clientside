"""
Insta485 create view.

URLs include:
/accounts/create/
"""
import uuid
import hashlib
import flask
import insta485


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Display create page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_edit'))

    if flask.request.method == 'POST':
        query = '''
        SELECT * FROM users WHERE username = ?
        '''
        user = insta485.model.query_db(query, [flask.request.form['username']])

        if user:
            flask.abort(409)

        if flask.request.form['password'] == '':
            flask.abort(400)

        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + flask.request.form['password']
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        filename = insta485.model.save_file(flask.request.files['file'])
        query = '''
        INSERT INTO users (username,fullname,email,filename,password)
        VALUES (?, ?, ?, ?, ?)
        '''
        insta485.model.query_db(query, [flask.request.form['username'],
                                        flask.request.form['fullname'],
                                        flask.request.form['email'],
                                        filename, password_db_string])

        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for('show_index'))

    context = {}
    context['logname'] = ''
    return flask.render_template("create.html", **context)
