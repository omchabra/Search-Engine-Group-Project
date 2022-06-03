import React, { useState } from 'react';
import CurrentFiles from './currentFiles';

function File(props) {
    const fileInput = React.createRef();
    const [uploadedState, setUploadedState] = useState("")




    const uploadFiles = (event) => {
        event.preventDefault();
        var formData = new FormData();
        let files = fileInput.current.files
        Object.keys(files).forEach((index) => {
            formData.append(`${files[index].name}`, files[index])
        })
        let URL = "http://localhost:80/uploadDocuments";
        fetch(URL, {
            method : "POST",
            body : formData
        }).then(response => {
            console.log(response.ok)
            if (response.ok) {
                setUploadedState(`Succesfully Uploaded ${files.length} files!`)  
            } else {
                throw response;
            }
        })
    }

    return (
        <form onSubmit = {uploadFiles}>
            <label>
                Upload Files: 
                <input type = "file" ref = {fileInput} multiple></input>
            </label>
            <input type = "submit" value = "Submit"></input>
            <br></br>
            {uploadedState}
        </form>
    )
}

export default File;