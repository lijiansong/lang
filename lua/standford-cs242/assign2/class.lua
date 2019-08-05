local Object
Object = {
  isinstance = function(cls) return cls == Object end,
  constructor = function() end,
  methods = {},
  data = {},
  metamethods = {}
}


-- override isinstance
function isInstance(instance, class) 
  local instClass = instance.thisClass
  while instClass ~= nil do
    if instClass == class then 
      return true
    else
      instClass = instClass.parent
    end
  end
  return false
end


-- This is a utility function you will find useful during the metamethods section.
function table.merge(src, dst)
  for k,v in pairs(src) do
    if not dst[k] then dst[k] = v end
  end
end


local function class(parent, child)

  -- The "child.methods or {}" syntax can be read as:
  -- "if child.methods is nil then this expression is {}, otherwise it is child.methods"
  -- Generally, "a or b" reduces to b if a is nil or false, evaluating to a otherwise.
  local methods = child.methods or {}
  local data = child.data or {}
  local constructor = child.constructor or parent.constructor
  local metamethods = child.metamethods or {}

  local Class = {}

  -- Your code here.
  
  -- override isinstance in methods
  methods.isinstance = isInstance
  
  -- merge 
  if parent ~= nil then
    if parent.methods ~= nil then table.merge(parent.methods, methods) end
    if parent.data ~= nil then table.merge(parent.data, data) end
    if parent.metamethods ~= nil then table.merge(parent.metamethods, metamethods) end
  end
  
  -- for inheritance
  Class.parent = parent
  Class.methods = methods
  Class.data = data
  Class.constructor = constructor
  Class.metamethods = metamethods
  
  function Class.new(...) 
    local public = {thisClass = Class}
    local private = {thisClass = Class}
    
    -- for public method to call private data member
    function index(t, k) 
      if methods[k] == nil then 
        return nil 
      else return 
        function(self, ...) 
          return methods[k](private, ...)
        end
      end
    end
    
    -- set meta table
    local publicMetaTab = {__index = index}
    local privateMetaTab = {__index = methods}
    
    -- copy metamethods
    for k, v in pairs(metamethods) do
      publicMetaTab[k] = v
      privateMetaTab[k] = v
    end
    
    -- set meta table
    setmetatable(public, publicMetaTab)
    setmetatable(private, privateMetaTab)
    
    -- data exists only in private
    for k, v in pairs(data) do private[k] = v end
    
    -- execute constructor
    constructor(private, ...)
    
    return public
    
  end

  return Class
end

return {class = class, Object = Object} 
