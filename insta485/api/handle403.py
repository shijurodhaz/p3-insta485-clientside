"""Global handler for 403."""
import flask


def handle403(context):
    """Fill context dictionary and return 403."""
    context['status_code'] = 403
    context['message'] = "Forbidden"
    return flask.jsonify(**context), 403
