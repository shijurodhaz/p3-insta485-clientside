"""REST API for posts."""
import flask
import insta485


def get_n_posts(size=10, page=0):
    """Helper function to get posts from size and page."""
    offset = page * size
    query = '''
    SELECT
    posts.postid AS postid
    FROM following
    INNER JOIN posts ON following.username1 = ? AND
    following.username2 = posts.owner

    UNION

    SELECT posts.postid AS postid
    FROM posts
    WHERE posts.owner = ?

    ORDER BY postid  DESC
    LIMIT ? OFFSET ?
    '''                                                                            
    results = insta485.model.query_db(query,
                                      (flask.session['username'],
                                       flask.session['username'],
                                       size + 1, offset))
        
    url = '/api/v1/p/'
    for result in results:
        result['url'] =  url + str(result['postid']) + '/'

    return results
                                                                                   
@insta485.app.route('/api/v1/p/', methods=["GET"])
def get_multiple_posts():
    """Return the n newest posts on page p."""
    context = {}
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    if size < 0 or page < 0:
        context['message'] = "Bad Request"
        context['status_code'] = 400
        return flask.jsonify(**context), 400
    results = get_n_posts(size, page)
    context['next'] = ""
    if(len(results) > size):
        results = results[:-1]
        page += 1
        context["next"] = "/api/v1/p/?size=" + str(size) + "&page=" + str(page)
    context['results'] = results
    context['url'] = "/api/v1/p/"
    return flask.jsonify(**context)
