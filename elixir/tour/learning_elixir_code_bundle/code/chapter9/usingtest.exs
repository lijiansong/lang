defmodule UsingTest do

  defmacro __using__(_opts) do
    quote do
      IO.puts "I'm the __using__/1 of #{unquote(__MODULE__)}"
    end
  end
end

defmodule TestMyUsing do
  use UsingTest
end
