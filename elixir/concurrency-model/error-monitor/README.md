for `cache.ex`:


```
$ elixirc cache.ex
$ iex
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> Cache.start_link
#PID<0.107.0>
iex(2)> Cache.put("huawei.com", "Welcome to HUAWEI!!!")
{:put, "huawei.com", "Welcome to HUAWEI!!!"}
iex(3)> Cache.get("huawei.com")
"Welcome to HUAWEI!!!"
iex(4)> Cache.size
20
iex(5)> Cache.put("alibaba.com", nil)
** (EXIT from #PID<0.105.0>) shell process exited with reason: an exception was raised:
    ** (ArgumentError) errors were found at the given arguments:

  * 1st argument: not a bitstring

        :erlang.byte_size(nil)
        cache.ex:35: Cache.loop/2

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)>
00:08:22.415 [error] Process #PID<0.107.0> raised an exception
** (ArgumentError) errors were found at the given arguments:

  * 1st argument: not a bitstring

    :erlang.byte_size(nil)
    cache.ex:35: Cache.loop/2

nil
```

`将错误处理隔离到一个管理进程中`。

for `link.ex`:

```
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> pid1=spawn(&LinkTest.loop/0)
#PID<0.107.0>
iex(2)> pid2=spawn(&LinkTest.loop/0)
#PID<0.109.0>
iex(3)> send(pid1, {:link_to, pid2})
{:link_to, #PID<0.109.0>}
iex(4)> send(pid2, {:exit_because, :bad_thing_happend})
{:exit_because, :bad_thing_happend}
iex(5)> Process.info(pid1)
nil
iex(6)> Process.info(pid2)
nil
iex(7)>
```

链接是双向的：

```
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> pid1=spawn(&LinkTest.loop/0)
#PID<0.107.0>
iex(2)> pid2=spawn(&LinkTest.loop/0)
#PID<0.109.0>
iex(3)> send(pid1, {:link_to, pid2})
{:link_to, #PID<0.109.0>}
iex(4)> send(pid1, {:exit_because, :bad_thing_happend})
{:exit_because, :bad_thing_happend}
iex(5)> Process.info(pid1)
nil
iex(6)> Process.info(pid2)
nil
iex(7)>
```

正常终止：

```
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> pid1=spawn(&LinkTest.loop/0)
#PID<0.107.0>
iex(2)> pid2=spawn(&LinkTest.loop/0)
#PID<0.109.0>
iex(3)> send(pid1, {:link_to, pid2})
{:link_to, #PID<0.109.0>}
iex(4)> send(pid2, {:exit_because, :normal})
{:exit_because, :normal}
iex(5)> Process.info(pid1)
[
  current_function: {LinkTest, :loop, 0},
  initial_call: {:erlang, :apply, 2},
  status: :waiting,
  message_queue_len: 0,
  links: [],
  dictionary: [],
  trap_exit: false,
  error_handler: :error_handler,
  priority: :normal,
  group_leader: #PID<0.65.0>,
  total_heap_size: 233,
  heap_size: 233,
  stack_size: 4,
  reductions: 17,
  garbage_collection: [
    max_heap_size: %{error_logger: true, kill: true, size: 0},
    min_bin_vheap_size: 46422,
    min_heap_size: 233,
    fullsweep_after: 65535,
    minor_gcs: 0
  ],
  suspending: []
]
iex(6)> Process.info(pid2)
nil
iex(7)>
```

系统进程：

```
Erlang/OTP 24 [erts-12.0.3] [source] [64-bit] [smp:8:8] [ds:8:8:10] [async-threads:1] [jit] [dtrace]

Interactive Elixir (1.12.2) - press Ctrl+C to exit (type h() ENTER for help)
iex(1)> pid2=spawn(&LinkTest.loop/0)
#PID<0.107.0>
iex(2)> pid1=spawn(&LinkTest.loop_system/0)
#PID<0.109.0>
iex(3)> send(pid1, {:link_to, pid2})
{:link_to, #PID<0.107.0>}
iex(4)> send(pid2, {:exit_because, :yet_another_bad_thing_happended})
#PID<0.107.0> exited because yet_another_bad_thing_happended
{:exit_because, :yet_another_bad_thing_happended}
iex(5)> Process.info(pid2)
nil
iex(6)> Process.info(pid1)
[
  current_function: {LinkTest, :loop, 0},
  initial_call: {:erlang, :apply, 2},
  status: :waiting,
  message_queue_len: 0,
  links: [],
  dictionary: [],
  trap_exit: true,
  error_handler: :error_handler,
  priority: :normal,
  group_leader: #PID<0.65.0>,
  total_heap_size: 237,
  heap_size: 233,
  stack_size: 4,
  reductions: 99,
  garbage_collection: [
    max_heap_size: %{error_logger: true, kill: true, size: 0},
    min_bin_vheap_size: 46422,
    min_heap_size: 233,
    fullsweep_after: 65535,
    minor_gcs: 0
  ],
  suspending: []
]
iex(7)>
```
