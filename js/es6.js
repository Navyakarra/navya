
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

let doubledArr = arr.map(x => x * 2);
console.log("Doubled Array:", doubledArr);

let evenArr = arr.filter(x => x % 2 === 0);
console.log("Even Numbers:", evenArr);

let sum = arr.reduce((acc, curr) => acc + curr, 0);
console.log("Sum of Array:", sum);

arr.forEach(x => console.log("Element:", x));