#!/bin/bash
python3 extract_data.py end2end-fps.log hardware-fps.log total-exe-time.log #acc.log prepare-input.log copyin-time.log copyout-time.log
python3 excel_io.py
