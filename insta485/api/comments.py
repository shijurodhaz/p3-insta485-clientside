"""REST API for Comments."""
import flask
import insta485


def handle_post(postid):
    """Handle post requests for this endpoint."""
    data = flask.request.get_json()
    if 'text' in data:
        query = '''
        INSERT INTO
            comments(owner, postid, text)
        VALUES(?, ?, ?);
        '''
        insta485.model.query_db(query,
                                (flask.session['username'],
                                 postid,
                                 data['text']))


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
                    methods=['GET', 'POST'])
def get_comments(postid_url_slug):
    """Return a list of comments for this post."""
    context = {}
    if "username" not in flask.session:
        context['message'] = "Forbidden"
        context['status_code'] = 403
        return flask.jsonify(**context), 403
    query = '''
    SELECT * FROM posts WHERE postid=?
    '''
    result = insta485.model.query_db(query, (postid_url_slug,))
    if not result:
        context = {"message": "Not Found", "status_code": 404}
        return flask.jsonify(**context), 404
    status = 200
    post_request = False
    if flask.request.method == 'POST':
        post_request = True
        status = 201
        handle_post(postid_url_slug)
    context['url'] = '/api/v1/p/' + str(postid_url_slug) + '/comments/'
    query = '''
    SELECT commentid, owner, postid, text FROM comments
    WHERE postid=?
    '''
    comments = insta485.model.query_db(query, (postid_url_slug,))
    if post_request:
        comments = [comments[-1]]
    for comment in comments:
        comment['owner_show_url'] = '/u/' + comment['owner'] + '/'
    context['comments'] = comments
    return flask.jsonify(**context), status
