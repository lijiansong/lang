defmodule Fibonacci do
  def seq(0), do: 0
  def seq(1), do: 1
  def seq(n) when n > 1, do: seq(n-1) + seq(n-2)
end

IO.puts Fibonacci.seq(50)
