#include <iostream>

class Box {
public:
  static int objectCount;

  Box(double l = 2.0, double b = 2.0, double h = 2.0) {
    std::cout << "Constructor called." << std::endl;
    length = l;
    breadth = b;
    height = h;

    // Increase every time object is created
    ++objectCount;
  }

  double getVolume() { return length * breadth * height; }

  void clearObjCount() { objectCount = 0; }

  static int getObjCount() { return objectCount; }

private:
  double length;  // Length of a box
  double breadth; // Breadth of a box
  double height;  // Height of a box
};

// Initialize static member of class Box
// objectCount is NOT allowed inside a function
int Box::objectCount = 0;

int main() {
  Box Box1(1, 2, 3);
  // Box1.ClearObjCount();
  Box Box2(4, 5, 6);

  // Print total number of objects.
  std::cout << "Total objects: " << Box::objectCount << std::endl;
  std::cout << "Total objects: " << Box::getObjCount() << std::endl;

  return 0;
}
