#!/usr/bin/env python3

import time

if __name__ == '__main__':
    players = [1, 2]
    current_player = 1
    try:
        while True:
            current_player = (players[0] if current_player == players[1] else players[1])
            print(current_player)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('\r\nquit')
