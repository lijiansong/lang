defmodule MyIf do

  def if(condition, clauses) do
    do_clause = Keyword.get(clauses, :do, nil)
    else_clause = Keyword.get(clauses, :else, nil)
    case condition do
      val when val in [false, nil] ->
        else_clause
      _ -> do_clause
    end
  end

end
