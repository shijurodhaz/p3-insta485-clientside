import React from 'react';
import PropTypes from 'prop-types';
import Likes from './likes';
import Comments from './comments';

class Post extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            age: "",
            img_url: "",
            owner: "",
            owner_img_url: "",
            owner_show_url: "",
            post_show_url: ""
        };
    }

    componentDidMount() {
        this.setState({
            "age": "2017-09-28 04:33:28",
            "img_url": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
            "owner": "awdeorio",
            "owner_img_url": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
            "owner_show_url": "/u/awdeorio/",
            "post_show_url": "/p/3/"
        });
    }

    render() {
        return(
             <div style={{width:'60%', border: '1px solid black', margin: '0px auto'}}>                 
                <table style={{width:'100%', margin: '0px auto', padding:'30px'}}>                       
                  <tr>                                                                         
                    <td style={{width:'50px'}}>                                                    
                      <a href={this.state.owner_show_url} style={{'textDecoration':'none', color:'black'}}>
                        <img src={this.state.owner_img_url} style={{height:'50px', width:'50px', 'float':'left'}} alt="image" />
                      </a>                                                                     
                    </td>                                                                      
                    <td style={{'fontSize':'20px'}}>                                                
                      <a href={this.state.owner_show_url} style={{'textDecoration':'none', color:'black'}}>
                        <b>{this.state.owner}</b>                                             
                      </a>                                                                     
                    </td>                                                                      
                    <td style={{'fontSize':'20px', 'textAlign':'right'}}>                               
                      <a href={this.state.post_show_url} style={{'textDecoration':'none', color:'black'}}>{this.state.age}</a>
                    </td>                                                                      
                  </tr>                                                                        
                                                                                               
                </table>                                                                       
                <img src={this.state.img_url} alt="image" style={{width:'100%'}} />
                                                                                               
                <div style={{'marginLeft':'10px'}}> 
                    <Likes url={this.props.url + 'likes/'} logname={this.props.logname}  />
                </div>                                                              

                <div style={{'marginLeft':'10px'}}>
                    <Comments url={this.props.url + 'comments/'} logname={this.props.logname}  />
                </div>
                        {alert("gets here")}
            </div>
        )
    }

}
export default Post;
