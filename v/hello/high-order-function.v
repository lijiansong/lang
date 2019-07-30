fn sqr(n int) int {
    return n * n
}

fn run(value int, op fn(int) int) int {
    return op(value)
}

const (
	Pi    = 3.14
	World = '世界'
)
struct Color {
    r int
    g int
    b int
}

fn (c Color) str() string { return '{$c.r, $c.g, $c.b}' }

fn rgb(r, g, b int) Color { return Color{r: r, g: g, b: b} }

const (
    Numbers = [1, 2, 3]

    Red  = Color{r: 255, g: 0, b: 0}
    Blue = rgb(0, 0, 255)
)


fn main()  {
    // high order function
    println(run(5, sqr)) // "25"
    // const
    println(Pi)
    println(World)

    // const
    println(Numbers)
    println(Red)
    println(Blue)
}
