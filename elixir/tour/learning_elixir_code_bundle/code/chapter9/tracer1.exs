defmodule Tracer do

  defmacro def(defintion={name, _, args}, content) do
    quote do
      Kernel.def(unquote(definition)) do
      unquote(content)
    end
  end

  defmacro __using__(_) do
    quote do
      import Kernel, except: [def: 2]
      import unquote(__MODULE__), only: [def: 2]
    end
  end

end
