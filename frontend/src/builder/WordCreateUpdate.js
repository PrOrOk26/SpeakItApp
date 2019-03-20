import React, { Component } from 'react';
import WordsService from './WordsService';

const wordsService = new WordsService();

class WordCreateUpdate extends Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
      }

      componentDidMount() {
        const { match: { params } } = this.props;
        if(params && params.pk)
        {
            wordsService.getWord(params.user, params.pk).then((c)=> {
            this.refs.word.value = c.word;
            this.refs.grammar_part.value = c.grammar_part;
            this.refs.date_created.value = c.date_created;
          })
        }
      }

      handleCreate() {
        wordsService.createWord( this.props.user, 
          {
            "word": this.refs.word.value,
            "grammar_part": this.refs.grammar_part.value,
            "date_created": this.refs.date_created.value,
          }          
        ).then((result) => {
          alert("Word created!");
        }).catch(() => {
          alert('There was an error! Please re-check your form.');
        });
      }

      handleUpdate(pk) {
        wordsService.updateWord(this.props.user, 
            {
              "word": this.refs.word.value,
              "grammar_part": this.refs.grammar_part.value,
              "date_created": this.refs.date_created.value,
            }           
        ).then((result)=>{
          console.log(result);
          alert("Word updated!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }

      handleSubmit(event) {
        const { match: { params } } = this.props;

        if(params && params.pk){
          this.handleUpdate(params.pk);
        }
        else
        {
          this.handleCreate();
        }

        event.preventDefault();
      }

      render() {
        return (
          <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <label>
              Word:</label>
              <input className="form-control" type="text" ref='word' />

            <label>
              Grammar Part:</label>
              <input className="form-control" type="text" ref='grammarpart'/>

            <label>
              Date Created:</label>
              <input className="form-control" type="text" ref='datecreated' />

            <input className="btn btn-primary" type="submit" value="Submit" />
            </div>
          </form>
        );
      }  
}

export default WordCreateUpdate;