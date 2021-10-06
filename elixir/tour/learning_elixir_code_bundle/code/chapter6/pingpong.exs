defmodule PingPong do

  def start_link do
    spawn_link(fn -> loop() end)
  end

  defp loop do
    receive do
      {:ping, sender} ->
        send sender, {:pong, self()}
      {:pong, sender} ->
        IO.puts("Received :pong")
    end
  end
end
