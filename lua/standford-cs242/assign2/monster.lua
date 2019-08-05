local Entity = require "entity"

local Monster = class.class(
  Entity, {
    methods = {
      Char = function(self)
        return "%"
      end,

      Color = function(self)
        return termfx.color.RED
      end,

      Collide = function(self, e)
        self.game:Log("A monster hits you for 2 damage.")
        e:SetHealth(e:Health() - 2)
      end,

      Die = function(self, e)
        self.game:Log("The monster dies.")
      end,

      Think = function(self)
        -- Your code here.
        if self:CanSee(self.game:Hero()) then
          local vect = self:PathTo(self.game:Hero())
          table.remove(vect)
          local v = table.remove(vect)
          local next_step = v - self:Pos()
          self.game:TryMove(self, next_step)
        end
        
      end
    }
})

return Monster
