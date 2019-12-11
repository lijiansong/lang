var Student = /** @class */ (function () {
    function Student(firstName, middleInitial, lastName) {
        this.firstName = firstName;
        this.middleInitial = middleInitial;
        this.lastName = lastName;
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
    return Student;
}());
function greeter(s) {
    return "Hello, " + s.firstName + " " + s.lastName + "! You are " + s.middleInitial;
}
var user = new Student("Json", "M.", "Lee");
document.body.textContent = greeter(user);
