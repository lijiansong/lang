defmodule ControlFlow do
  defmacro unless(condition, clauses) do
    true_clause = Keyword.get(clauses, :do, nil)
    false_clause = Keyword.get(clauses, :else, nil)
    quote do
      case not unquote(condition) do
        val when val in [false, nil] -> unquote(true_clause)
        _ -> unquote(false_clause)
      end
    end
  end
end
