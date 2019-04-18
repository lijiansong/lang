#include "serial.h"

int serial_open(int fd, char *port) {

  fd = open(port, O_RDWR | O_NOCTTY | O_NDELAY);
  if (FALSE == fd) {
    printf("Can't Open Serial Port!!!"); // json lee
    // perror("Can't Open Serial Port");
    return (FALSE);
  }
  //判断串口的状态是否为阻塞状态
  if (fcntl(fd, F_SETFL, 0) < 0) {
    printf("fcntl failed!/n");
    return (FALSE);
  } else {
    printf("fcntl=%d/n", fcntl(fd, F_SETFL, 0));
  }
  //测试是否为终端设备
  if (0 == isatty(STDIN_FILENO)) {
    printf("standard input is not a terminal device/n");
    return (FALSE);
  } else {
    printf("isatty success!/n");
  }
  printf("fd->open=%d/n", fd);
  return fd;
}

int serial_set(int fd, int speed, int flow_ctrl, int databits, int stopbits,
                int parity) {
  int i;
  int status;
  int speed_arr[] = {B38400, B19200, B9600, B4800, B2400, B1200, B300,
                     B38400, B19200, B9600, B4800, B2400, B1200, B300};
  int name_arr[] = {38400, 19200, 9600, 4800, 2400, 1200, 300,
                    38400, 19200, 9600, 4800, 2400, 1200, 300};

  struct termios options;

  if (tcgetattr(fd, &options) != 0) {
    perror("SetupSerial 1");
    return (FALSE);
  }

  //设置串口输入波特率和输出波特率
  for (i = 0; i < sizeof(speed_arr) / sizeof(int); i++) {
    if (speed == name_arr[i]) {
      cfsetispeed(&options, speed_arr[i]);
      cfsetospeed(&options, speed_arr[i]);
    }
  }

  //修改控制模式，保证程序不会占用串口
  options.c_cflag |= CLOCAL;
  //修改控制模式，使得能够从串口中读取输入数据
  options.c_cflag |= CREAD;

  //设置数据流控制
  switch (flow_ctrl) {

  case 0: //不使用流控制
    options.c_cflag &= ~CRTSCTS;
    break;

  case 1: //使用硬件流控制
    options.c_cflag |= CRTSCTS;
    break;
  case 2: //使用软件流控制
    options.c_cflag |= IXON | IXOFF | IXANY;
    break;
  }
  //设置数据位
  options.c_cflag &= ~CSIZE; //屏蔽其他标志位
  switch (databits) {
  case 5:
    options.c_cflag |= CS5;
    break;
  case 6:
    options.c_cflag |= CS6;
    break;
  case 7:
    options.c_cflag |= CS7;
    break;
  case 8:
    options.c_cflag |= CS8;
    break;
  default:
    fprintf(stderr, "Unsupported data size/n");
    return (FALSE);
  }
  //设置校验位
  switch (parity) {
  case 'n':
  case 'N': //无奇偶校验位。
    options.c_cflag &= ~PARENB;
    options.c_iflag &= ~INPCK;
    break;
  case 'o':
  case 'O': //设置为奇校验
    options.c_cflag |= (PARODD | PARENB);
    options.c_iflag |= INPCK;
    break;
  case 'e':
  case 'E': //设置为偶校验
    options.c_cflag |= PARENB;
    options.c_cflag &= ~PARODD;
    options.c_iflag |= INPCK;
    break;
  case 's':
  case 'S': //设置为空格
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    break;
  default:
    fprintf(stderr, "Unsupported parity/n");
    return (FALSE);
  }
  // 设置停止位
  switch (stopbits) {
  case 1:
    options.c_cflag &= ~CSTOPB;
    break;
  case 2:
    options.c_cflag |= CSTOPB;
    break;
  default:
    fprintf(stderr, "Unsupported stop bits/n");
    return (FALSE);
  }

  //修改输出模式，原始数据输出
  options.c_oflag &= ~OPOST;

  //设置等待时间和最小接收字符
  options.c_cc[VTIME] = 1; /* 读取一个字符等待1*(1/10)s */
  options.c_cc[VMIN] = 1;  /* 读取字符的最少个数为1 */

  //如果发生数据溢出，接收数据，但是不再读取
  tcflush(fd, TCIFLUSH);

  //激活配置 (将修改后的termios数据设置到串口中）
  if (tcsetattr(fd, TCSANOW, &options) != 0) {
    perror("com set error!/n");
    return (FALSE);
  }
  return (TRUE);
}

int serial_init(int fd, int speed, int flow_ctrlint, int databits,
                 int stopbits, int parity) {
  int err;
  //设置串口数据帧格式
  if (serial_set(fd, speed, 0, 8, 1, 'N') == FALSE) {
    return FALSE;
  } else {
    return TRUE;
  }
}

int serial_recv(int fd, char *rcv_buf, int data_len) {
  int len, fs_sel;
  fd_set fs_read;

  struct timeval time;

  FD_ZERO(&fs_read);
  FD_SET(fd, &fs_read);

  time.tv_sec = 10;
  time.tv_usec = 0;

  //使用select实现串口的多路通信
  fs_sel = select(fd + 1, &fs_read, NULL, NULL, &time);
  if (fs_sel) {
    len = read(fd, rcv_buf, data_len);
    return len;
  } else {
    return FALSE;
  }
}

int serial_send(int fd, unsigned char *send_buf, int data_len) {
  int len = 0;

  len = write(fd, send_buf, data_len);
  if (len == data_len) {
    return len;
  } else {
    tcflush(fd, TCOFLUSH);
    return FALSE;
  }
}

void serial_close(int fd) { close(fd); }
