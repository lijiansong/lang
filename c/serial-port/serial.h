#ifndef serialPort_hpp
#define serialPort_hpp
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <termios.h>
#include <unistd.h>

#define FALSE -1
#define TRUE 0
int serial_open(int fd, char *port);
int serial_set(int fd, int speed, int flow_ctrl, int databits, int stopbits,
                int parity);
int serial_init(int fd, int speed, int flow_ctrlint, int databits,
                 int stopbits, int parity);
int serial_recv(int fd, char *rcv_buf, int data_len);
int serial_send(int fd, unsigned char *send_buf, int data_len);
void serial_close(int fd);
#endif /* serialPort_hpp */
