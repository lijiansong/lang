defmodule Reverse do
  def reverse([]), do: []
  def reverse([h|t]), do: reverse(t) ++ [h]
end
