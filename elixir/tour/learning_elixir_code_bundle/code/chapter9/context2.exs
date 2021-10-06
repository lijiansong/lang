defmodule MacroContext do
  defmacro info do
    IO.puts "Macro context: (#{__MODULE__})"

    quote do
      IO.puts "Caller context: (#{__MODULE__})"

      def some_info do
        IO.puts """
        I am #{__MODULE__} and I come with the following:
        #{inspect __info__(:functions)}
        """
      end
    end
  end
end

defmodule MyModule do
  require MacroContext
  MacroContext.info
end
