import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component{
    /* Display comments for one post
    */

    constructor(props) {
        // Initialize mutable state
        super(props);
        this.state = { value: "", comments: [], items: []};
        this.add_comment = this.add_comment.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    

    componentDidMount() {
        this.state.comments = [
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
        ];
        let items = this.state.items;
        let comments = this.state.comments;
        let self = this;

        comments.forEach(function(comment) {
            console.log("Adding comment");
            self.add_comment(comment);
        });
        this.setState({
            comments: comments,
            items: items    
        });
    }

    add_comment(comment) {
        this.state.comments.push(comment);
        this.state.items.push(
            <div>
                <a href={comment.owner_show_url} style={{"textDecoration":"none", "color":"black"}}>
                    <b>{comment.owner}</b>
                </a>
                &nbsp; {comment.text}
            </div>
        )
    }

    handleChange(event) {
        this.setState({value: event.target.value});
        event.preventDefault();
    }

    handleSubmit(event) {
        let logname_show_url = "/u/" + this.props.logname + "/";
        let comment = {
            text: this.state.value,
            owner: this.props.logname,
            owner_show_url: logname_show_url
        };
        this.add_comment(comment);
        this.state.value = "";

        let comments = this.state.comments;
        let items = this.state.items;
        this.setState({comments: comments, items: items});
        event.preventDefault();
    }

    render() {
        //render comments
        return (
            <div>
                <table>
                <tbody>
                {this.state.items}
                </tbody>
                </table>
                <form id="comment-form" onSubmit={this.handleSubmit}>
                    <input type="text" value={this.state.value} onChange = {this.handleChange}/>
                </form>
            </div>
        );
    }
}

export default Comments;
