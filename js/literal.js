let name = "Navya";
let age = 21;
let num1 = 10;
let num2 = 20;

let greeting = `Hello, my name is ${name} and I am ${age} years old.`;
let sum = `The sum of ${num1} and ${num2} is ${num1 + num2}.`;

let multilineStr = `This is a
multiline string
using template literals.`;

function upperCase(strings, ...values) {
  let result = strings.reduce((acc, str, i) => {
    return acc + str + (values[i] ? values[i].toUpperCase() : '');
  }, '');
  return result;
}

let taggedGreeting = upperCase`Hello, ${name}!`;

let escapedStr = `This is how you escape a backtick: \`\``;
let dollarSignStr = `The price is \$100.`;

console.log(greeting);
console.log(sum);
console.log(multilineStr);
console.log(taggedGreeting);
console.log(escapedStr);
console.log(dollarSignStr);
