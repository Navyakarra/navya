import React ,{use, useEffect, useState} from "react";
import {BrowserRouter as Router,Route,Link} from 'react-router-dom'
import './App.css'
// import Custom from "./Custom.jsx";
// console.log("hello" && "html")
// let age=20
// function App(){

//     function buttonClickfn(){
//         console.log("i was pressed")
//     }
//     return<div>
//         <h1> hello world{2+2}</h1>
//         <button onClick={buttonClickfn}>clickme</button>
//   <Custom name={age**2} greetingMessage="hola"/>
//     </div>
// }


// usestate useeffect
// function App(){
//     const[counter,setCounter]=useState(0)
//     useEffect(()=>{
//     console.log('i ran',counter)
// },[counter])
//     function increase(){
//         setCounter(oldCounterValue => oldCounterValue +1)

//     }
//     function decrease(){
//         setCounter(oldCounterValue => oldCounterValue -1)
// }
// return<div>
//     <h1> Counter:{counter}</h1>
//     <button onClick={increase}>increase the counter</button>
//     <button onClick={decrease}>decrease the counter</button>
// </div>
// }
// export default App

// todoapp
// function App(){
//     const[task,setTask]=useState("")
//     const[todos,setTodos]=useState([
//         "nav","web"
//     ])
// function createTodo(event){
//     event.preventDefault()
//     setTodos(oldTodos =>{
//         setTask('')
//         return[...oldTodos,task]

//     })
// }
// return <div>
//     <h1> best to do app ever</h1>
//  <form onSubmit={createTodo}>
//     <input
//      type="text"
//       value={task} 
//       nChange={event =>{
//         setTask(event.target.value)
//     }}
//     />
//     <button type="submit">create todo</button>
//     </form>
//     <ul>
//         {todos.map((todo,index )=>{
//             return<li key={index}>{todo}</li>
//         })}
//     </ul>
// </div>
//     }
// export default App

// // reacterrouterdom
// function App(){
//     return(
//         <BrowserRouter>
//         <div>
//         <nav>
//         <ul>
//         <li>
//         <Link to ="/hello world">go to website</Link>
//         </li>
//         <li>
//         <Link to ="/ ">go to web</Link>
//         </li>
//         </ul>
//         </nav>
//         <Route path="/hello world"exact>
//         <h1>hello</h1>
//         </Route>
//         <Route path="/"exact>
//         <h1>hello web</h1>
//         </Route>
//         </div>
//         </BrowserRouter>
//     )
// }
// export default App
// dynamicroutes
import User from "./user";
import users from "./users.json";

const App = () => {
  return (
    <Router>
      <div>
        <h1>Users List</h1>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              <Link to={`/user/${user.id}`}>{user.name}</Link>
            </li>
          ))}
        </ul>

        <Route>
          <Route path="/user/:id" element={<User />} />
        </Route>
      </div>
    </Router>
  );
};

export default App;