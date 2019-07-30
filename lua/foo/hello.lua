#!/usr/local/bin/lua

-- REF: https://www.tutorialspoint.com/lua/

--[[ Lua comments

multiple line
--]]

print("Hello World!")
io.write("Hello world, from ", _VERSION, "!\n")
-- Variable definition:
local a, b

-- Initialization
a = 10
b = 30

print("value of a:", a)

print("value of b:", b)

-- Swapping of variables
b, a = a, b

print("value of a:", a)

print("value of b:", b)

f = 70.0/3.0
print("value of f", f)
print(type(f))
print(type("What is my type"))   --> string
t = 10

print(type(5.8*t))               --> number
print(type(true))                --> boolean
print(type(print))               --> function
print(type(nil))                 --> nil
print(type(type(ABC)))           --> string

-- High order function
function create_a_counter()
    local count = 0
    return function()
        count = count + 1
        return count
    end
end

function max(num1, num2)
   if (num1 > num2) then
      result = num1;
   else
      result = num2;
   end

   return result;
end

print("max 1 2: ", max(1, 2))

-- Assigning and passing functions
myprint = function(param)
   print("This is my print function -   ##",param,"##")
end

function add(num1,num2,functionPrint)
   result = num1 + num2
   functionPrint(result)
end

myprint(10)
add(2,5,myprint)

-- Function with Variable Argument
function average(...)
   result = 0
   local arg = {...}
   for i,v in ipairs(arg) do
      result = result + v
   end
   return result/#arg
end

print("The average is",average(10,5,3,4,5,6))

string1 = "Lua";

print(string.upper(string1))
print(string.lower(string1))

print(string.byte("Lua"))
-- Third character
print(string.byte("Lua",3))
-- first character from last
print(string.byte("Lua",-1))

string1 = "Lua"
string2 = "Tutorial"

-- String Concatenations using ..
print("Concatenated string:",string1..string2)

-- Length of string
print("Length of string1 is:",string.len(string1))
print("Length of string1 is:",#string1)

-- Repeating strings
repeatedString = string.rep(string1,3)
print(repeatedString)

array = {"Lua", "Tutorial"}

for i = 0, 2 do
   print(array[i])
end

--[[
--In Lua, indexing generally starts at index 1. But it is possible to create objects at index 0 and below 0 as well. Array using negative indices is shown below where we initialize the array using a for loop.
----]]
array = {}

for i= -2, 2 do
   array[i] = i *2
end

for i = -2,2 do
   print(array[i])
end

-- Initializing the array
array = {}

for i=1,3 do
   array[i] = {}

   for j=1,3 do
      array[i][j] = i*j
   end

end

-- Accessing the array

for i=1,3 do

   for j=1,3 do
      print(array[i][j])
   end

end

-- Initializing the array

array = {}

maxRows = 3
maxColumns = 3

for row=1,maxRows do

   for col=1,maxColumns do
      array[row*maxColumns +col] = row*col
   end

end

-- Accessing the array

for row=1,maxRows do

   for col=1,maxColumns do
      print(array[row*maxColumns +col])
   end

end

-- Simple empty table
mytable = {}
print("Type of mytable is ",type(mytable))

mytable[1]= "Lua"
mytable["wow"] = "Tutorial"

print("mytable Element at index 1 is ", mytable[1])
print("mytable Element at index wow is ", mytable["wow"])

-- alternatetable and mytable refers to same table
alternatetable = mytable

print("alternatetable Element at index 1 is ", alternatetable[1])
print("mytable Element at index wow is ", alternatetable["wow"])

alternatetable["wow"] = "I changed it"

print("mytable Element at index wow is ", mytable["wow"])

-- only variable released and and not table
alternatetable = nil
print("alternatetable is ", alternatetable)

-- mytable is still accessible
print("mytable Element at index wow is ", mytable["wow"])

mytable = nil
print("mytable is ", mytable)
-- Table
fruits = {"banana","orange","apple","grapes"}

for k,v in ipairs(fruits) do
   print(k,v)
end

table.sort(fruits)
print("sorted table")

for k,v in ipairs(fruits) do
   print(k,v)
end

fruits = {"banana","orange","apple"}

-- returns concatenated string of table
print("Concatenated string ",table.concat(fruits))

--concatenate with a character
print("Concatenated string ",table.concat(fruits,", "))

--concatenate fruits based on index
print("Concatenated string ",table.concat(fruits,", ", 2,3))
fruits = {"banana","orange","apple"}

-- insert a fruit at the end
table.insert(fruits,"mango")
print("Fruit at index 4 is ",fruits[4])

--insert fruit at index 2
table.insert(fruits,2,"grapes")
print("Fruit at index 2 is ",fruits[2])

-- print("The maximum elements in table is",table.maxn(fruits))

print("The last element is",fruits[5])

table.remove(fruits)
print("The previous last element is",fruits[5])

-- meta table
mytable = setmetatable({key1 = "value1"}, {
   __index = function(mytable, key)

      if key == "key2" then
         return "metatablevalue"
      else
         return mytable[key]
      end
   end
})

print(mytable.key1,mytable.key2)
