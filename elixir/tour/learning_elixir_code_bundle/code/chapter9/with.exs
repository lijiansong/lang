defmodule With do
  defmacro with(res, block) do
    do_clause = Keyword.get(block, :do, nil)
    quote do
      {:ok, var!(f)} = File.open(unquote(res))
      result = unquote(do_clause)
      :ok = File.close(var!(f))
      result
    end
  end
end
