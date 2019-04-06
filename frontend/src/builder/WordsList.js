import  React, { Component } from  'react';
import  WordsService  from  './WordsService';

const  wordsService  =  new WordsService();

class  WordsList  extends  Component {

    constructor(props) {
        super(props);
        this.state  = {
            words: [],
            nextPageURL:  '',
            user: '',
        };
        this.nextPage  =  this.nextPage.bind(this);
        this.handleDelete  =  this.handleDelete.bind(this);
    }

    componentDidMount() {
        this.state.user = this.props.setUser()
        wordsService.getWords(this.state.user).then(function (result) {
            this.setState({ words:  result.data, nextPageURL:  result.nextlink})
        });
    }

    nextPage() {
        wordsService.getWordsByURL(this.state.user, this.state.nextPageURL).then(function (result) {
            this.setState({ words:  result.data, nextPageURL:  result.nextlink})
        });
    }

    handleDelete(e, pk) {
        wordsService.deleteWord(this.state.user, pk).then( () => {
            var  newArr  =  this.state.words.filter(function(obj) {
                return  obj.pk  !==  pk;
            });
            this.setState({words:  newArr})
        });
    }

    render() {

        return (
        <div  className="words--list">
            <table  className="table">
                <thead  key="thead">
                <tr>
                    <th>#</th>
                    <th>Word</th>
                    <th>Grammar Part</th>
                    <th>Date Created</th>
                </tr>
                </thead>
                <tbody>
                    {this.state.words.map( c  =>
                    <tr  key={c.pk}>
                        <td>{c.pk}  </td>
                        <td>{c.word}</td>
                        <td>{c.grammar_part}</td>
                        <td>{c.date_created}</td>
                        <td>
                        <button  className="btn btn-primary" onClick={(e)=>  this.handleDelete(e, c.pk) }> Delete</button>
                        <a  className="btn btn-primary" href={"/builder/" + c.pk}> Update</a>
                        </td>
                    </tr>)}
                </tbody>
            </table>
            <button  className="btn btn-primary"  onClick=  {  this.nextPage  }>Next</button>
        </div>
        );
    }
}

export  default  WordsList;

