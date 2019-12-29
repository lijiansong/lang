#!/bin/bash
net=densenet121
insert_data_file=${net}-sparse-int8-data.txt
insert_acc_file=${net}-sparse-int8-acc.txt

for origin_prototxt in `ls ${net}_float16_dense_1batch-int8-0.*`
do
    echo "===--- begin processing ${origin_prototxt} ---==="
    sed -i '25,29d' ${origin_prototxt}
    sed -i '1,13d' ${origin_prototxt}
    # add a blank line to the first line
    sed -i '1i\\' ${origin_prototxt}
    sed -i "1 r ${insert_data_file}" ${origin_prototxt}
    sed -i "$ r ${insert_acc_file}" ${origin_prototxt}
    echo "===--- end processing ${origin_prototxt} ---==="
done
