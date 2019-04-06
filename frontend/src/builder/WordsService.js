import axios from 'axios';
const BUILDER_URL = 'http://localhost:8000';

export default class WordsService{

    constructor(){}


    getWords(user) {
        const url = `${BUILDER_URL}/{user.username}/builder/`;
        return axios.get(url).then(response => response.data);
    }  
    getWordsByURL(user, link) {
        const url = `${BUILDER_URL}/{user.username}/builder/{link}$`;
        return axios.get(url).then(response => response.data);
    }
    getWord(user, pk) {
        const url = `${BUILDER_URL}/{user.username}/builder/{pk}$`;
        return axios.get(url).then(response => response.data);
    }
    deleteWord(user, pk){
        const url = `${BUILDER_URL}/{user.username}/builder/{pk}$`;
        return axios.delete(url);
    }
    createWord(user, word){
        const url = `${BUILDER_URL}/{user.username}/builder/{pk}$`;
        return axios.post(url, word);
    }
    updateWord(user, word){
        const url = `${BUILDER_URL}/{user.username}/builder/{pk}$`;
        return axios.put(url, word);
    }
}