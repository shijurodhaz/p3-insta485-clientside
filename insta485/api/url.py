"""REST API for url."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=["GET"])
def get_url():
    """Return list of services.

    Example:
    {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    """
    context = {}
    if "username" not in flask.session:
        context['message'] = "Forbidden"
        context['status_code'] = 403
        return flask.jsonify(**context), 403
    context["posts"] = "/api/v1/p/"
    context["url"] = "/api/v1/"

    return flask.jsonify(**context)
    
