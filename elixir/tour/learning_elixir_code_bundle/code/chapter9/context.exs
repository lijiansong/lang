defmodule ContextInfo do
  defmacro grab_caller_context do
    quote do
      IO.puts var!(x)
    end
  end

  defmacro inject_context_change do
    quote do
      var!(x) = 0
    end
  end
end
