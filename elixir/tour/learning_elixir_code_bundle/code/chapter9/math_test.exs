ExUnit.start
Code.require_file("math.exs", __DIR__)

defmodule MathTest do
  use ExUnit.Case
  import Math

  test "basic test" do
    assert 100 == square(10)
  end

  test "correct order of operations" do
    assert 2/100 == 2 / square(10)
  end

  test "correct evaluation of passed expressions" do
    assert 4 == square(1 + 1)
  end

  test "evaluates passed expression once" do
    assert 256 == square((fn() -> send(self, :square); 16 end).())
    assert_received :square
    refute_received :square
  end

end
