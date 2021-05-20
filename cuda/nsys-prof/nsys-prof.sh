#!/bin/bash
nsys profile -o nsys-log --stats=true ./a.out
nsys stats nsys-log.qdrep --format csv

