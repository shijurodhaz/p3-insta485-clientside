import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component {
  /* Display comments for one post
    */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { value: '', comments: [], items: [] };
    this.addComment = this.addComment.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }


  componentDidMount() {
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const comments = data.comments;
        const self = this;
        comments.forEach((comment) => {
          self.addComment(comment);
        });
        this.setState({
          comments: this.state.comments,
          items: this.state.items,
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console       
  }

  addComment(comment) {
    this.state.comments.push(comment);
    this.state.items.push(
      <div>
        <a href={comment.owner_show_url} style={{ textDecoration: 'none', color: 'black' }}>
          <b>{comment.owner}</b>
        </a>
        {`  ${comment.text}`}
      </div>,
    );
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
    event.preventDefault();
  }

  handleSubmit(event) {
    const lognameShowUrl = `/u/${this.props.logname}/`;
    const comment = {
      text: this.state.value,
      owner: this.props.logname,
      owner_show_url: lognameShowUrl,
    };
    fetch(this.props.url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(comment),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json;
      })
      .catch(error => console.log(error));

    this.addComment(comment);
    this.state.value = '';

    const comments = this.state.comments;
    const items = this.state.items;
    this.setState({ comments, items });
    event.preventDefault();
  }

  render() {
    // render comments
    return (
      <div>
        <table>
          <tbody>
            {this.state.items}
          </tbody>
        </table>
        <form id="comment-form" onSubmit={this.handleSubmit}>
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </form>
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
  logname: PropTypes.string.isRequired,
};

export default Comments;
