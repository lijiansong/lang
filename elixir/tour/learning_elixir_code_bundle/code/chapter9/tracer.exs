defmodule Tracer do

  def dump_args(args) do
    args |> Enum.map(&inspect/1) |> Enum.join(", ")
  end

  defmacro def(definition={name, _, args}, do: content) do
    quote do
      Kernel.def(unquote(definition)) do
        IO.puts :stderr,
                ">>> Calling #{unquote(name)} with #{Tracer.dump_args(unquote(args))}"
        result = unquote(content)
        IO.puts :stderr, "<<< Result: #{Macro.to_string result}"
        result
      end
    end
  end

  defmacro __using__(_) do
    quote do
      import Kernel, except: [def: 2]
      import unquote(__MODULE__), only: [def: 2]
    end
  end

end
