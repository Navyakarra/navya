const age=20
let sum=200
let totalcount=5

function showtogetlicense(age,bribe,whitestand)
{
    if(!whitestand){
        console.log("you r banned",whitestand)
        return
    }
    if(age<=18 &&bribe>100 || bribe>500)
    {
        console.log("your pass")
    }
    else if(age>18){
        console.log("this person is above 18")
    }else if (bribe<=100){
console.log("this person below 18")
    }
    }
    showtogetlicense(50,300,false)

    const result=1 ===1
    console.log(result)
