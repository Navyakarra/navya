import React,{use, useEffect, useState} from "react";
// import Custom from "./Custom";
function App1(){
    const[counter,setCounter]=useState(0)
    useEffect(()=>{
    console.log('i ran',counter)
},[counter])
    function increase(){
        setCounter(oldCounterValue => oldCounterValue +1)

    }
    function decrease(){
        setCounter(oldCounterValue => oldCounterValue -1)
}
return<div>
    <h1> Counter:{counter}</h1>
    <button onClick={increase}>increase the counter</button>
    <button onClick={decrease}>increase the counter</button>
</div>

}
export default App1
