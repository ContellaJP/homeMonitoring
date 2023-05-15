import './App.css';
import React, { useState, useEffect } from 'react';

export default function App() {
    const [data, setData] = useState([]);
    useEffect(() => {
        getData();
    }, []);
    function getData() {
        fetch('http://127.0.0.1:5000/weatherWidgetData')
         .then(response => response.json())
         .then(data => {
            setData(data);
         })
         .catch(error => console.error(error));
     }
     return (
        <div>
            <h1>Header 1</h1>
            {data.high}
        </div>
    );
}

// export default App;