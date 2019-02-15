"""REST API for to show a post."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/', methods=["GET"])
def get_post(postid_url_slug):
    """Return likes on postid.

    Example:
    {
        "age": "2017-09-28 04:33:28",
        "img_url": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
        "owner": "awdeorio",
        "owner_img_url":
            "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "owner_show_url": "/u/awdeorio/",
        "post_show_url": "/p/3/",
        "url": "/api/v1/p/3/"
    }
    """
    context = {}

    if "username" not in flask.session:
        context['message'] = "Forbidden"
        context['status_code'] = 403
        return flask.jsonify(**context), 403

    # url
    context["url"] = flask.request.path

    # Post
    postid = postid_url_slug

    query = '''
    SELECT *
    FROM posts
    WHERE postid = ?;
    '''
    results = insta485.model.query_db(query, (postid,))
    if not results:
        context['message'] = "Not Found"
        context['status_code'] = 404
        return flask.jsonify(**context), 404

    context['age'] = results[0]['created']
    context['img_url'] = "/uploads/" + results[0]['filename']
    context['owner'] = results[0]['owner']
    context['post_show_url'] = "/p/" + str(postid) + "/"
    context['owner_show_url'] = "/u/" + results[0]['owner'] + "/"

    query = '''
    SELECT filename
    FROM users
    WHERE username = ?;
    '''
    user_prof = insta485.model.query_db(query, (results[0]['owner'],))
    context['owner_img_url'] = "/uploads/" + user_prof[0]['filename']

    return flask.jsonify(**context)
