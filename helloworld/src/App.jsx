import React from "react";
import Custom from "./Custom.jsx";
console.log("hello" && "html")
let age=20
function App(){

    function buttonClickfn(){
        console.log("i was pressed")
    }
    return<div>
        <h1> hello world{2+2}</h1>
        <button onClick={buttonClickfn}>clickme</button>
  <Custom name={age**2} greetingMessage="hola"/>
    </div>
}
export default App