#!/bin/bash
# Parameter1 int8_mode: 1-int8; 0-float16

usage()
{
    echo "Usage:"
    echo "  $0 [0|1] [1|2]"
    echo ""
    echo "  Parameter description:"
    echo "    parameter1: int8 mode or float16 mode. 0:float16, 1:int8"
    echo "    parameter2: simple_compile_interface? 0:false, 1:true"
}

checkFile()
{
    if [ -f $1 ]; then
        return 0
    else
        return 1
    fi
}
bang_option="0"

do_run()
{

    echo "----------------------"
    echo "multiple core"
    echo "using prototxt: $proto_file"
    echo "using model:    $model_file"
    if [[ $simple_compile -eq 0 ]]; then
        echo "dataparallel:  $dp,  modelparallel:  $mp,  threadnum:  ${thread_num}"
    else
        echo "batchsize:  $batchsize,  core_number:  $core_number"
    fi

    #first remove any offline model
    /bin/rm offline.cambricon* &> /dev/null

    log_file=$(echo $proto_file | sed 's/prototxt$/log/' | sed 's/^.*\///')
    echo > $CURRENT_DIR/$log_file

    genoff_cmd="$CURRENT_DIR/../../build/tools/caffe${SUFFIX} genoff \
        -model $proto_file \
        -weights $model_file \
        -mcore MLU100 \
        -Bangop $bang_option"
    if [[ $simple_compile -eq 0 ]]; then
        concurrent_genoff=" -model_parallel $mp &>> $CURRENT_DIR/$log_file"
    else
        concurrent_genoff=" -batchsize $batchsize -core_number $core_number -simple_compile 1 &>> $CURRENT_DIR/$log_file"
    fi
    genoff_cmd="$genoff_cmd $concurrent_genoff"

    run_cmd="$CURRENT_DIR/../../build/examples/ssd/ssd_offline_multicore$SUFFIX \
        -offlinemodel $CURRENT_DIR/offline.cambricon  \
        -images $CURRENT_DIR/$FILE_LIST \
        -labelmapfile $CURRENT_DIR/labelmap_voc.prototxt  \
        -confidencethreshold 0.6 \
        -Bangop $bang_option \
        -dump 1"
    if [[ $simple_compile -eq 0 ]]; then
        concurrent_run=" -threads ${thread_num} -dataparallel $dp &>> $CURRENT_DIR/$log_file"
    else
        concurrent_run=" -simple_compile 1 &>> $CURRENT_DIR/$log_file"
    fi
    run_cmd="$run_cmd $concurrent_run"

    check_cmd="python $CAFFE_DIR/scripts/meanAP_VOC.py $CURRENT_DIR/$FILE_LIST $CURRENT_DIR/ $VOC_PATH &>> $CURRENT_DIR/$log_file"

    echo "genoff_cmd: $genoff_cmd" &>> $CURRENT_DIR/$log_file
    echo "run_cmd: $run_cmd" &>> $CURRENT_DIR/$log_file
    echo "check_cmd: $check_cmd" &>> $CURRENT_DIR/$log_file

    echo "generating offline model..."
    eval "$genoff_cmd"

    if [[ "$?" -eq 0 ]]; then
        echo -e "running offline test...\n"
        eval "$run_cmd"
        # tail -n 3 $CURRENT_DIR/$log_file
        grep "^Total execution time: " -A 2 $CURRENT_DIR/$log_file
        eval "$check_cmd"
        tail -n 1 $CURRENT_DIR/$log_file
    else
        echo "generating offline model failed!"
    fi
}

desp_list=(
    dense
    sparse
)

bscn_list=(
  # '1  1 '
  # '8  8 '
  # '16 16'
   '32 32'
  # '64 32'
)

batch_list=(
    1batch
    # 2batch
    # 4batch
)

dpmp_list=(
    '8 1'
    # '1 2'
    # '2 4'
    # '4 8'
)

network_list=(
    ssd
    ssd_mobilenetv1
    ssd_mobilenetv2
    ssd_vgg16
)

if [[ "$#" -ne 2 ]]; then
    echo "[ERROR] Unknown parameter."
    usage
    exit 1
fi

CURRENT_DIR=$(dirname $(readlink -f $0))

# check caffe directory
if [ -z "$CAFFE_DIR" ]; then
    CAFFE_DIR=$CURRENT_DIR/../..
else
    if [ ! -d "$CAFFE_DIR" ]; then
        echo "[ERROR] Please check CAFFE_DIR."
        exit 1
    fi
fi

. $CAFFE_DIR/scripts/set_caffe_module_env.sh

int8_mode=$1
ds_name=""
if [[ $int8_mode -eq 1 ]]; then
    ds_name="int8"
elif [[ $int8_mode -eq 0 ]]; then
    ds_name="float16"
else
    echo "[ERROR] Unknown parameter."
    usage
    exit 1
fi
simple_compile=$2
thread_num="4"

/bin/rm *.jpg &> /dev/null
/bin/rm 200*.txt &> /dev/null
/bin/rm *.log &> /dev/null

for network in "${network_list[@]}"; do
    for desp in "${desp_list[@]}"; do
        model_file=$CAFFE_MODELS_DIR/${network}/${network}_${ds_name}_${desp}.caffemodel
		checkFile $model_file
        if [ $? -eq 1 ]; then
            continue
        fi

        echo -e "\n===================================================="
        echo "running ${network} offline - ${ds_name},${desp}..."

        if [[ $simple_compile -eq 0 ]]; then
            for batch in "${batch_list[@]}"; do
                for proto_file in $CAFFE_MODELS_DIR/${network}/${network}_${ds_name}*${desp}_${batch}.prototxt; do
                    checkFile $proto_file
                    if [ $? -eq 1 ]; then
                        continue
                    fi

                    for dpmp in "${dpmp_list[@]}"; do
                        dp=${dpmp:0:1}
                        mp=${dpmp:2:1}
                        do_run
                    done
                done
            done
        else
            for proto_file in $CAFFE_MODELS_DIR/${network}/${network}_${ds_name}*${desp}_1batch.prototxt; do
                checkFile $proto_file
                if [ $? -eq 1 ]; then
                    continue
                fi
                for bscn in "${bscn_list[@]}"; do
                    batchsize=${bscn:0:2}
                    core_number=${bscn:3:2}
                    do_run
                done
            done
        fi
    done
done