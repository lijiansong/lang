struct Dog {}
struct Cat {}

fn (d Dog) speak() string {
	return 'woof'
}

fn (c Cat) speak() string {
	return 'meow'
}

interface Speaker {
	speak() string
}

fn perform(s Speaker) {
	println(s.speak())
}

fn main()  {
    // interface example
    dog := Dog{}
    cat := Cat{}
    perform(dog) // ==> "woof"
    perform(cat) // ==> "meow"
}
