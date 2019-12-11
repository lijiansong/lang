function greeter(person) {
    return "Hello, " + person.firstName + " " + person.lastName;
}
var user = { firstName: "Json", lastName: "Lee" };
document.body.textContent = greeter(user);
