import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component{
    /* Display comments for one post
    */

    constructor(props) {
        // Initialize mutable state
        super(props);
        this.state = { value: "", comments: [], items: [] };
    }

    componentDidMount() {
        this.setState({
            comments: [
                {
                    "text": "This is practice",
                    "owner": "rodneyss",
                    "owner_show_url": "/u/rodneyss/"
                },
                {
                    "text": "This is another practice",
                    "owner": "vedagupt",
                    "owner_show_url": "/u/vedagupt/"
                }
            ]
        });
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit(event) {
        logname_show_url = "/u/" + this.props.logname + "/";
        updateComment(logname_show_url, this.props.logname, this.state.value);
        event.preventDefault();
    }

    updateComment(owner_show_url, owner, text) {
        this.state.items.push(
            <a href="{owner_show_url}" style="text-decoration:none;color:black">
                <b>{owner}</b>
            </a>
            <div> {text} </div>
        )
    }

    render() {
        //render comments

        this.state.comments.forEach(function(comment) {
            updateComment(comment['owner_show_url'], comment['owner'], comment['text']);
        });

        return (
            {this.state.items}
            <form id="comment-form" onSubmit={this.handleSubmit}>
                <input type="text" value={this.state.value} onChange = {this.handleChange}/>
            </form>
        );
    }
}

expore default Comments;