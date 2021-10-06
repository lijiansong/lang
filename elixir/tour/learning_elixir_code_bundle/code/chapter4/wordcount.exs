"The quick brown fox jumped over the lazy dog" |>
String.split(" ") |>
Enum.map(&String.upcase/1) |>
Enum.map fn(x) -> {x, 1} end |>

