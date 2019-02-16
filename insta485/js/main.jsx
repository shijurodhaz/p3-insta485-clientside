import React from 'react';
import ReactDOM from 'react-dom';
import Likes from './likes';
import Comments from './comments';
import Post from './post';

logname = document.getElementById('logname').innerHTML
alert(1);

ReactDOM.render(
  <Post url="/api/v1/p/1/" logname = {logname}/>,
  document.getElementById('reactEntry'),
);
