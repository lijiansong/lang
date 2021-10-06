defmodule Fibonacci do
  def seq(0), do: 0
  def seq(1), do: 1
  def seq(n) when n > 1 do
    compute_seq(n, 1, [0, 1])
  end

  defp compute_seq(n, i, acc) when n == i, do: Enum.at(acc, length(acc) - 1)
  defp compute_seq(n, i, acc) do
    len = length(acc)
    compute_seq(n, i + 1, acc ++ [Enum.at(acc, len-1) + Enum.at(acc, len-2)])
  end
end

IO.puts Fibonacci.seq(50)
