import React from 'react';
import ReactDOM from 'react-dom';
import Likes from './likes';
import Comments from './comments';
import Post from './post';
import Posts from './posts';

//alert('gets here');
let logname = document.getElementById('logname').innerHTML;

ReactDOM.render(
  <Posts logname={logname}  />,
  document.getElementById('reactFeedEntry'),
);
