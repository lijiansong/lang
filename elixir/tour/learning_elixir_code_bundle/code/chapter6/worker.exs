defmodule Worker do

  def do_work() do
    receive do
      {:compute, x, pid} ->
        send pid, {:result, x * x}
    end
    do_work()
  end
end
