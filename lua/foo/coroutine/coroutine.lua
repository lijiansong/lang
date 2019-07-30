lua_co = coroutine.create(function (value1,value2)
   local tempvar3 = 10
   print("coroutine section 1:", value1, value2, tempvar3)

   local tempvar1 = coroutine.yield(value1+1,value2+1)
   tempvar3 = tempvar3 + value1
   print("coroutine section 2:",tempvar1 ,tempvar2, tempvar3)

   local tempvar1, tempvar2= coroutine.yield(value1+value2, value1-value2)
   tempvar3 = tempvar3 + value1
   print("coroutine section 3:",tempvar1,tempvar2, tempvar3)
   return value2, "end"

end)

print("main", coroutine.resume(lua_co, 3, 2))
print("main", coroutine.resume(lua_co, 12,14))
print("main", coroutine.resume(lua_co, 5, 6))
print("main", coroutine.resume(lua_co, 10, 20))
--[[
coroutine section 1:	3	2	10
main	true	4	3
coroutine section 2:	12	nil	13
main	true	5	1
coroutine section 3:	5	6	16
main	true	2	end
main	false	cannot resume dead coroutine
--]]

function getNumber()
   local function getNumberHelper()
      co = coroutine.create(function ()
      coroutine.yield(1)
      coroutine.yield(2)
      coroutine.yield(3)
      coroutine.yield(4)
      coroutine.yield(5)
      end)
      return co
   end

   if(numberHelper) then
      status, number = coroutine.resume(numberHelper);

      if coroutine.status(numberHelper) == "dead" then
         numberHelper = getNumberHelper()
         status, number = coroutine.resume(numberHelper);
      end

      return number
   else
      numberHelper = getNumberHelper()
      status, number = coroutine.resume(numberHelper);
      return number
   end

end

for index = 1, 10 do
   print(index, getNumber())
end

--[[
1	1
2	2
3	3
4	4
5	5
6	1
7	2
8	3
9	4
10	5
--]]
