class Student {
    fullName: string;
    constructor(public firstName: string, public middleInitial: string, public lastName: string) {
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
}

interface Person {
    firstName: string;
    lastName: string;
}

function greeter(s: Student) {
    return "Hello, " + s.firstName + " " + s.lastName + "! You are " + s.middleInitial;
}

let user = new Student("Json", "M.", "Lee");

document.body.textContent = greeter(user);
