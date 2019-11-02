#!/bin/bash

grep -ril "cnrtError" val.log-int8-dense-* | xargs -i mv {} cnrt-error

grep -rin "End2end throughput fps" val.log-int8-dense-* 2>&1 | tee end2end-fps.log
grep -rin "Hardware fps" val.log-int8-dense-* 2>&1 | tee hardware-fps.log
grep -rin "Total execution time" val.log-int8-dense-* 2>&1 | tee total-exe-time.log
grep -rin "Global accuracy" val.log-int8-dense-* | cut -d ":" -f1,2 2>&1 | tee acc.log
python3 extract_acc.py acc.log
mv end2end-fps.log hardware-fps.log total-exe-time.log scripts

#grep -rin "prepare input data" val.log-int8-dense-* 2>&1 | tee prepare-input.log
#grep -rin "copyin time" val.log-int8-dense-* 2>&1 | tee copyin-time.log
#grep -rin "copyout time" val.log-int8-dense-* 2>&1 | tee copyout-time.log
#mv prepare-input.log copyin-time.log copyout-time.log scripts
