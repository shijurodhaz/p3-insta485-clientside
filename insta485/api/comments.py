"""REST API for Comments"""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/comments/', 
                    methods=['GET'])
def get_comments(postid_url_slug):
    """Return a list of comments for this post"""
    context = {}
    context['url'] = '/api/v1/p/' + str(postid_url_slug) + '/comments/'
    query = '''
    SELECT commentid, owner, postid, text FROM comments
    WHERE postid=?
    '''
    comments = insta485.model.query_db(query, (postid_url_slug,))
    for comment in comments:
        comment['owner_show_url'] = '/u/' + comment['owner'] + '/'
    context['comments'] = comments
    return flask.jsonify(**context)
