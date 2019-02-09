"""
Insta485 image tool.

URLs include:
/uploads/<img_name>.<ext>
"""
from flask import send_from_directory, abort
import insta485


@insta485.app.route('/uploads/<img_url>', methods=['GET', 'POST'])
def show_image(img_url):
    """Display images."""
    try:
        return send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                   img_url)
    except FileNotFoundError:
        abort(404)
        return ""
