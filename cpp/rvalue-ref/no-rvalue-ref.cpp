// REF: https://github.com/qicosmos/cosmos
// Rvalue reference
// Impl constructor and operator = with `move constructor and move assignment function`

#include <iostream>
#include <vector>

size_t copy_times = 0;

class MyString {
private:
  char *m_data;
  size_t m_len;

  void copy_data(const char *s) {
    std::cout << "------copy data: " << ++copy_times << std::endl;
    m_data = new char[m_len + 1];
    memcpy(m_data, s, m_len);
    m_data[m_len] = '\0';
  }

public:
  MyString() {
    m_data = NULL;
    m_len = 0;
  }

  MyString(const char *p) {
    m_len = strlen(p);
    copy_data(p);
    std::cout << "---- MyString(const char *p):\n";
    std::cout << "source: "<< this->m_data << std::endl;
  }

  MyString(const MyString &str) {
    m_len = str.m_len;
    copy_data(str.m_data);
    std::cout << "MyString(const MyString &str):\n";
    std::cout << "Copy Constructor is called! source:" << str.m_data
              << std::endl;
  }

  MyString &operator=(const MyString &str) {
    if (this != &str) {
      m_len = str.m_len;
      copy_data(str.m_data);
    }
    std::cout << "MyString &operator=(const MyString &str)\n";
    std::cout << "Copy Assignment is called! source:" << str.m_data
              << std::endl;
    return *this;
  }

  virtual ~MyString() {
    if (m_data != NULL) {
      delete[] m_data;
    }
  }
};

int main(void) {
  MyString a;
  a = MyString("Hello");

  std::vector<MyString> vec;
  vec.push_back(MyString("World"));

  return 0;
}
