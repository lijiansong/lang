
def extract_data(data_file_blob='data.txt'):
    with open(data_file_blob, 'r') as f:
        data_lines = f.readlines()
        for data in data_lines:
            data = data.rstrip('\n')
            items = data.split('\t')
            prepare_input_time = float(items[0])
            copy_in_time = float(items[1])
            execution_time = float(items[2])
            copy_out_time = float(items[3])
            post_process_time = float(items[4])
            sum_stage_time = prepare_input_time + copy_in_time + execution_time + copy_out_time + post_process_time
            print('{} {} {} {} {}'.format(prepare_input_time / sum_stage_time * 100,
                copy_in_time / sum_stage_time * 100,
                execution_time / sum_stage_time * 100,
                copy_out_time / sum_stage_time * 100,
                post_process_time / sum_stage_time * 100))


if __name__ == '__main__':
    extract_data()
