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
def get_posts():
    """Return the 10 newest posts."""
    print(flask.request.query_string);
    context = {}
    results = get_n_posts()
    if(len(results) > 10):
        results = results[:-1]
    context['results'] = results
    context['url'] = "/api/v1/p/"
    context['next'] = "" #TODO
    return flask.jsonify(**context)

@insta485.app.route('/api/v1/p/?size=<int:size_url_slug>', methods=["GET"])
def get_posts_size(size_url_slug):
    """Return n newest posts."""
    size = size_url_slug
    context = {}
    results = get_n_posts(size)
    context['next'] = ""
    if(len(results) > size):
        results = results[:-1]
        context["next"] = "/api/v1/p/?size=" + str(size_url_slug) + "&page=1"
    context['url'] = "/api/v1/p/"
    return flask.jsonify(**context)

@insta485.app.route('/api/v1/p/?page=<int:page_url_slug>', methods=["GET"])
def get_posts_page(page_url_slug):
    """Return page n of newest posts."""
    page = page_url_slug
    context = {}
    results = get_n_posts(10, page)
    context['next'] = ""
    if(len(results) > 10):
        results = results[:-1]
        page += 1
        context["next"] = "/api/v1/p/?page=" + str(page)
    context['url'] = "/api/v1/p/"
    return flask.jsonify(**context)

@insta485.app.route('/api/v1/p/?size=<int:size_url_slug>&page=<int:page_url_slug>', methods=["GET"])
def get_posts_page_size(size_url_slug, page_url_slug):
    """Return page p of newest posts with n posts per page."""
    page = page_url_slug
    size = size_url_slug
    context = {}
    results = get_n_posts(size, page)
    context['next'] = ""
    if(len(results) > size):
        results = results[:-1]
        page += 1
        context["next"] = "/api/v1/p/?size=" + str(size) + "&page=" + str(page)
    context['url'] = "/api/v1/p/"
    return flask.jsonify(**context)
