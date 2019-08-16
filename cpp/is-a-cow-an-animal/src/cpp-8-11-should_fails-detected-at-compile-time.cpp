// -*- C++ -*-

#include <iostream>
#include <string>
#include <vector>

using namespace std;

void mythrow(string s) {
  cerr << "error: " << s << "\n";
  throw(s);
}

struct Food {
  bool valid;
  int energy;

  Food(int energy) : valid(true), energy(energy) {}

  virtual bool is_innumerable() = 0;

  virtual int eaten() {
    if (!valid)
      mythrow("bad food");
    if (!is_innumerable())
      valid = false;
    return energy;
  }
};

struct Any_animal {
  int energy;
};

template <class When_slaughtered, class Accepted_food>
struct Animal : Any_animal {
  bool valid;
  int energy;
  When_slaughtered *(*when_slaughtered)(int);

  Animal(int energy_, When_slaughtered *(*when_slaughtered)(int))
      : when_slaughtered(when_slaughtered) {
    energy = energy_;
  }

  void eat(Accepted_food &food) {
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

struct Carrots_or_Meat : virtual Food {
  Carrots_or_Meat(int energy) : Food(energy) {}
};

struct Vegetable : virtual Food {
  Vegetable(int energy) : Food(energy) {}
  bool is_innumerable() { return true; }
};
struct Meat : Carrots_or_Meat {
  Meat(int energy) : Carrots_or_Meat(energy), Food(energy) {}
  bool is_innumerable() { return false; }
};

struct Carrot : Carrots_or_Meat, Vegetable {
  Carrot(int energy)
      : Carrots_or_Meat(energy), Vegetable(energy), Food(energy) {}
};
struct Grass : Vegetable {
  Grass(int energy) : Vegetable(energy), Food(energy) {}
};

struct Beef : Meat {
  Beef(int energy) : Meat(energy), Food(energy) {}
};
struct Dead_rabbit : Meat {
  Dead_rabbit(int energy) : Meat(energy), Food(energy) {}
};
struct Dead_human : Meat {
  Dead_human(int energy) : Meat(energy), Food(energy) {}
};

Beef *new_beef(int energy) { return new Beef(energy); }
Dead_rabbit *new_dead_rabbit(int energy) { return new Dead_rabbit(energy); }
Dead_human *new_dead_human(int energy) { return new Dead_human(energy); }

struct Cow : Animal<Beef, Grass> {
  Cow(int energy) : Animal<Beef, Grass>(energy, &new_beef) {}
};
struct Rabbit : Animal<Dead_rabbit, Carrot> {
  Rabbit(int energy) : Animal<Dead_rabbit, Carrot>(energy, &new_dead_rabbit) {}
};
struct Human : Animal<Dead_human, Carrots_or_Meat> {
  Human(int energy)
      : Animal<Dead_human, Carrots_or_Meat>(energy, &new_dead_human) {}
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

  cout << a_human.energy << "\n";

  if (a_human.energy != 1785)
    mythrow("failed");
}

/*
8 should_fail's are detected at compile-time:

Cow(10).slaughter().eat(grass); //=> request for member `eat' in ... which is of
non-aggregate type `Beef *' Cow(10).slaughter().slaughter(); //=> request for
member `slaughter' in ... which is of non-aggregate type `Beef *'
carrot.eat(grass); //=> no matching function for call to `Carrot::eat (Grass &)'
carrot.slaughter(); //=> no matching function for call to `Carrot::slaughter ()'
a_human.eat(Cow(10)); //=> no matching function for call to `Human::eat (Cow)'
candidates are: ... Cow(10).eat(carrot); //=> no matching function for call to
`Cow::eat (Carrot &)' candidates are: ... Cow(10).eat(*Cow(10).slaughter());
//=> no matching function for call to `Cow::eat (Beef &)' candidates are: ...
a_human.eat(grass); //=> no matching function for call to `Human::eat (Grass &)'
candidates are: ...
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
