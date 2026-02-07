// auto refresh
// setTimeout(() => {
//     //location.reload(true);
//     window.location.reload();
// }, 3000);

// functions 
function reload() {             // reload current page
  window.location.reload(true); // true forces server reload 
}

let gohome;

function stop_home() {
  clearTimeout(gohome);
}

function go_home() {
  let result = confirm("Are you sure you want to redirect to home page?");
  if (result) {
    console.log("User confirmed to home");
    gohome = setTimeout(() => {
      window.location.href = "/";
    }, 6000);
  } else {
    console.log("User cancelled");
    alert("user cancelled!");
  }
}

const loginurl = "{% url 'cbv:login' %}";

function redi_login() {
  // window.location.href = loginurl;
  // window.location.assign(loginurl);
  window.location.replace(loginurl);
}

function check_name() {
  const name = document.getElementById("name")
  let name_value = name.value.trim()
  if (!name_value) {
    alert("Please enter your name");
    name.focus();
  } else {
    alert(`your name is ${name.value}`)
  }
}

function Uservalidation() {
  function isValidUser(username, password) {
    return username === "admin" && password === "1234";
  }

  if (isValidUser("admin", "1234")) {
    console.log("Login success");
    alert("Login Success")
  } else {
    console.log("Login failed");
    alert("Login failed")
  }
}

//Higher-Order Functions
function calculate(operation) {
  return operation(5, 3);
}
const add = (a, b) => a + b;
console.log(calculate(add));

// Callback function
function greet(name, callback) {
  console.log("Hello " + name);
  callback();
}
function done() {
  console.log("Done");
}
greet("Vishnu", done);

// arrow function
// const user5 = {
//   name: "Vishnu",
//   sayName: () => {
//     console.log(this.name);
//   }
// };
// user5.sayName() // not work
//Arrow functions do not have their own this
// Avoid arrow functions as object methods

const name_val_func = names => {
  if (names) {
    alert("welcome " + names)
  }
}
function name_prompt() {
  const na = prompt("Enter your name")
  name_val_func(na);
}

const age1 = age => {
  return age
}
function age_prompt() {
  alert("your age is " + age1(prompt("enter your age")))
}
// import welcomemessage from './vis2.js';

const sum = (a, b = 0) => a + b
console.log(sum(5) + ' sum number')

const squere = n => n * n;
console.log(squere(8) + ' squer num')

// confirm method
function permission() {
  let isLoggedIn = confirm("Are you sure?");
  if (isLoggedIn) {
    alert(isLoggedIn)
  } else {
    alert(isLoggedIn)
  }
}

// addEventListener

const redilogin = document.getElementById("redi_login");
if (redilogin) {
  redilogin.addEventListener("click", () => {
    window.location.href = loginurl;
  });
}

// if (password.length < 8) {
//     alert("Password must be at least 8 characters");
// }
// if (!email.includes("@")) {
//     alert("Invalid email");
// }

// typeof 
console.log(typeof 'vis')
console.log(typeof 10)
// console.log(typeof null)

// swithch and case method
let day = 1;
switch (day) {
  case 1:
    console.log("Monday");
    break;
  case 2:
    console.log("Tuesday");
    break;
  case 3:
    console.log("Wednesday");
    break;
  default:
    console.log("Invalid day");
}
// for loop method
for (let i = 1; i <= 5; i++) {
  console.log(i);
}

const welcomeElements = document.getElementsByClassName('content');
for (let i = 0; i < welcomeElements.length; i++) {
  console.log(welcomeElements[i].textContent);
}

// do while
let i = 5;
do {            //do while loop--> if true, loop continue
  console.log(i + "vis");
  i++;
  if (i === 7) {
    break
  }
} while (i <= 9);

let a = 3
if (true) {
  let a = 6
  console.log(a + "if")
}
console.log(a + 'globel')

// console.log("User logged in");
// console.error("Login failed");
// console.warn("Password is weak");
// document.write("<h1>Hello World</h1>");

// Array
let fruits = ["Apple", "Banana", "Mango"];

console.log(fruits[0]); // Apple
console.log(fruits[2]); // Mango
console.log(fruits.length)

// Common Array Methods (Very Important)

// push() — Add at end
fruits.push("Grapes");
console.log(fruits)

// unshift() — Add at start
fruits.unshift("Pineapple");
console.log(fruits)

// pop() — Remove from end
fruits.pop();
console.log(fruits)

// shift() — Remove from start
fruits.shift();
console.log(fruits)

// Using for
for (let i = 0; i < fruits.length; i++) {
  console.log(fruits[i] + ' for');
}

// Using for...of (Clean)
for (let fruit of fruits) {
  console.log(fruit + ' for of');
}

// map() — Transform array
let numbers = [1, 2, 3, 4, 5];

let gstPrices = numbers.map(price => price + 18);
console.log(gstPrices + ' gst')

// filter() — Select items
let even = numbers.filter(n => n % 2 === 0);
console.log(even + ' even')

// reduce() — Combine values
let total = numbers.reduce((sum, n) => sum + n, 0);
console.log(total + ' total')

// forEach
let users = [
  { name: "Vishnu", age: 24 },
  { name: "kum", age: 26 }
];

users.forEach(user => {
  console.log(user.name);
});

// reduce
let cart = [
  { product: "Phone", price: 15000 },
  { product: "Laptop", price: 50000 },
  { product: "Laptop", price: 0 }
];

let totals = cart.reduce((sum, item) => sum + item.price, 10);
console.log(totals + ' reduce total') // 65010

// object in javascript
const user = {
  name: "Vishnu",
  age: 24,
  country: "India"
};

// for in loop
// for...in loops over keys (property names)
//for...of loops over values
for (let key in user) {
  console.log(key, user[key]);
}

// Dot Notation
console.log(user.name);
// Bracket Notation
console.log(user["age"]);

// Modifying Object Properties
user.age = 25;
user.city = "Chennai";
console.log(user)

// delete object properties
delete user.country;
console.log(user)

// Object with methods
const user1 = {
  name: "Vishnu",
  greet: function () {
    console.log("Hello " + this.name);
  }
};
user1.greet();

//this refers to the current object.
const car = {
  brand: "Toyota",
  showBrand() {
    console.log(this.brand);
  }
};
car.showBrand();


// splice
//splice() is an array method 
// used to: Add elements, Remove elements, Replace elements.
let arr = ["A", "B", "C"];

arr.splice(1, 1, "X", "m");
console.log(arr) // ["A", "x", "m", "C"]

arr.splice(-2, 2);
console.log(arr) // ["A", "x"]


//Array Deatructuring
// Without Destructuring (Old Way)
const numbers1 = [10, 20, 30];

let a1 = numbers1[2];
let b1 = numbers1[1];
console.log(a1, b1)

// With Destructuring (Modern Way)

let [a2, b, c] = numbers1;

console.log(a2, b, c);

// Skipping Values
const colors = ["Red", "Green", "Blue"];

let [first, , third] = colors;

console.log(first, third);

// Default Values in Array Destructuring
const datas = [5];

let [x, y = 10] = datas;

console.log(x, y);

// Swapping Variables (Very Useful)
let x1 = 5;
let y1 = 10;

[x1, y1] = [y1, x1];

console.log(x1, y1);

// Object Destructuring
const user3 = {
  name: "Vishnu",
  age: 24,
  country: "India"
};
const { name, country, age } = user3;

console.log(name, country, age);

// Renaming Variables
const user2 = {
  name: "Vishnu",
  age: 26
};
const { name: userName, age: userAge } = user2;
console.log(userName, userAge);

// Default Values in Object Destructuring
const settings = {
  theme: "dark"
};
const { theme, language = "English" } = settings;
console.log(theme, language);

// Nested Object Destructuring
const user4 = {
  name: "Vishnu",
  address: {
    city: "Madurai",
    pincode: 626127
  }
};
const { address: { city } } = user4;
console.log(city);

// Destructuring in Function Parameters (Very Important)
function displayUser({ name, age }) {
  console.log(name, age);
}
displayUser({ name: "Vishnu", age: 24 });

// Real-World Example (API Response)
const response = {
  status: 200,
  data: {
    id: 1,
    title: "JavaScript"
  }
};

const { data: { title } } = response;

console.log(title);

//DOM (Document Object Model)
console.log(document);
console.log(window);
document.body.style.backgroundColor = "lightblue";

let a3 = document.getElementById("idname")
let c3 = document.querySelector("h1");
let c4 = document.querySelector(".box"); // class
let c5 = document.querySelector("#title"); // id
let d = document.querySelectorAll(".box"); // modern way
let b3 = document.getElementsByClassName("box") // old way

d.forEach(d1 => {
  console.log(d1);
});

// Selecting Nested Elements
let litag = document.querySelector("ul li");
let ptag = document.querySelectorAll(".card p");

// Checking If Element Exists
const btn = document.querySelector("#submit");

if (btn) {
  btn.style.backgroundColor = "green";
}

// Changing Text Content
const title1 = document.querySelector("h1");

//innerText : Changes only the visible text.
title1.innerText = "Welcome Vishnu";

// textContent : Changes all text (including hidden).
title1.textContent = "Hello World";

// innerHTML(Avoid) : Changes HTML inside an element.
title1.innerHTML = "<span>Hello</span> JavaScript";

// Changing Styles (CSS with JavaScript)
// Inline Style Change
const box = document.querySelector("#box");

box.style.backgroundColor = "blue"; // background-color → backgroundColor
box.style.color = "white";
box.style.padding = "10px";

// Adding & Removing CSS Classes (Best Practice)
box.classList.add("active");
box.classList.remove("active");
box.classList.toggle("active");

// Working with Attributes
const img = document.querySelector("img");

// Get Attribute
console.log(img.getAttribute("src"));

// Remove Attribute
img.removeAttribute("alt");

// Set Attribute
img.setAttribute("alt", "Profile Image");

// Creating New Elements
const p = document.createElement("p");
p.innerText = "This is a new paragraph";

document.body.appendChild(p);

// Adding Elements at Specific Positions
const container = document.querySelector(".container");
const newDiv = document.createElement("div");
newDiv.innerText = "New Item";

// container.append(newDiv);      // end
container.prepend(newDiv);     // start

// Removing Elements
const item = document.querySelector(".item");
item.remove();

const ul = document.querySelector("ul");
const li = document.createElement("li");
li.innerText = "Vis JavaScript";
// ul.appendChild(li);

//Add Event Listener
//click, input,	change, submit, mouseover, keydown, load
const button = document.getElementById('btn')
const nameinput = document.getElementById('name')
const formsub = document.getElementById('formsub')

// button.addEventListener("click", function (event) {
//   console.log("Button clicked");
//   this.style.backgroundColor = "green";
//   alert(event)
// });
// button.addEventListener("click", () => {
//   button.classList.toggle("active");
// });
nameinput.addEventListener("input", () => {
  console.log("Button input");
});
button.addEventListener("change", function () {
  console.log("Button change");
  alert("change")
});
// formsub.addEventListener("submit", function () {
//   console.log("Button submit");
//   alert("submit")
// });
// button.addEventListener("mouseover", function () {
//   console.log("Button mouseover");
//   alert("mouseover")
// });
// keydown: Buttons usually don’t receive key events unless focused.
// button.addEventListener("keydown", function () {
//   console.log("Button keydown");
//   alert("keydown")
// });
// window.addEventListener("load", function () {
//   console.log("Button load"); // when window is load, that function will activate
//   alert("load")
// });

// Closure: A function that remembers its surrounding variables.
function outer() {
  let count = 0;
  function inner() {
    count++;
    console.log(count);
  }
  return inner;
}
const counter = outer();
counter(); // 1
counter(); // 2

//Closure with Parameters
function Hello(name) {
  return function () {
    console.log("Hello " + name);
  };
}

const sayHello = Hello("Vishnu");
sayHello();

// Data Privacy Using Closures (Very Important)
function bankAccount() {
  let balance = 1000;
  return {
    deposit(amount) {
      balance += amount;
      console.log(`${balance} with deposit.`);
    },
    withdraw(amount) {
      balance -= amount;
      console.log(`${balance} with withdraw.`);
    }
  };
}
const account = bankAccount();
account.deposit(500);
account.withdraw(200);

// Closures in Event Handlers
function setup() {
  let clicks = 0;
  document.addEventListener("click", () => {
    clicks++;
    console.log(clicks);
    // alert("clicked")
  });
}
setup();

//Closures in Loops
for (let i = 1; i <= 3; i++) {
  setTimeout(() => console.log(i), 3000);
}

function once(fn) {
  let called = false;
  return function () {
    if (!called) {
      called = true;
      fn();
    }
  };
}
const init = once(() => console.log("Initialized"));
init();
init(); // won't run again

// Higher-Order Functions: A function that works with functions.
function calculater(a, b, operation) {
  return operation(a, b);
}
const addsum = (x, y) => x + y;
const multiply = (x, y) => x * y;
console.log(calculater(5, 3, addsum));    // 8
console.log(calculater(5, 3, multiply));  // 15

// Function Returning Function
function multiplier(factor) {
  return function (number) {
    console.log(`number is ${number} and factor is ${factor}`)
    return number * factor;
  };
}
const double = multiplier(2);
console.log(double(5)); // 10

// Chaining Higher-Order Functions
const result = [1, 2, 3, 4, 5]
  .filter(n => n % 2 === 0)
  .map(n => n * 10);

console.log(result); // [20, 40]

// Creating Your Own HOF
function logger(fn) {
  return function (...args) {
    console.log("Calling function");
    return fn(...args);
  };
}
const adding = (a, b) => a + b;
const loggedAdd = logger(adding);

console.log(loggedAdd(2, 3));

// Real-World Example (Permission Check)
function withPermission(fn) {
  return function (user) {
    if (!user) {
      return "Access Denied";
    }
    return fn(user);
  };
}
const deleteUser = user => "User deleted";
const secureDelete = withPermission(deleteUser);
console.log(secureDelete('vishnu'))

//this, call, apply, and bind in JavaScript
console.log(`this ${this}`);

// this Inside a Function
function show() {
  console.log(`inside a function this ${this}`);
}
show();

// this Inside an Object Method
const userv = {
  name: "Vishnu",
  greet() {
    console.log(`object method this ${this.name}`);
  }
};
userv.greet();

// this in Arrow Functions (Critical Rule)
const userk = {
  name: "Vishnu",
  greet: () => {
    console.log(this.name);
  }
};

button.addEventListener("click", function () {
  console.log(this);
});

// call, apply, bind: They allow you to manually set the value of this.
function greety(method) {
  console.log(this.name + " from " + method);
}
const uservis = { name: "Vishnu" };

//call
greety.call(uservis, "call");

// apply
greety.apply(uservis, ["apply"]);

// bind: returns function
const boundGreet = greety.bind(uservis, "bind");
boundGreet();

// Callback with Error Handling
function login(user, callback) {
  setTimeout(() => {
    if (user === "admin") {
      callback(null, "Login success");
    } else {
      callback("Login failed");
    }
  }, 1000);
}

login("admin", function (error, success) {
  if (error) {
    console.log(error);
  } else {
    console.log(success);
  }
});

// Callback Hell (Pyramid of Doom)
setTimeout(() => {
  console.log("Step 1");
  setTimeout(() => {
    console.log("Step 2");
    setTimeout(() => {
      console.log("Step 3");
    }, 1000);
  }, 1000);
}, 1000);

// Promises in JavaScript
const loginPromise = new Promise((resolve, reject) => {
  let success = true;

  setTimeout(() => {
    if (success) {
      resolve("Login successful");
    } else {
      reject("Login failed");
    }
  }, 2000);
});
loginPromise
  .then(result => {
    console.log(result);
  })
  .catch(error => {
    console.log(error);
  })
  .finally(() => console.log("Operation completed"));

// Promise Chaining (Very Important)
function getUserdata() {
  return new Promise(resolve => {
    setTimeout(() => resolve("Vishnu"), 1000);
  });
}
function getProfile(user) {
  return new Promise(resolve => {
    setTimeout(() => resolve(user + "'s profile"), 1000);
  });
}
getUserdata()
  .then(user => getProfile(user))
  .then(profile => console.log(profile))
  .catch(err => console.log(err))
  .finally(() => console.log("Operation completed"));

// async / await in JavaScript
// An async function always returns a Promise.This is a strict rule in JavaScript.
// You can use await only inside async functions
async function fetchData() {
  const data = await Promise.resolve("Data loaded");
  console.log(data);
}
function processData(data) {
  console.log("Processed:", data);
}

function handleError(err) {
  console.error(err);
}

fetchData();

// Promise Style
fetchData()
  .then(data => processData(data))
  .catch(err => handleError(err));

// async / await Style
async function load() {
  try {
    const data = await fetchData();
    processData(data);
  } catch (err) {
    handleError(err);
  }
}
load()

// Parallel Execution with Promise.all()
function getUser() {
  return new Promise(resolve =>
    setTimeout(() => resolve("User data"), 2000)
  );
}
function getPosts() {
  return new Promise(resolve =>
    setTimeout(() => resolve("Posts data"), 3000)
  );
}
async function loadAll() {
  const [user, posts] = await Promise.all([
    getUser(),
    getPosts()
  ]);
}
loadAll() // Output after 3 seconds:

// Real-World Example (API Call Simulation)
async function fetchProduct() {
  try {
    const response = await fetch("http://127.0.0.1:8000/members_list");
    const data = await response.json();
    console.log("members list", data);
  } catch (err) {
    console.log("Fetch error", err);
  }
}
fetchProduct()

// Fetch API in JavaScript
// JSON.stringify() == converts a JavaScript object into a JSON string.
// JSON.parse() == converts a JSON string into a JavaScript object.
// response.json() == is a method of the Fetch API that reads the HTTP response body and converts JSON text into a JavaScript object.
fetch("http://127.0.0.1:8000/members_list")
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.log(error));

// POST Request (Sending Data)  
async function createUser() {
  const response = await fetch("http://127.0.0.1:8000/members_list", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: "Vishnu",
      age: 24
    })
  });

  const data = await response.json();
  console.log(data);
}

// Fetching & Displaying Data in DOM
async function loadPosts() {
  const response = await fetch("http://127.0.0.1:8000/members_list");
  const posts = await response.json();

  posts.forEach(post => {
    const p = document.createElement("p");
    p.innerText = post.title;
    document.body.appendChild(p);
  });
}

// Real-World Example (Login Request)
async function loginfbv(username, password) {
  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) throw new Error("Login failed");

    const data = await response.json();
    console.log("Welcome", data.user);
  } catch (err) {
    console.log(err.message);
  }
}

// Spread with Arrays
const nums1 = [1, 2];
const nums2 = [3, 4];

const all = [...nums1, ...nums2];

// Copy Array (Safe)
const copy = [...nums1];

// Spread with Objects
const userdetail = { name: "Vishnu", age: 24 };
const updatedUser = { ...userdetail, city: "Madurai" };

function sumadd(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}
console.log(sumadd(1, 2, 3, 4));

// Optional Chaining (?.) Nullish Coalescing (??)
// API Safe Access
const responses = {
  data: {
    user: {
      name: "Vishnu"
    }
  }
};
const userNames = responses.data?.user?.name ?? "Anonymous";
// Script has type="module" to import
// <script type="module" src="main.js"></script>

// import welcomemessage, {add as sums, sub, mul, divi} from './vis2.js';
// console.log(welcomemessage("vishnu kumar"))
// console.log(sum(3, 6))
// console.log(sub(3, 6))
// console.log(mul(3, 6))
// console.log(divi(3, 6))

// import * as math from "./vis2.js";

// math.add(2, 3);
// math.subtract(5, 2);

// error handling
function withdraw(amount) {
  if (amount <= 0) {
    throw new Error("Invalid amount");
  }
  console.log("Withdrawn:", amount);
}

try {
  withdraw(-100);
} catch (e) {
  console.log(e.message);
}

// Creating Custom Error Types (Advanced)
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";   // ValidationError: Invalid input
  }
}

try {
  throw new ValidationError("Invalid input");
} catch (e) {
  console.log(e.name, e.message);
}

// JavaScript uses two main memory areas: 1.Stack Memory, 2.Heap Memory

let user5 = { name: "Vishnu" };
user5 = null; // eligible for garbage collection
// If nothing references an object → it can be removed.

// Common Causes of Memory Leaks
let data = "safe"; // no let/const → global

// Detached DOM Elements
// box.parentNode.removeChild(box);  // ❌ unsafe parent
box.remove();

// Memory Leaks in Event Listeners
function handler() {
  console.log("clicked");
}
button.addEventListener("click", handler);
// element removed but listener remains

button.removeEventListener("click", handler);

// Throttling

// Module Pattern (Very Important)
const counterModule = (function () {
  let count = 0; // private

  return {
    increment() {
      count++;
      console.log(count);
    },
    reset() {
      count = 0;
    }
  };
})();
counterModule.increment();
counterModule.increment();
counterModule.reset();

// Singleton Pattern
const AppConfig = (function () {
  let instance;
  function createInstance() {
    return { appName: "visapp" };
  }
  return {
    getInstance() {
      if (!instance) {
        instance = createInstance();
      }
      return instance;
    }
  };
})();
const aa = AppConfig.getInstance();
const bb = AppConfig.getInstance();

aa === bb //→ true

// Factory Pattern
function userFactory(role) {
  if (role === "admin") {
    return { role, access: "full" };
  }
  return { role, access: "limited" };
}
const admin = userFactory("admin");
const user6 = userFactory("user");

// Observer Pattern (Very Common)
class Subject {
  constructor() {
    this.observers = [];
  }
  subscribe(fn) {
    this.observers.push(fn);
  }
  notify(data) {
    this.observers.forEach(fn => fn(data));
  }
}
let msg = 'marveles!'
const news = new Subject();
news.subscribe(msg => console.log("User1:", msg));
news.subscribe(msg => console.log("User2:", msg));
news.notify("Breaking News");

const calculator = (function () {
  function add(a, b) {
    return a + b;
  }

  function subtract(a, b) {
    return a - b;
  }

  return { add, subtract };
})();


