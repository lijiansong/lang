defmodule Math do
  defmacro square(x) do
    quote bind_quoted: [x: x]do
      x * x
    end
  end
end
