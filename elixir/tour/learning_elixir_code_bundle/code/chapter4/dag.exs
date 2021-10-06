dag = [a: {:b, :c}, b: {:c, :d}, c: {:e}, d: {:e}, e: {}]

dag |>
Enum.map(fn({node, neighbors}) ->
  neighbors |> Tuple.to_list |> Enum.map(fn(child) -> {child, node} end) end)
  |> List.flatten |>
(fn(nodes) -> {nodes |> Keyword.keys |> Enum.uniq, nodes} end).() |>
(fn({keys, nodes}) -> keys |>
                      Enum.map(fn(key) ->
                        {key, nodes |>
                              Keyword.get_values(key) |>
                              List.to_tuple} end)
 end).()
