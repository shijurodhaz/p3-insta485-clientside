import React from 'react';
import PropTypes from 'prop-types';

class Post extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            comments: [],
            age: "",
            img_url: "",
            owner: "",
            owner_img_url: "",
            post_show_url: "",
            url: ""
        };
    }
}

