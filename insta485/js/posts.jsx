import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Posts extends React.Component {
  /* Display all posts on main page
    */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { posts: [], next_url: '/api/v1/p/', next_page: 0 };
    this.fetchData = this.fetchData.bind(this);
  }

  componentDidMount() {
    // Call REST API to get posts
    this.fetchData();
  }

  fetchData() {
    if (window.performance.navigation.type === 2) {
      this.setState({
        posts: window.history.state.posts,
        next_url: window.history.state.next_url,
        next_page: window.history.state.next_page,
      });
      return;
    }
    if (this.state.next_url === '') {
      return;
    }
    fetch(this.state.next_url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const self = this;
        data.results.forEach((result) => {
          self.state.posts.push(result);
        });
        this.setState({
          posts: this.state.posts,
          next_url: data.next,
        });
        window.history.replaceState(this.state, 'sjnvjs', '');
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  render() {
    return (
      <div>
        <InfiniteScroll
          dataLength={this.state.posts.length}
          next={this.fetchData}
          loader={<h4>Loading...</h4>}
          hasMore
        >
          {this.state.posts.map(post => (
            <div key={post.url}>
              <Post url={post.url} logname={this.props.logname} />
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
