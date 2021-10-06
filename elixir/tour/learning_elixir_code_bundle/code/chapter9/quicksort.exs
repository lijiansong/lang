defmodule Quicksort do
  use Tracer

  def sort(list), do: _sort(list)

  defp _sort([]), do: []
  defp _sort(l = [h|_t]) do
    (l |> Enum.filter(&(&1 < h)) |> _sort)
    ++ [h] ++
    (l |> Enum.filter(&(&1 > h)) |> _sort)
  end

end
