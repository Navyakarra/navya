### Variables
x = 10
name = "Alice"
is_active = True

### Receiving Input
user_input = input("Enter your name: ")
print("Hello, " + user_input)

### Type Conversion
x = int("10")
y = float("10.5")
z = str(100)

### Strings
text = "Hello, World!"
print(text[0])
print(text[-1])
print(text[0:5])
print(len(text))

### Formatted Strings
name = "John"
age = 25
print(f"My name is {name} and I am {age} years old.")

### String Methods
text = "hello world"
print(text.upper())
print(text.lower())
print(text.title())
print(text.replace("hello", "hi"))
print("world" in text)

### Arithmetic Operations
x = 10
y = 3
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x // y)
print(x % y)
print(x ** y)

### Operator Precedence
result = 10 + 3 * 2
print(result)

### Math Functions
import math
print(math.sqrt(16))
print(math.ceil(4.3))
print(math.floor(4.7))
print(math.pow(2, 3))
print(math.factorial(5))

### If Statements
age = 18
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

### Logical Operators
is_student = True
has_ID = False
if is_student and has_ID:
    print("You get a discount.")
if is_student or has_ID:
    print("You may get a discount.")

### Comparison Operators
x = 10
y = 20
print(x > y)
print(x < y)
print(x == y)
print(x != y)
print(x >= y)
print(x <= y)

### Weight Converter Program
weight = float(input("Enter weight in kg: "))
print("Weight in pounds:", weight * 2.20462)

### While Loops
count = 1
while count <= 5:
    print(count)
    count += 1

### Building a Guessing Game
secret_number = 7
guess = 0
while guess != secret_number:
    guess = int(input("Guess the number: "))
print("You guessed it!")

### Building the Car Game
command = ""
while command.lower() != "quit":
    command = input("> ")
    if command.lower() == "start":
        print("Car started!")
    elif command.lower() == "stop":
        print("Car stopped!")

### For Loops
for i in range(5):
    print(i)

### Nested Loops
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")

### Lists
numbers = [1, 2, 3, 4]
print(numbers[0])
numbers.append(5)
numbers.remove(2)
numbers.sort()
print(numbers)

### 2D Lists
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])

### List Methods
numbers.append(6)
numbers.pop()
numbers.insert(1, 10)
print(numbers)

### Tuples
tuple_example = (1, 2, 3)
print(tuple_example[0])

### Unpacking
x, y, z = (10, 20, 30)
print(x, y, z)

### Dictionaries
person = {"name": "Alice", "age": 25}
print(person["name"])
print(person.get("age"))
person["city"] = "New York"
print(person)

### Emoji Converter
def emoji_converter(text):
    words = text.split()
    emojis = {":)": "😊", ":(": "😞"}
    return " ".join(emojis.get(word, word) for word in words)

message = input("> ")
print(emoji_converter(message))

### Functions
def greet():
    print("Hello!")

greet()

### Parameters
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")

### Keyword Arguments
def greet(name, age):
    print(f"Hello, {name}. You are {age} years old.")

greet(age=25, name="Bob")

### Return Statement
def square(num):
    return num * num

print(square(4))

### Creating a Reusable Function
def multiply(a, b):
    return a * b

print(multiply(3, 4))

### Exceptions
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

### Classes
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name}.")

p = Person("Alice", 25)
p.greet()

### Constructors
class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year

car = Car("Tesla", 2022)
print(car.model)

### Inheritance
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
        print("Bark!")

dog = Dog()
dog.speak()

### Modules
import math
print(math.pi)

### Packages
from datetime import datetime
print(datetime.now())

### Generating Random Values
import random
print(random.randint(1, 10))

### Working with Directories
import os
print(os.getcwd())

### Pypi and Pip
import requests
response = requests.get("https://api.github.com")
print(response.status_code)
