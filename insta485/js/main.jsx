import React from 'react';
import ReactDOM from 'react-dom';
import Posts from './posts';

// alert('gets here');
const logname = document.getElementById('logname').innerHTML;

ReactDOM.render(
  <Posts logname={logname} />,
  document.getElementById('reactFeedEntry'),
);
