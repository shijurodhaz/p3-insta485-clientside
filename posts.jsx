import React from 'react';
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
        this.state = { postids: [], next_url: ''};
    }

    componentDidMount(){
        // Call REST API to get posts
        fetch(this.props.url, { credentials: 'same-origin' })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
                return response.json();
        })
        .then((data) => {
            let postids_local = this.state.postids;
            for (var key in data.results) {
                postids_local.push(data.results[key].postid);
            }
            this.setState({
                postids: postids_local,
                next_url: data.next
            });
         })
        .catch(error => console.log(error)); // eslint-disable-line no-console
    }

    fetchData() {
        fetch(this.state.next_url, { credentials: 'same-origin' })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
                return response.json();
        })
        .then((data) => {
            let postids_local = this.state.postids
            for (var key in data.results) {
                postids_local.push(data.results[key].postid)
            }
            this.setState({
                postids: postids_local,
            });
         })
        .catch(error => console.log(error)); // eslint-disable-line no-console
    }; 

    render(){
        return (
            <div>
                <InfiniteScroll
                  dataLength={this.state.postids.length}
                  next={this.fetchData}
                  hasMore={true}
                >
                    {this.state.urls.map((i, index) => (
                        {let url_in = "/api/v1/p/" + i + "/"}
                        <Post url={url_in} logname = {this.props.logname}/>,
                    ))}
                </InfiniteScroll>
            </div>
        );
    }

export default Posts;
