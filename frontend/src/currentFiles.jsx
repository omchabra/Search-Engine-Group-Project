import React, {useState} from 'react';
const { useEffect } = React;


function CurrentFiles(props) {

    const [listOfFiles, setListOfFiles] = useState([])

    const getFiles = () => {
        let url = "http://localhost:80/currentFiles"
        fetch(url, {
            method : "GET"
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response;
            }
        }).then(data => {
            setListOfFiles(data.response)
        }).catch(err => {
            console.log("ERror: ", err);
        })
    }

    const files = listOfFiles.map((file) => {
        return (
            <p>{file}</p>
        )
    })

    useEffect(() => {
        getFiles()
    }, [])

    return (
        <div>
            {
                files && files.length > 0 && (
                    <span>
                        <h1>Current Files Stored: ({files.length}) </h1>
                        <span>
                            {files}
                        </span>
                    </span>
                )
            }
        </div>
    )
}

export default CurrentFiles