defmodule QueryList do
  defmacro bar(x) do
    quote bind_quoted: [x: x] do
      x * x
    end
  end

  defmacro foo(q, mer) do
    quote bind_quoted: [records: records] do
      for unquote(q) <- mer, do: unquote(q)
    end
  end
end
