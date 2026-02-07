// auto refresh
setTimeout(() => {
    //location.reload(true);
    window.location.reload();
}, 1000);

console.log('welcome to vis3.js')
console.log('welcome to vis3.js')

// this in the Global Scope
// In Browsers
console.log(this); // Output: window

// In Node.js
console.log(this);  // Output: {}
// In Node.js modules, this refers to module.exports

// this Inside a Normal Function (Non-Strict Mode)
function show() {
    console.log(this);
}
show();  // Output (Browser): window

// this in Strict Mode ("use strict")
"use strict";

function showstatic() {
    console.log(this);
}
showstatic();  // Output: undefined

// Correct Use of Arrow Functions Inside Objects
const user = {
    name: "Vishnu",
    greet() {
        const inner = () => {
            console.log(`arrow function ${this.name}`);
        };
        inner();
    }
};
user.greet();

// this in class
class User {
    constructor(name) {
        this.name = name;
    }
    greet() {
        console.log(`class method ${this.name}`);
    }
}
const u = new User("Vishnu");
u.greet();

const button = document.getElementById("btn")
if (button){
  button.addEventListener("click", function () {
      console.log(this);
  });
}

// this in setTimeout
const user1 = {
    name: "Vishnu",
    greet() {
        setTimeout(function () {
            console.log(this.name);
        }, 1000);
    }
};
user1.greet();  // Output: undefined

// Fix with Arrow Function
const user2 = {
    name: "Vishnu",
    greet() {
        setTimeout(() => {
            console.log(this.name);
        }, 1000);
    }
};
user2.greet();

// E-Commerce Cart Calculation
const cart = {
  total: 0,
  add(price) {
    this.total += price;
  }
};
cart.add(50)

// Form Validation Object
const validator = {
  errors: [],
  addError(msg) {
    this.errors.push(msg);
  }
};

// Button Click Event (DOM)
button.addEventListener("click", function () {
  this.disabled = true;
});

// Timer with State (setTimeout)
const app = {
  name: "TimerApp",
  start() {
    setTimeout(() => {
      console.log(this.name);
    }, 1000);
  }
};

// Constructor Function (User Creation)
function User3(name) {
  this.name = name;
}

// ES6 Class (Service Layer)
class ApiService {
  constructor(url) {
    this.url = url;
  }
}

// React Class Component (Legacy)
// this.setState({ count: this.state.count + 1 });
// Keep this only inside React class components.

// React Event Handler Binding
this.handleClick = this.handleClick.bind(this);

// Method Borrowing with call()
function logName() {
  console.log(this.name);
}

logName.call({ name: "Admin" });

// Array Iteration with Context
numbers.forEach(function (n) {
  this.sum += n;
}, calculator);

// Express.js Controller
class UserController {
  getUser(req, res) {
    res.send(this.service.getUser());
  }
}

// Middleware Pattern
function middleware(req, res) {
  console.log(this.config);
}

// Debounce / Throttle Utility
function debounce(fn) {
  return function () {
    fn.apply(this, arguments);
  };
}

// Data Store / State Manager
const store = {
  state: {},
  set(key, value) {
    this.state[key] = value;
  }
};

// Logger Utility
const logger = {
  prefix: "[APP]",
  log(msg) {
    console.log(this.prefix, msg);
  }
};

// Plugin Architecture
plugin.init = function () {
  this.enabled = true;
};

// Custom Event System
eventHandler.handle = function () {
  console.log(this.eventName);
};

// Fetch Wrapper Class
class HttpClient {
  request() {
    return fetch(this.baseUrl);
  }
}

// Configuration-Driven Application
const appConfig = {
  env: "production",
  getEnv() {
    return this.env;
  }
};