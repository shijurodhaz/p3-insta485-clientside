"""REST API for Comments"""
import flask
import insta485


def handle_post(postid):
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
    """Return a list of comments for this post"""
    post_request = False
    if flask.request.method == 'POST':
        post_request = True
        handle_post(postid_url_slug)
    context = {}
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
    return flask.jsonify(**context)
