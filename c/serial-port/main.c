#include "serial.h"

int main(int argc, char **argv) {
  int fd, err, len;
  unsigned char send_buff[3];
  unsigned char recv_buff[30];
  fd = serial_open(fd, argv[1]);
  do {
    // int fd, int speed, int flow_ctrl, int databits, int stopbits, int parity
    err = serial_init(fd, 9600, 0, 8, 1, 'N');
    printf("Set port exactly!\n");
  } while (FALSE == err || FALSE == fd);

  send_buff[0] = (char)0xaa;
  send_buff[1] = (char)3;
  send_buff[2] = (char)4;
  int i;
  for(i = 0; i < 2; ++i) {
    len = serial_send(fd, send_buff, 3);
    if (len > 0) {
      printf("Send data successful\n");
    } else {
      printf("Error! Send data failed!\n");
    }
    serial_recv(fd, recv_buff, 10);
    printf("%s\n", recv_buff);
  }
  sleep(2);
  serial_close(fd);
  return 0;
}
