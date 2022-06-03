import React, { useState } from 'react';
import Form from './form'

function Result(props) {
    const [data, setData] = useState({})
    const [threeData, setThreeData] = useState({})

    const updateResult = (data) => {
        setData(data);
    }

    const updateThreeData = (data) => {
        setThreeData(data)
    }

    const table = Object.keys(data).map((result) => {
        let jsString = `<tr><th scope = 'rowgroup' colspan = '3'>${result}</th></tr>`
        data[result].map((t) => {
            jsString += `<tr><td className =${'id' + t[0]}>${t[0]}</td><td>${t[1]}</td></tr>`
        })
        console.log(jsString)
        return (jsString)
    })

    const threeTables = Object.keys(threeData).map((result) => {
        console.log("here");
        let jsString = `<table><thead><tr><th scope = 'rowgroup' colspan = '3'>${result}</th></tr><tr><th>Doc Id</th><th>Confidence</th></tr></thead><tbody>`
        Object.keys(threeData[result]).map((searchAlgo) => {
            jsString += `<tr><th scope = 'rowgroup' colspan = '3'>${searchAlgo}</th></tr>`
            threeData[result][searchAlgo].map((t) => {
                jsString += `<tr><td className = ${'id' + t[0]}>${t[0]}</td><td>${t[1]}</td></tr>`
            })
        })
        jsString += `</tbody></table>`
        return jsString;
    })

    // function parseObj(obj) {
    //     Object.keys(obj).map((result) => {
    //         let jsString = `<tr>`
    //     })
    // }

    return (
        <div>
            <Form func = {updateResult} func2 = {updateThreeData}/>
            {
                table && table.length > 0 && (
                <table>
                    <thead>
                        <tr>
                            <th>Doc Id</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody dangerouslySetInnerHTML={{__html: table}}></tbody>
                </table>
                )
            } 
            {
                threeTables && threeTables.length > 0 && (
                    <div dangerouslySetInnerHTML={{__html: threeTables}}></div>
                )
            }
        </div>

    )

}
export default Result;