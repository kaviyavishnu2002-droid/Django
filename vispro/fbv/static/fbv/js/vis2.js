console.log(typeof 'viskum')

// for loop
let sum = 0;
for (let i = 1; i <= 10; i++) {
    sum += i;
}
console.log(sum)

const colors = ["red", "green", "blue"];

for (let color of colors) {
    console.log(color);
}

// for of 
const person = [{ name: "Vishnu", age: 24 },
{ name: "kavi", age: 25 }
];

for (let key of Object.keys(person)) {
    console.log(key, person[key]);
}

// for in
const persons = {
    name: "Vishnu",
    age: 24,
    city: "Chennai"
};

for (let key in persons) {
    console.log(key, persons[key]);
}

console.log('export deleted')

