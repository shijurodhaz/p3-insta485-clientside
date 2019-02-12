"""REST API for posts."""                                                          
import flask                                                                       
import insta485                                                                    
    
                                                                               
def get_n_posts(size=10, page=0):
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
    WHERE posts.owner = ?;       
 

    ORDER BY postid  DESC;                                                         
    LIMIT ? OFFSET ?
    '''                                                                            
    results = insta485.model.query_db(query,                               
                                      (flask.session['username'],
                                       flask.session['username'],
                                       size, offset))        
        
    url = '/api/v1/p/'                                                                           
    for result in results:
        result['url'] =  url + result['postid'] + '/'                                                                                    
    
                                                                                   
@insta485.app.route('/api/v1/p/', methods=["GET"])  
def get_posts():                                                    
    """Return the 10 newest posts
    #TODO  
