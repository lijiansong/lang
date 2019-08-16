// -*- C++ -*-

#include <iostream>
#include <string>
#include <typeinfo>
#include <vector>

using namespace std;

void mythrow(string s) {
  cerr << "error: " << s << "\n";
  throw(s);
}

template <class Eaters> struct Food {
  int energy;

  Food(int energy) : energy(energy) {}

  virtual int eaten() { return energy; }
};

template <class Eaters> struct Meat : Food<Eaters> {
  int valid;

  Meat(int energy) : Food<Eaters>(energy), valid(true) {}

  virtual int eaten() {
    if (!valid)
      mythrow("bad food");
    valid = false;
    return this->Food<Eaters>::eaten();
  }
};

struct Any_animal {
  int energy;
  Any_animal(int energy) : energy(energy) {}
};

template <class My_kind, class When_slaughtered> struct Animal : Any_animal {
  bool valid;
  When_slaughtered *(*when_slaughtered)(int);

  Animal(int energy, When_slaughtered *(*when_slaughtered)(int))
      : Any_animal(energy), when_slaughtered(when_slaughtered) {}

  template <class Kind> void eat(Food<Kind> &food) {
    // FIXME: in clang this build will fail
    (void)static_cast<My_kind *>((Kind *)0);
    if (!valid)
      mythrow("bad animal");
    energy += food.eaten();
  }

  When_slaughtered *slaughter() {
    if (!valid)
      mythrow("bad animal");
    valid = false;
    return when_slaughtered(energy);
  }
};

class Human_kind {};
class Rabbit_kind {};
class Cow_kind {};
class Human_or_rabbit_kind : Human_kind, Rabbit_kind {};
class Meat_eaters : Human_kind {};

struct Carrot : Food<Human_or_rabbit_kind> {
  Carrot(int energy) : Food<Human_or_rabbit_kind>(energy) {}
};
struct Grass : Food<Cow_kind> {
  Grass(int energy) : Food<Cow_kind>(energy) {}
};

struct Beef : Meat<Meat_eaters> {
  Beef(int energy) : Meat<Meat_eaters>(energy) {}
};
struct Dead_rabbit : Meat<Meat_eaters> {
  Dead_rabbit(int energy) : Meat<Meat_eaters>(energy) {}
};
struct Dead_human : Meat<Meat_eaters> {
  Dead_human(int energy) : Meat<Meat_eaters>(energy) {}
};

Beef *new_beef(int energy) { return new Beef(energy); }
Dead_rabbit *new_dead_rabbit(int energy) { return new Dead_rabbit(energy); }
Dead_human *new_dead_human(int energy) { return new Dead_human(energy); }

struct Cow : Animal<Cow_kind, Beef> {
  Cow(int energy) : Animal<Cow_kind, Beef>(energy, &new_beef) {}
};
struct Rabbit : Animal<Rabbit_kind, Dead_rabbit> {
  Rabbit(int energy)
      : Animal<Rabbit_kind, Dead_rabbit>(energy, &new_dead_rabbit) {}
};
struct Human : Animal<Human_kind, Dead_human> {
  Human(int energy) : Animal<Human_kind, Dead_human>(energy, &new_dead_human) {}
};

Grass grass(0);
Carrot carrot(0);
Beef a_beef(0);
Dead_rabbit a_dead_rabbit(0);
Rabbit a_rabbit(0);
Cow a_cow(0);
Human a_human(0), another_human(0);

void should_work() {
  grass = Grass(5);
  carrot = Carrot(10);

  a_rabbit = Rabbit(100);
  a_cow = Cow(1000);
  a_human = Human(300);
  another_human = Human(350);

  {
    vector<string> names;
    vector<Any_animal> animals;
    names.push_back("rabbit");
    animals.push_back(a_rabbit);
    names.push_back("cow");
    animals.push_back(a_cow);
    names.push_back("human");
    animals.push_back(a_human);
    vector<Any_animal>::const_iterator p;
    vector<string>::const_iterator q;
    for (p = animals.begin(), q = names.begin(); p != animals.end(); p++, q++)
      cout << *q << " -> " << p->energy << "\n";
  }

  a_rabbit.eat(carrot);
  a_cow.eat(grass);

  a_dead_rabbit = *a_rabbit.slaughter();
  a_beef = *a_cow.slaughter();

  a_human.eat(carrot);
  a_human.eat(carrot);
  a_human.eat(a_beef);
  a_human.eat(a_dead_rabbit);

  a_human.eat(*another_human.slaughter());

  if (a_human.energy != 1785)
    mythrow("failed");
}

/*
7 should_fail's are detected at compile-time:

Cow(10).slaughter().eat(grass); //=> request for member `eat' in ... which is of
non-aggregate type `Beef *' Cow(10).slaughter().slaughter(); //=> request for
member `slaughter' in ... which is of non-aggregate type `Beef *'
carrot.eat(grass); //=> no matching function for call to `Carrot::eat (Grass &)'
carrot.slaughter(); //=> no matching function for call to `Carrot::slaughter ()'
a_human.eat(Cow(10)); //=> no matching function for call to `Human::eat (Cow)'
candidates are: ... Cow(10).eat(carrot); //=> no matching function for call to
`Cow::eat (Carrot &)' candidates are: ... Cow(10).eat(*Cow(10).slaughter());
//=> no matching function for call to `Cow::eat (Beef &)' candidates are: ...

a_human.eat(grass); //=> invalid static_cast from type `Cow_kind *' to type
`Human_kind *'

*/

void fail09() { a_human.eat(a_beef); } // a_beef is already eaten
void fail10() { a_cow.eat(grass); }    // a_cow is dead, it can't eat
void fail11() {
  a_cow.slaughter();
} // a_cow is dead, it can't be slaughtered again

void must_fail(void (*f)()) {
  bool ok = false;
  try {
    f();
  } catch (string e) {
    ok = true;
  }
  if (!ok)
    mythrow("must_fail failed");
}

void should_fail() {
  must_fail(fail09);
  must_fail(fail10);
  must_fail(fail11);
}

int main() {
  should_work();
  should_fail();
  cerr << "all is ok\n";
}
