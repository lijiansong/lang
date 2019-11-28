#ifndef TURING_HPP
#define TURING_HPP

#ifndef TYPELIST_HPP
#define TYPELIST_HPP

#ifndef CONDITIONAL_HPP
#define CONDITIONAL_HPP

template <bool C, typename A, typename B> struct Conditional {
  typedef A type;
};

template <typename A, typename B> struct Conditional<false, A, B> {
  typedef B type;
};

#endif
// this ones only purpose is to store a template parameter list. it does not
// have a definition, because it will never be instantiated
template <typename...> struct ParameterPack;
#ifndef ENABLE_IF_HPP
#define ENABLE_IF_HPP

template <bool C, typename = void> struct EnableIf { /* no typedef here */
};

template <typename Type> struct EnableIf<true, Type> { typedef Type type; };

#endif
#ifndef IDENTIFY_HPP
#define IDENTIFY_HPP

template <typename T> struct Identity { typedef T type; };

#endif

// define a type list
template <typename...> struct TypeList;

template <typename T, typename... TT> struct TypeList<T, TT...> {
  typedef T type;
  typedef TypeList<TT...> tail;
};

template <> struct TypeList<> {};

// the following functions returns the size of a list
template <typename List> struct GetSize;

template <typename... Items> struct GetSize<TypeList<Items...>> {
  enum { value = sizeof...(Items) };
};

// the following meta-function smelts TypeLists together into one list
template <typename... T> struct ConcatList;

template <typename... First, typename... Second, typename... Tail>
struct ConcatList<TypeList<First...>, TypeList<Second...>, Tail...> {
  typedef
      typename ConcatList<TypeList<First..., Second...>, Tail...>::type type;
};

template <typename T> struct ConcatList<T> { typedef T type; };

// appends an item to a list
template <typename NewItem, typename List> struct AppendItem;

template <typename NewItem, typename... Items>
struct AppendItem<NewItem, TypeList<Items...>> {
  typedef TypeList<Items..., NewItem> type;
};

// prepends an item to a list
template <typename NewItem, typename List> struct PrependItem;

template <typename NewItem, typename... Items>
struct PrependItem<NewItem, TypeList<Items...>> {
  typedef TypeList<NewItem, Items...> type;
};

// gets the item on the Nth position
template <typename List, int N, typename = void> struct GetItem {
  static_assert(N > 0, "index cannot be negative");
  static_assert(GetSize<List>::value > 0, "index too high");
  typedef typename GetItem<typename List::tail, N - 1>::type type;
};

template <typename List> struct GetItem<List, 0> {
  static_assert(GetSize<List>::value > 0, "index too high");
  typedef typename List::type type;
};

// finds an item using a Matcher policy
template <typename List, template <typename, typename...> class Matcher,
          typename... Keys>
struct FindItem {
  static_assert(GetSize<List>::value > 0, "Could not match any item.");
  typedef typename List::type current_type;
  typedef typename Conditional<
      Matcher<current_type, Keys...>::value,
      Identity<current_type>, // found!
      FindItem<typename List::tail, Matcher, Keys...>>::type::type type;
};

// replaces one item at a certain index I
template <typename List, int I, typename NewItem> struct ReplaceItem {
  static_assert(I > 0, "index cannot be negative");
  static_assert(GetSize<List>::value > 0, "index too high");
  typedef typename PrependItem<typename List::type,
                               typename ReplaceItem<typename List::tail, I - 1,
                                                    NewItem>::type>::type type;
};

template <typename NewItem, typename Type, typename... T>
struct ReplaceItem<TypeList<Type, T...>, 0, NewItem> {
  typedef TypeList<NewItem, T...> type;
};

#endif
#ifndef RULE_HPP
#define RULE_HPP

// one rule definition

// direction either right or left
enum Direction { Left = -1, Right = 1 };

template <typename OldState, typename Input, typename NewState, typename Output,
          Direction Move>
struct Rule {
  typedef OldState old_state;
  typedef Input input;
  typedef NewState new_state;
  typedef Output output;
  static Direction const direction = Move;
};

#endif

#ifndef IS_SAME_HPP
#define IS_SAME_HPP

template <typename A, typename B> struct IsSame {
  enum { value = false };
};

template <typename A> struct IsSame<A, A> {
  enum { value = true };
};

#endif
#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

/*
 * This struct represents the configuration of one turing machine
 * at one time.
 */
template <typename Input, typename State, int Position> struct Configuration {
  typedef Input input;
  typedef State state;
  enum { position = Position };
};

#endif
#ifndef MAX_HPP
#define MAX_HPP

template <int A, int B> struct Max {
  enum { value = A > B ? A : B };
};

#endif

// building block for one state
template <int n> struct State {
  enum { value = n };

  // name of the state
  static char const *name;
};

template <int n> char const *State<n>::name = "unnamed";

/*
 * Two predefined states
 */
struct QAccept {
  enum { value = -1 };
  static char const *name;
};

struct QReject {
  enum { value = -2 };
  static char const *name;
};

// building blocks for our input
template <int n> struct Input {
  enum { value = n };

  // name of the input
  static char const *name;

  template <int... I> struct Generate { typedef TypeList<Input<I>...> type; };
};

template <int n> char const *Input<n>::name = "unnamed";

/*
 * one predefined input
 */
typedef Input<-1> InputBlank;

template <typename Config, typename Transitions, typename = void>
struct Controller {
  // some parameters that we do expose
  typedef Config config;
  enum { position = config::position };
  typedef
      typename Conditional<static_cast<int>(
                               GetSize<typename config::input>::value) <=
                               static_cast<int>(position),
                           AppendItem<InputBlank, typename config::input>,
                           Identity<typename config::input>>::type::type input;
  typedef typename config::state state;

  // input cell that the head is over
  typedef typename GetItem<input, position>::type cell;

  // the rule we now gonna take. we use a matcher template to find the rule
  template <typename Item, typename State, typename Cell> struct Matcher {
    typedef typename Item::old_state checking_state;
    typedef typename Item::input checking_input;
    enum {
      value = IsSame<State, checking_state>::value &&
              IsSame<Cell, checking_input>::value
    };
  };
  typedef typename FindItem<Transitions, Matcher, state, cell>::type rule;

  // define the new parameters passed to the next recursion step
  typedef typename ReplaceItem<input, position, typename rule::output>::type
      new_input;
  typedef typename rule::new_state new_state;
  typedef Configuration<new_input, new_state,
                        Max<position + rule::direction, 0>::value>
      new_config;

  typedef Controller<new_config, Transitions> next_step;
  typedef typename next_step::end_config end_config;
  typedef typename next_step::end_input end_input;
  typedef typename next_step::end_state end_state;
  enum { end_position = next_step::position };
};

template <typename Input, typename State, int Position, typename Transitions>
struct Controller<Configuration<Input, State, Position>, Transitions,
                  typename EnableIf<IsSame<State, QAccept>::value ||
                                    IsSame<State, QReject>::value>::type> {
  typedef Configuration<Input, State, Position> config;
  enum { position = config::position };
  typedef
      typename Conditional<static_cast<int>(
                               GetSize<typename config::input>::value) <=
                               static_cast<int>(position),
                           AppendItem<InputBlank, typename config::input>,
                           Identity<typename config::input>>::type::type input;
  typedef typename config::state state;

  // yeah, we are at the end!
  typedef config end_config;
  typedef input end_input;
  typedef state end_state;
  enum { end_position = position };
};

/*
 * accepts an input-typelist, the transitions type-list, and the start-state
 * type.
 */
template <typename Input, typename Transitions, typename StartState>
struct TuringMachine {
  typedef Input input;
  typedef Transitions transitions;
  typedef StartState start_state;

  // will either become QAccept or QReject depending on the rules
  typedef Controller<Configuration<Input, StartState, 0>, Transitions>
      controller;
  typedef typename controller::end_config end_config;
  typedef typename controller::end_input end_input;
  typedef typename controller::end_state end_state;
  enum { end_position = controller::end_position };
};

#endif
#ifndef PRINTER_HPP
#define PRINTER_HPP

#include <ostream>

template <typename Rule> struct RulePrinter {
  typedef typename Rule::old_state old_state;
  typedef typename Rule::input input;
  typedef typename Rule::new_state new_state;
  typedef typename Rule::output output;
  static Direction const direction = Rule::direction;

  static void print_dot(std::ostream &os) {
    os << old_state::name << " -> " << new_state::name;
    os << " [ label = \"" << input::name << " -> " << output::name << ','
       << (direction == Left ? "L" : "R") << "\" ];\n";
  }
};

template <typename Transitions> struct TransitionsPrinter {
  typedef Transitions transitions;
  static void print_dot(std::ostream &os) {
    RulePrinter<typename transitions::type>::print_dot(os);
    TransitionsPrinter<typename transitions::tail>::print_dot(os);
  }
};

template <> struct TransitionsPrinter<TypeList<>> {
  static void print_dot(std::ostream &os) {
    // empty
  }
};

enum { LeftToRight, TopToBottom };

template <typename Turing> struct DiagramPrinter {
  typedef typename Turing::input input;
  typedef typename Turing::transitions transitions;
  typedef typename Turing::start_state start_state;

  // runtime stuff
  static void print_dot(std::ostream &os, int rank_dir) {
    char const *rank_codes[] = {"LR", "TB"};
    if (rank_dir < 0 || rank_dir >= sizeof rank_codes / sizeof *rank_codes)
      return;
    os << "digraph finite_state_machine {\n";
    os << "rankdir=" << rank_codes[rank_dir] << ";\n";
    os << "node [shape = circle];\n";
    TransitionsPrinter<transitions>::print_dot(os);
    os << "}" << std::endl;
  }
};

#endif

template <> char const *Input<-1>::name = "_";

char const *QAccept::name = "qaccept";
char const *QReject::name = "qreject";

#include <iostream>

int main() {
  typedef Input<1> x;
  x::name = "x";
  typedef Input<2> x_mark;
  x_mark::name = "x_mark";
  typedef Input<3> split;
  split::name = "split";
  typedef State<0> start;
  start::name = "start";
  typedef State<1> find_blank;
  find_blank::name = "find_blank";
  typedef State<2> go_back;
  go_back::name = "go_back";

  // syntax: Rule< State, Input, NewState, Output, Move >
  typedef TypeList<Rule<start, x, find_blank, x_mark, Right>,
                   Rule<find_blank, x, find_blank, x, Right>,
                   Rule<find_blank, split, find_blank, split, Right>,
                   Rule<find_blank, InputBlank, go_back, x, Left>,
                   Rule<go_back, x, go_back, x, Left>,
                   Rule<go_back, split, go_back, split, Left>,
                   Rule<go_back, x_mark, start, x, Right>,
                   Rule<start, split, QAccept, split, Left>>
      rules;

  typedef TuringMachine<TypeList<x, x, x, x, split>, rules, start> double_it;
  static_assert(IsSame<double_it::end_input,
                       TypeList<x, x, x, x, split, x, x, x, x>>::value,
                "Hmm... This is borky!");

  DiagramPrinter<double_it>::print_dot(std::cout, LeftToRight);
}
