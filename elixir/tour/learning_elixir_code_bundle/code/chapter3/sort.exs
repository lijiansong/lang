defmodule Sort do
  def quicksort([]), do: []
  def quicksort([h|t]) do
    lower = Enum.filter(t, &(&1 <= h))
    upper = Enum.filter(t, &(&1 > h))
    quicksort(lower) ++ [h] ++ quicksort(upper)
  end
end
