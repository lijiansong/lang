#include "house.h"

void House::SetHeight(double h) {
  if (h < 0) {
    throw std::invalid_argument("Height must be non-negative!!!");
  }
  this->height = h;
}
