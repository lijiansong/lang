for `counter.ex`:


```
$ elixirc counter.ex
$ iex
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> counter=Counter.start(10)
#PID<0.107.0>
iex(2)> Counter.next(counter)
Current count: 10
{:next}
iex(3)> Counter.next(counter)
Current count: 11
{:next}
iex(4)> Counter.next(counter)
Current count: 12
{:next}
iex(5)>
```

for `counter2.ex`:

```
$ elixirc counter.ex
$ iex
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> counter = Counter.start(10)
#PID<0.107.0>
iex(2)> Counter.next(counter)
10
iex(3)> Counter.next(counter)
11
iex(4)> Counter.next(counter)
12
iex(5)> pid = Counter.start(13)
#PID<0.112.0>
iex(6)> Process.register(pid, :count)
true
iex(7)> count=Process.whereis(:count)
#PID<0.112.0>
iex(8)> count
count      counter
iex(8)> Counter.next(count)
13
iex(9)> Counter.next(count)
14
iex(10)> Counter.next(count)
15
iex(11)> Process.registered
[:logger_sup, :erts_code_purger, IEx.Pry, :kernel_sup, :standard_error,
 :erl_signal_server, :logger_proxy, :erl_prim_loader, IEx.Config,
 :socket_registry, :kernel_refc, Logger.BackendSupervisor, :inet_db, :init,
 IEx.Broker, :elixir_sup, :logger_handler_watcher, :code_server, :logger,
 :user_drv, :user, :elixir_config, :global_name_server, :application_controller,
 :kernel_safe_sup, IEx.Supervisor, Logger, :standard_error_sup, :rex,
 :global_group, :elixir_code_server, Logger.Supervisor, :count, :file_server_2]
iex(12)>
```

for `counter3.ex`:

```
$ elixirc counter.ex
$ iex
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> Counter.start(10)
#PID<0.107.0>
iex(2)> Counter.next
10
iex(3)> Counter.next
11
iex(4)> Counter.next
12
iex(5)> Counter.next
13
iex(6)>
```

for `parallel.ex`:

```
$ elixirc parallel.ex
$ iex
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> slow_double = fn(x) -> :timer.sleep(1000); x * 2 end
#Function<44.40011524/1 in :erl_eval.expr/5>
iex(2)> :timer.tc(fn() -> Enum.map([1, 2, 3, 4], slow_double) end)
{4003349, [2, 4, 6, 8]}
iex(3)> :timer.tc(fn() -> Parallel.map([1, 2, 3, 4], slow_double) end)
{1000633, [2, 4, 6, 8]}
iex(4)>
```

