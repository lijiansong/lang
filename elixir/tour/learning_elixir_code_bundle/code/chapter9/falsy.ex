defprotocol Falsy do
  def falsy?(data)
end

defimpl Falsy, for: Atom do
  def falsy?(false), do: true
  def falsy?(nil), do: true
  def falsy?(_), do: false
end

defimpl Falsy, for: Integer do
  def falsy?(0), do: true
  def falsy?(_), do: false
end

defimpl Falsy, for: List do
  def falsy?([]), do: true
  def falsy?(_), do: false
end

defimpl Falsy, for: Map do
  def falsy?(map), do: map_size(map) == 0
end
