defmodule ControlFlow do
  defmacro unless(condition, clauses) do
    true_clause = Keyword.get(clauses, :do, nil)
    false_clause = Keyword.get(clauses, :else, nil)
    quote do
      if not unquote(condition) do
        unquote(true_clause)
      else
        unquote(false_clause)
      end
    end
  end
end
