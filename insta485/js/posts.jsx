import React from 'react';
import PropTypes from 'prop-types'; 
import ReactDOM from 'react-dom';
import Likes from './likes';
import Comments from './comments';
import Post from './post';
import InfiniteScroll from "react-infinite-scroll-component";

class Posts extends React.Component{
    /* Display all posts on main page
    */

    constructor(props){
        // Initialize mutable state
        super(props);
        this.state = { posts: [], next_url: '/api/v1/p/'};
        this.fetchData = this.fetchData.bind(this);
    }

    componentDidMount(){
        // Call REST API to get posts
        this.fetchData();    
    }

    fetchData() {
        if (this.state.next_url === '') {
            return;
        }
        fetch(this.state.next_url, { credentials: 'same-origin' })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            let self = this;
            data.results.forEach(function(result) {
               console.log(result.url);
               self.state.posts.push(result); 
            });
            this.setState({
                posts: this.state.posts,
                next_url: data.next
            });
         })
        .catch(error => console.log(error)); // eslint-disable-line no-console
    }; 

    render(){
        return (
            <div>
                <InfiniteScroll
                  dataLength={this.state.posts.length}
                  next={this.fetchData}
                  loader={<h4>Loading...</h4>}
                  hasMore={true}>
                  {this.state.posts.map((post) => (
                    <div key={post.url}>
                        <Post url={post.url} logname={this.props.logname}  />
                    </div>
                  ))}
                </InfiniteScroll>
            </div>
        );
    }
}

Posts.propTypes = {                                                                 
  logname: PropTypes.string.isRequired,                                            
};    

export default Posts;
