import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component{
    /* Display comments for one post
    */

    constructor(props) {
        // Initialize mutable state
        super(props);
        this.state = { value: "", comments: []};
        this.get_comment_html = this.get_comment_html.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    get_comment_html(items, owner_show_url, owner, text) {
        items.push(
            <div>
                <a href={owner_show_url} style={{"textDecoration":"none", "color":"black"}}>
                    <b>{owner}</b>
                </a>
                <p> {text} </p>
            </div>
        )
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
        event.preventDefault();
    }

    handleSubmit(event) {
        let logname_show_url = "/u/" + this.props.logname + "/";
        let comments = this.state.comments;
        comments.push({"text": this.state.value, "owner": this.props.logname, "owner_show_url": logname_show_url});
        this.setState({comments: comments});
        event.preventDefault();
    }

    render() {
        //render comments
        let items = [];
        let get_comment_html = (items, owner_show_url, owner, text) => {this.get_comment_html(items, owner_show_url, owner, text)}

        this.state.comments.forEach(function(comment) {
            get_comment_html(items, comment['owner_show_url'], comment['owner'], comment['text']);
        });


        return (
            <div>
                <table>
                <tbody>
                {items}
                </tbody>
                </table>
                <form id="comment-form" onSubmit={this.handleSubmit}>
                    <input type="text" value={this.state.value} onChange = {this.handleChange}/>
                    <input type="submit" name="comment" value="comment"/>
                </form>
            </div>
        );
    }
}

export default Comments;
