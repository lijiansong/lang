#include <iostream>
#include <memory>

std::weak_ptr<int> gw;

// 如何通过锁来保证指针的有效性
void f() {
  if (auto spt = gw.lock()) {
    // 使用之前必须复制到 shared_ptr
    std::cout << *spt << '\n';
    std::cout <<"    f ----> spt use count: " << spt.use_count() << '\n';
    std::cout <<"    f ----> gw use count: " << gw.use_count() << '\n';
  } else {
    std::cout << "gw is expired\n";
    std::cout << "   f ----> gw use count: " << gw.use_count() << '\n';
  }
}

int main() {
  {
    auto sp = std::make_shared<int>(42);
    std::cout <<"main ----> initial sp use count: " << sp.use_count() << '\n';
    std::cout <<"main ----> initial gw use count: " << gw.use_count() << '\n';
    gw = sp;
    std::cout <<"main ----> after 'gw = sp;' sp use count: " << sp.use_count() << '\n';
    std::cout <<"main ----> after 'gw = sp;' gw use count: " << gw.use_count() << '\n';

    f();
    std::cout <<"main ----> after 'gw = sp; f();' sp use count: " << sp.use_count() << '\n';
    std::cout <<"main ----> after 'gw = sp; f();' gw use count: " << gw.use_count() << '\n';
  }

  std::cout <<"main ----> gw use count: " << gw.use_count() << '\n';
  f();
  std::cout <<"main ----> after gw use count: " << gw.use_count() << '\n';
}
