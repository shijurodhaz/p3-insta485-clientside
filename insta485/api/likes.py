"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["GET", "DELETE", "POST"])
def get_likes(postid_url_slug):
    """Show and change likes on postid.

    Example:
    {
      "logname_likes_this": 1,
      "likes_count": 3,
      "postid": 1,
      "url": "/api/v1/p/1/likes/"
    }
    """
    context = {}
    # TODO
    if "username" not in flask.session:
        context['message'] = "Forbidden"
        context['status_code'] = 403
        return flask.jsonify(**context), 403

    postid = postid_url_slug
    logname = flask.session["username"]

    if flask.request.method == 'GET':
        # url
        context["url"] = flask.request.path

        # Post
        context["postid"] = postid

        # Did this user like this post?
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT EXISTS( "
            "  SELECT 1 FROM likes "
            "    WHERE postid = ? "
            "    AND owner = ? "
            "    LIMIT 1"
            ") AS logname_likes_this ",
            (postid, logname)
        )
        logname_likes_this = cur.fetchone()
        context.update(logname_likes_this)

        # Likes
        cur = connection.execute(
            "SELECT COUNT(*) AS likes_count FROM likes WHERE postid = ? ",
            (postid,)
        )
        likes_count = cur.fetchone()
        context.update(likes_count)

        return flask.jsonify(**context), 200

    if flask.request.method == "DELETE":
        query = '''
        DELETE
        FROM likes
        WHERE postid = ?
        AND owner = ?;
        '''
        insta485.model.query_db(query,
                                (postid, logname,))
        return flask.jsonify(**context), 204

    if flask.request.method == "POST":
        query = '''
        SELECT *
        FROM likes
        WHERE owner = ?
        AND postid = ?;
        '''

        results = insta485.model.query_db(query, (logname, postid,))

        if results:
            context['logname'] = logname
            context['message'] = "Conflict"
            context['postid'] = postid
            context['status_code'] = 409
            return flask.jsonify(**context), 409

        query = '''
        INSERT INTO likes(owner, postid)
        VALUES(?, ?);
        '''
        insta485.model.query_db(query,
                                (logname, postid,))
        context['logname'] = logname
        context['postid'] = postid
        return flask.jsonify(**context), 201

    context['message'] = "Bad Request"
    context['status_code'] = 400
    return flask.jsonify(**context), 400
