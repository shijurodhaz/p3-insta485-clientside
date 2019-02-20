import React from 'react';
import PropTypes from 'prop-types';
import Likes from './likes';
import Comments from './comments';

// TODO: Humanize timestamp

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      age: '',
      img_url: '',
      owner: '',
      owner_img_url: '',
      owner_show_url: '',
      post_show_url: '',
    };
  }

  componentDidMount() {
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          age: data.age,
          img_url: data.img_url,
          owner: data.owner,
          owner_img_url: data.owner_img_url,
          owner_show_url: data.owner_show_url,
          post_show_url: data.post_show_url,
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console 
  }

  render() {
    return (
      <div style={{ width: '60%', border: '1px solid black', margin: '0px auto' }}>
        <table style={{ width: '100%', margin: '0px auto', padding: '30px' }}>
          <tbody>
            <tr>
              <td style={{ width: '50px' }}>
                <a href={this.state.owner_show_url} style={{ textDecoration: 'none', color: 'black' }}>
                  <img src={this.state.owner_img_url} style={{ height: '50px', width: '50px', float: 'left' }} alt="User" />
                </a>
              </td>
              <td style={{ fontSize: '20px' }}>
                <a href={this.state.owner_show_url} style={{ textDecoration: 'none', color: 'black' }}>
                  <b>{this.state.owner}</b>
                </a>
              </td>
              <td style={{ fontSize: '20px', textAlign: 'right' }}>
                <a href={this.state.post_show_url} style={{ textDecoration: 'none', color: 'black' }}>{this.state.age}</a>
              </td>
            </tr>
          </tbody>
        </table>
        <img src={this.state.img_url} style={{ width: '100%' }} alt="post" />

        <div >
          <Likes url={`${this.props.url}likes/`} logname={this.props.logname} />
        </div>

        <div style={{ marginLeft: '10px' }}>
          <Comments url={`${this.props.url}comments/`} logname={this.props.logname} />
        </div>
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
  logname: PropTypes.string.isRequired,
};

export default Post;
