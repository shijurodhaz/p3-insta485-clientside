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
        this.state = { posts: [], items: [], next_url: '/api/v1/p/'};
        this.fetchData = this.fetchData.bind(this);
    }

    componentDidMount(){
        // Call REST API to get posts
        this.fetchData();    
    }

    fetchData() {
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
               self.state.items.push(
               <div key={result.url}>
                    <Post  url={result.url} logname={self.props.logname} />
                    <br />
               </div>
               );
            });
            this.setState({
                posts: this.state.posts,
                items: this.state.items,
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
                  endMessage={
                    <p>End of posts</p>
                  }
                  hasMore={true}>
                  {this.state.items}                      
                </InfiniteScroll>
            </div>
        );
    }
}

Posts.propTypes = {                                                                 
  logname: PropTypes.string.isRequired,                                            
};    

export default Posts;
