import React,{useState} from 'react';
import logo from './logo.svg';
import './App.css';
import { useQuery } from '@tanstack/react-query';

function Button(){
  const{data,error}=useQuery('hello-world',()=>{
return new Promise(resolve=>{
  setTimeout(()=>resolve(Math.random()),2000)
})
  })
  console.log({data,error})
  return <button >i am button{data}</button>
}
 
  function App() {
    const[visible,setVisible]=useState(true)
    function toggleButton(){
      setVisible(visible=>visible)
    }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
