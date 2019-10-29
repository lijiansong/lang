from sklearn import linear_model

def get_data(file_name):
    file_reader = open(file_name, 'r')
    x_list = []
    y_list = []
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if model_parallel == 1 and batch_size == 8:
                x_list.append([batch_size, data_parallel, model_parallel, thread_num, fifo_size])
                y_list.append(end2end_fps)
                print(batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps)

    finally:
        if file_reader:
            file_reader.close()
    return x_list, y_list

def get_lr_model(X, y):
    clf = linear_model.LinearRegression()
    clf.fit(X, y)
    return clf.coef_

if __name__ == '__main__':
    print('===---------------- dense int8 ----------------===')
    X, y = get_data('int8-dense.txt')
    print(len(X), len(y))
