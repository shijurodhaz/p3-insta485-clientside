import React from 'react';
import ReactDOM from 'react-dom';
import Likes from './likes';
import Comments from './comments';
import Post from './post';

//alert('gets here');
let logname = document.getElementById('logname').innerHTML;

ReactDOM.render(
  <Post url="/api/v1/p/1/" logname = {logname}/>,
  document.getElementById('reactEntry'),
);
