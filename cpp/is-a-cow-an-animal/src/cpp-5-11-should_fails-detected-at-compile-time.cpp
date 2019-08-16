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
  bool innumerable;
  string name;
  int energy;

  Food() {}

  Food(bool innumerable, string name, int energy)
      : valid(true), innumerable(innumerable), name(name), energy(energy) {}

  int eaten() {
    if (!valid)
      mythrow("bad food");
    if (!innumerable)
      valid = false;
    return energy;
  }
};

struct Animal {
  bool valid;
  string name;
  int energy;
  string when_slaughtered;
  bool (*food_accepted)(string);

  Animal() {}

  Animal(string name, int energy, string when_slaughtered,
         bool (*food_accepted)(string))
      : name(name), energy(energy), when_slaughtered(when_slaughtered),
        food_accepted(food_accepted) {}

  void eat(Food &food) {
    if (!valid)
      mythrow("bad animal");

    if (food_accepted(food.name))
      energy += food.eaten();
    else
      mythrow(name + " doesn't accept food " + food.name);
  }

  Food *slaughter() {
    if (!valid)
      mythrow("bad animal");

    valid = false;

    return new Food(false, when_slaughtered, energy);
  }
};

bool is_meat(string s) {
  return s == "beef" || s == "dead_rabbit" || s == "dead_human";
}

bool is_grass(string s) { return s == "grass"; }
bool is_carrot(string s) { return s == "carrot"; }
bool is_human_eatable(string s) { return s == "carrot" || is_meat(s); }

Food new_grass(int energy) { return Food(true, "grass", energy); }
Food new_carrot(int energy) { return Food(true, "carrot", energy); }

Animal new_cow(int energy) { return Animal("cow", energy, "beef", is_grass); }
Animal new_rabbit(int energy) {
  return Animal("rabbit", energy, "dead_rabbit", is_carrot);
}
Animal new_human(int energy) {
  return Animal("human", energy, "dead_human", is_human_eatable);
}

Food grass, carrot, a_beef, a_dead_rabbit;
Animal a_rabbit, a_cow, a_human, another_human;

void should_work() {
  grass = new_grass(5);
  carrot = new_carrot(10);

  a_rabbit = new_rabbit(100);
  a_cow = new_cow(1000);
  a_human = new_human(300);
  another_human = new_human(350);

  {
    vector<Animal> animals;
    animals.push_back(a_rabbit);
    animals.push_back(a_cow);
    animals.push_back(a_human);
    for (vector<Animal>::const_iterator p = animals.begin(); p != animals.end();
         p++)
      cout << p->name << " -> " << p->energy << "\n";
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
5 should_fail's are detected at compile-time:

new_cow(10).slaughter().eat(grass); //=> no matching function for call to
`Food::eat (Food &)' new_cow(10).slaughter().slaughter(); //=> no matching
function for call to `Food::slaughter ()' carrot.eat(grass); //=> no matching
function for call to `Food::eat (Food &)' carrot.slaughter(); //=> no matching
function for call to `Food::slaughter ()' a_human.eat(new_cow(10)); //=> no
matching function for call to `Animal::eat (Animal)' candidates are: void
Animal::eat (Food)
*/

void fail06() { new_cow(10).eat(carrot); } // cow do not eat carrot
void fail07() {
  new_cow(10).eat(*new_cow(10).slaughter());
} // cow do not eat beef
void fail08() { a_human.eat(grass); }  // human do not eat grass
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
  must_fail(fail06);
  must_fail(fail07);
  must_fail(fail08);
  must_fail(fail09);
  must_fail(fail10);
  must_fail(fail11);
}

int main() {
  should_work();
  should_fail();
  cerr << "all is ok\n";
}
