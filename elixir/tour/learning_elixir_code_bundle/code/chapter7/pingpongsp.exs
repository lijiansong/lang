defmodule PingPong do

  def start_link(opts \\ []) do
    :proc_lib.start_link(__MODULE__, :init, [self(), opts])
  end

  def init(parent, opts) do
    Process.register(self(), __MODULE__)
    debug = :sys.debug_options([])
    Process.link(parent)
    :proc_lib.init_ack(parent, {:ok, self()})
    state = HashDict.new
    loop(state, parent, debug)
  end

  def ping() do
    send __MODULE__, {:ping, self()}
    receive do
      {:reply, response} ->
        response
    after 10000 ->
      {:error, :timeout}
    end
  end

  defp loop(state, parent, debug) do
    receive do
      {:ping, from} ->
        send from, {:reply, :pong}
      {:system, from, request} ->
        :sys.handle_system_msg(request, from, parent, __MODULE__, debug, state)
    end
    loop(state, parent, debug)
  end

  def system_continue(parent, debug, state) do
    loop(state, parent, debug)
  end

  def system_terminate(reason, _, _, _) do
    exit(reason)
  end

  def system_get_state(state) do
    {:ok, state}
  end

end
