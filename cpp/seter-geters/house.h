#ifndef _HOUSE_H_
#define _HOUSE_H_

#include <stdexcept>

class House {
public:
  double GetHeight() const { return height; }
  void SetHeight(double h);

private:
  double height;
};

#endif // _HOUSE_H_
