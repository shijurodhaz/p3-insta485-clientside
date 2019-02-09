"""
Insta485 login view.

URLs include:
/accounts/login/
"""
import hashlib
import flask
import insta485


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display login page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    if flask.request.method == 'POST':
        user_password = insta485.model.query_db('SELECT password FROM users \
            WHERE username = ?', [flask.request.form['username']])
        if not user_password:
            return ''' <b> Wrong Login Credentials. \
                Please go back and try again </b> '''
        salt_list = user_password[0]['password'].split('$')
        hashed_pass = salt_list[2]
        algorithm = 'sha512'
        salt = salt_list[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + flask.request.form['password']
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        if password_hash == hashed_pass:
            flask.session['username'] = flask.request.form['username']
            return flask.redirect(flask.url_for('show_index'))
        return ''' <b> Wrong Login Credentials. \
                Please go back and try again </b> '''
    context = {}
    context['logname'] = ''
    return flask.render_template("login.html", **context)
