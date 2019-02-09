"""
Insta485 logo tool.

URLs include:
/images/logo.png
"""

import flask
import insta485


@insta485.app.route('/images/logo.png', methods=['GET', 'POST'])
def show_logo():
    """Display logo."""
    return flask.send_from_directory(insta485.app.config['STATIC_FOLDER'],
                                     'images/logo.png')
