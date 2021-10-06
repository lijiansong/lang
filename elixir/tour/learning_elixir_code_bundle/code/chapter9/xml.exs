defmodule Xml do

  def start_buffer(state), do: Agent.start_link(fn -> state end)

  def stop_buffer(buffer), do: Agent.stop(buffer)

  def put_buffer(buffer, content), do: Agent.update(buffer, &[content | &1])

  def render(buffer) do
    Agent.get(buffer, &(&1))
    |> Enum.reverse
    |> Enum.join("")
  end

  defmacro xml(do: block) do
    quote do
      {:ok, var!(buffer, Xml)} = start_buffer([])
      put_buffer var!(buffer, Xml), "<?xml version=\"1.0\"?>"
      unquote(block)
      result = render(var!(buffer, Xml))
      :ok = stop_buffer(var!(buffer, Xml))
      result
    end
  end

  defmacro tag(name, attrs \\ [], do: inner) do
    quote do
      put_buffer var!(buffer, Xml), open_tag(unquote_splicing([name, attrs]))
      unquote(inner)
      put_buffer var!(buffer, Xml), "</#{unquote(name)}>"
    end
  end

  def open_tag(name, []), do: "<#{name}>"
  def open_tag(name, attrs) do
    attr_text = for {k, v} <- attrs, into: "", do: " #{k}=\"#{v}\""
    "<#{name}#{attr_text}>"
  end

  defmacro text(string) do
    quote do: put_buffer(var!(buffer, Xml), to_string(unquote(string)))
  end

end
