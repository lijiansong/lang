defmodule Foo do
  @spec identity(integer) :: integer
  def identity(x), do: x
end

IO.puts(Foo.identity(4))

IO.puts(Foo.identity("4.4"))
