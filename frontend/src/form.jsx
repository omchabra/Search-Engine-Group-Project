import React, { useState } from 'react';
import './form.css'

function Form(props) {

    const [query, setQuery] = useState('')
    const [limit, setLimit] = useState(0)
    const [algo, setAlgo] = useState('')

    //https://search-engine-222.herokuapp.com/search
    const getSearch = (event) => {
        event.preventDefault();
        var URL = "http://localhost:80/search?" + new URLSearchParams({
            query : query,
            limit : limit,
            searchAlgo: algo
        });
        fetch(URL, {
            method : "GET",
        }).then(response => response.json()).then(
            data => {
                console.log(data.results);
                if (algo === "") {
                    let results = data.results
                    props.func2(results);
                } else {
                    try {
                        let results = data.results;
                        props.func(results);    
                    } catch {
                        console.log(data.results);
                        // props.func(data.results);
                    }
                }
            }
        )
        
    }

    const updateQuery = (event) => {
        setQuery(event.target.value);
    }
    const updateLimit = (event) => {
        setLimit(event.target.value);
    }
    const updateAlgo = (event) => {
        setAlgo(event.target.value);
    }

    return (
        <form onSubmit = {getSearch} id = "searchForm">
            <label>
                Query: 
                <input type = "text" value = {query} onChange = {updateQuery} name = "query"    ></input>
            </label>
            <br />
            <label>
                Number of Results: 
                <input type = "number" value = {limit} onChange = {updateLimit} name = "limit"></input>
            </label>
            <br />
            <label>
                Search Algorithm: 
                <select type = "select" value = {algo} onChange = {updateAlgo} name = "algo" form = "searchForm">
                    <option value = "tfidf">TFIDF</option> 
                    <option value = "ratcliff">Ratcliff Ob</option>
                    <option value = "jaccard">Jaccard</option>
                    <option value = "">Run All Three!</option>
                </select>
            </label>
            <br />
            <input type="submit" value = "Submit"></input>
        </form>
    )
}
export default Form;