defmodule KV do

  def start_link do
    Agent.start_link(&HashDict.new/0, name: __MODULE__)
  end

  def get(key) do
    Agent.get(__MODULE__, &(HashDict.get(&1, key)))
  end

  def put(key, value) do
    Agent.update(__MODULE__, &(HashDict.put(&1, key, value)))
  end

end
