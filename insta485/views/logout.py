"""
Insta485 logout view (no page though).

URLs include:
/accounts/logout/
"""
import flask
import insta485


@insta485.app.route('/accounts/logout/', methods=['GET', 'POST'])
def show_logout():
    """Display logout page."""
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))
