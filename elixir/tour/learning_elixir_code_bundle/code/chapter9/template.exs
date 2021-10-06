defmodule Template do
  import Xml

  def render do
    xml do
      tag :model, name: "my_model" do
        for i <- 0..5 do
          tag :attribute do
            text "some value #{i}"
          end
        end
      end
    end
  end

end
