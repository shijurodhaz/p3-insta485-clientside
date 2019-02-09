"""
Insta485 password view.

URLs include:
/accounts/password/
"""
import uuid
import hashlib
import flask
import insta485


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Display password page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    if flask.request.method == 'POST':
        user_password = insta485.model.query_db('SELECT password FROM users \
                                                WHERE username = ?',
                                                [flask.session['username']])
        salt_list = user_password[0]['password'].split('$')
        salt = salt_list[1]
        hashed_pass = salt_list[2]
        algorithm_sha = 'sha512'
        hash_object = hashlib.new(algorithm_sha)
        password_salted = salt + flask.request.form['password']
        hash_object.update(password_salted.encode('utf-8'))
        password_hash = hash_object.hexdigest()
        if password_hash == hashed_pass:
            if (flask.request.form['new_password1'] ==
                    flask.request.form['new_password2']):
                algorithm_sha = 'sha512'
                salt = uuid.uuid4().hex
                hash_object = hashlib.new(algorithm_sha)
                password_salted = salt + flask.request.form['new_password1']
                hash_object.update(password_salted.encode('utf-8'))
                password_hash = hash_object.hexdigest()
                password_db_string = "$".join([algorithm_sha, salt,
                                               password_hash])
                insta485.model.query_db('UPDATE users SET password = ? \
                                        WHERE username = ?',
                                        [password_db_string,
                                         flask.session['username']])
                return flask.redirect(flask.url_for('show_edit'))
            flask.abort(401)
        flask.abort(403)
    context = {}
    context['logname'] = flask.session['username']
    return flask.render_template("password.html", **context)
