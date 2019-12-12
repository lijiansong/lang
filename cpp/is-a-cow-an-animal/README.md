## Is a Cow an Animal?

From these examples, Pixel try to extract a real problem which "Is a Cow an Animal?" is trying to solve.

**Goal #1**

Implement the rules below, rejecting at runtime *any* malformed program.

**Goal #2**

Try to enforce the rules at compile-time,
this can be:

- quite easy (eg: ensuring one doesn't feed carrots with grass),
- quite hard (eg: ensuring one doesn't feed cows with carrots or dead_rabbits),
- or very hard (eg: ensuring meat can be eaten only once)

===============

## Description of the World
- everything has some amount of energy
- there are animals: cow, rabbit, human
- there is food:
  - vegetable: grass, carrot
  - meat: beef, dead_rabbit, dead_human

general rules:

- animals can eat some food, their energy is raised by the food's energy amount
- animals can be slaughtered, the result is meat ; the energy of the meat is the same as the energy of the animal
- there should be a way to handle a list of animals and the energy of each animal
- slaughtered animals can't eat anymore nor be slaughtered again
- meat can be eaten only once
- whereas vegetable is innumerable and can be eaten more than once

animals' accepted food:

- a cow only eats grass
- a rabbit only eats carrots
- a human eats carrots and **any** meat

IMPORTANT: feeding a cow with something else than grass is a fatal error (same for feeding a human with grass...)

when slaughtered:

- a cow becomes beef
- a rabbit becomes dead_rabbit
- a human becomes dead_human


TODO: Try to re-implement this problem.

## REFs

- <http://rigaux.org/language-study/various/is-a-cow-an-animal/>
