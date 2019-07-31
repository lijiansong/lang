local util = require("common.util")
local posix = require("posix")
local Pipe = util.Pipe
local mod = {}

function mod.serialize(t)
	if type(t) == "number" then
		return "number(" .. tostring(t) .. ")"
	elseif type(t) == "string" then
		return "string(" .. t .. ")"
	elseif type(t) == "boolean" then 
		return "boolean(" .. tostring(t) .. ")"
	elseif type(t) == "nil" then 
		return "nil()"
	else -- table and recursively table
		if next(t) == nil then
			return "table()"
		end
		local str = "table("
		for k, v in pairs(t) do 
			str = str .. mod.serialize(k) .. mod.serialize(v)
		end
		str = str .. ")"
		return str
	end
	return nil
end


-- split by the first occurance
function mod.split2(str, pat) 
	local words = {}
	idx = string.find(str, pat)
	if idx == nil then
		return words
	end
	table.insert(words, string.sub(str, 1, idx - 1))
	table.insert(words, string.sub(str, idx + 1))
	return words
end


function mod.deserialize(s)
	-- print("str: " .. tostring(s))
	local idx, _ = string.find(s, "%(")
	-- print("idx: " .. tostring(idx))
	local sub_1 = string.sub(s, 1, idx - 1)
	-- print("sub_1: " .. tostring(sub_1))
	local sub_2 = string.sub(s, idx + 1, -2)
	-- print("sub_2: " .. tostring(sub_2))
	if sub_1 == "number" then
		return tonumber(sub_2) 
	elseif sub_1 == "string" then
		return sub_2
	elseif sub_1 == "boolean" then
		if sub_2 == "true" then
			return true
		else 
			return false
		end
	elseif sub_1 == "nil" then
		return nil
	else -- table and recursively table, deal with sub_2
		local ele = {}
		local ans = {}
		while sub_2 ~= "" do
			local ind, _ = string.find(sub_2, "%(")
			local start = ind
			local enddd = ind + 1
			local counter = 1
			while counter ~= 0 do
				if string.sub(sub_2, enddd, enddd) == "(" then
					counter = counter + 1
				end
				
				if string.sub(sub_2, enddd, enddd) == ")" then 
					counter = counter - 1
				end
				enddd = enddd + 1
			end
			local str = string.sub(sub_2, 1, enddd - 1)
			local test =  mod.deserialize(str)
			table.insert(ele, test)

			sub_2 = string.sub(sub_2, enddd)
		end
		local tl = tablelength(ele)
		for i = 1, tl -1, 2 do
			ans[ele[i]] = ele[i + 1]
		end
		-- print("table returns !!!!!!!!!!!")
		return ans

	end

	return nil
end

function tablelength(T)
	local count = 0
	for _ in pairs(T) do
		count = count + 1
	end
	return count
end


function mod.rpcify(class)
	in_pipe = Pipe.new()
	out_pipe = Pipe.new()
	local pid = -1
	local MyClassRPC = {}

	for k, v in pairs(class) do
		if type(v) == "function" and k ~= "new" then
			MyClassRPC[k .. "_async"] = function(...) 
				local tab = table.pack(k, {...})
				local ser = mod.serialize(tab)
				return function()
					Pipe.write(in_pipe, ser)-- here, not only the function name, but also arg list
					return Pipe.read(out_pipe) -- should be return value from child process
				end
			end
			MyClassRPC[k] = v
		end
	end

	MyClassRPC.new = function() -- this function should fork off a child process
		pid = posix.fork()
		if pid == 0 then
			MyClassRPC.child()
		end
		return class.new() 
	end

	MyClassRPC.exit = function()
		Pipe.write(in_pipe, "exit")
		posix.wait(pid)
	end

	MyClassRPC.child = function()
		while true do
			local message = Pipe.read(in_pipe)
			if message == "exit" then
				break
			end
			local tab = mod.deserialize(message)
			local key = tab[1]
			if class[key] ~= nil then
				Pipe.write(out_pipe, class[key](table.unpack(tab[2])))
			end
		end
		os.exit()
	end	
	return MyClassRPC 
end


return mod
