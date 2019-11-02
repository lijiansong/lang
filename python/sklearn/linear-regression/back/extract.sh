#!/bin/bash
#grep -rin "End2end throughput fps" val.log-int8-sparse-* 2>&1 | tee end2end-fps.log
#grep -rin "Hardware fps" val.log-int8-sparse-* 2>&1 | tee hardware-fps.log
#grep -rin "Total execution time" val.log-int8-sparse-* 2>&1 | tee total-exe-time.log
#grep -rin "Global accuracy" val.log-int8-sparse-* | cut -d ":" -f1,2 2>&1 | tee acc.log
#python3 extract_acc.py acc.log
grep -rin "prepare input data" val.log-int8-sparse-* 2>&1 | tee prepare-input.log
grep -rin "copyin time" val.log-int8-sparse-* 2>&1 | tee copyin-time.log
grep -rin "copyout time" val.log-int8-sparse-* 2>&1 | tee copyout-time.log
#mv end2end-fps.log hardware-fps.log total-exe-time.log scripts
mv prepare-input.log copyin-time.log copyout-time.log scripts
