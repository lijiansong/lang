defmodule WorkpoolSchedulerTest do
  use ExUnit.case, async: false

  setup do
    scheduler = Workpool.Scheduler.start_link
    on_exit(scheduler, fn ->
      Application.stop(scheduler)
      :timer.sleep(100)
    end)
    {:ok, scheduler: scheduler}
  end

end
