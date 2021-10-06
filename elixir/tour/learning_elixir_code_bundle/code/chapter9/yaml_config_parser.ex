defmodule YamlConfigParser do
  @behaviour ConfigParser

  def parse(str), do: str

  def extensions(), do: ["yaml", "yml"]

end
