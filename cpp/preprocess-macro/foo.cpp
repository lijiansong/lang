#include <iostream>
#include <vector>
using namespace std;

#define DRV_BOARD_TYPE 100
#if (DRV_BOARD_TYPE == 200)
#define START_ADDR_OF_SD528 0x14220000
#else if (DRV_BOARD_TYPE == 300)
#define START_ADDR_OF_SD528 0x14210000
#endif

/*
 * warning: extra tokens at end of #else directive [-Wextra-tokens]
 * */
int main() {
    unsigned int a;
    a = START_ADDR_OF_SD528;
    cout << hex << a << endl;
    return 0;
}
