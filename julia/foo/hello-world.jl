# This is a comment

#=
Comment block
=#

println("hello world!")

# function
function f(x)
   return x^2
end
println(f(4.0))

# Function: anonymous
g = x -> x^4
println(g(4.0))

# Tuples:
t = (1, 2.0, "test")
println(t[1])

# Named Tuples/ Anonymous Structures
# 1. vanilla
m = (x = 1, y = 2)
println(m.x)

# 2. constructor
#using Parameters
#mdef = @with_kw (x=1, y=2)
#m = mdef() # same as above
#m = mdef(x = 3)

# Closures
a = 2.0
f(x) = a + x
println(f(1.0))

# Inplace Modification
function f!(out, x)
    out .= x.^2
end
x = rand(10)
y = similar(x)
println(x)
println(y)
println(f!(y, x))

