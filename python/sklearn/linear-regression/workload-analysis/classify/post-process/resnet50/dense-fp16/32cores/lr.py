from sklearn import linear_model

def get_data(file_name):
    file_reader = open(file_name, 'r')
    x_list = []
    y_list = []
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        batch_size_min = data_parallel_min = model_parallel_min = thread_num_min = fifo_size_min = end2end_fps_min = 100000000
        batch_size_max = data_parallel_max = model_parallel_max = thread_num_max = fifo_size_max = end2end_fps_max = 0
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            batch_size_min, data_parallel_min, model_parallel_min, thread_num_min, fifo_size_min, end2end_fps_min = min(batch_size_min, batch_size), min(data_parallel_min, data_parallel), min(model_parallel_min, model_parallel), min(thread_num_min, thread_num), min(fifo_size_min, fifo_size), min(end2end_fps_min, end2end_fps)
            batch_size_max, data_parallel_max, model_parallel_max, thread_num_max, fifo_size_max, end2end_fps_max = max(batch_size_max, batch_size), max(data_parallel_max, data_parallel), max(model_parallel_max, model_parallel), max(thread_num_max, thread_num), max(fifo_size_max, fifo_size), max(end2end_fps_max, end2end_fps)
            x_list.append([batch_size, data_parallel, model_parallel, thread_num, fifo_size])
            y_list.append(end2end_fps)
        print(batch_size_min, data_parallel_min, model_parallel_min, thread_num_min, fifo_size_min, end2end_fps_min)
        print(batch_size_max, data_parallel_max, model_parallel_max, thread_num_max, fifo_size_max, end2end_fps_max)
        for i, item in enumerate(x_list):
            if (model_parallel_min == model_parallel_max) and (fifo_size_min == fifo_size_max):
                x_list[i] = [(item[0] - batch_size_min) / (batch_size_max - batch_size_min), (item[1] - data_parallel_min) / (data_parallel_max - data_parallel_min), 1, (item[3] - thread_num_min) / (thread_num_max - thread_num_min), 1]
            elif (model_parallel_min != model_parallel_max) and (fifo_size_min == fifo_size_max):
                x_list[i] = [(item[0] - batch_size_min) / (batch_size_max - batch_size_min), (item[1] - data_parallel_min) / (data_parallel_max - data_parallel_min), (item[2] - model_parallel_min) / (model_parallel_max - model_parallel_min), (item[3] - thread_num_min) / (thread_num_max - thread_num_min), 1]
            elif (model_parallel_min == model_parallel_max) and (fifo_size_min != fifo_size_max):
                x_list[i] = [(item[0] - batch_size_min) / (batch_size_max - batch_size_min), (item[1] - data_parallel_min) / (data_parallel_max - data_parallel_min), 1, (item[3] - thread_num_min) / (thread_num_max - thread_num_min), (item[4] - fifo_size_min) / (fifo_size_max - fifo_size_min)]
            else:
                x_list[i] = [(item[0] - batch_size_min) / (batch_size_max - batch_size_min), (item[1] - data_parallel_min) / (data_parallel_max - data_parallel_min), (item[2] - model_parallel_min) / (model_parallel_max - model_parallel_min), (item[3] - thread_num_min) / (thread_num_max - thread_num_min), (item[4] - fifo_size_min) / (fifo_size_max - fifo_size_min)]
        for i, item in enumerate(y_list):
            y_list[i] = (item - end2end_fps_min) / (end2end_fps_max - end2end_fps_min)

    finally:
        if file_reader:
            file_reader.close()
    return x_list, y_list

def get_lr_model(X, y):
    clf = linear_model.LinearRegression()
    clf.fit(X, y)
    return clf.coef_

if __name__ == '__main__':
    clf = linear_model.LinearRegression()
    print('===---------------- dense fp16 end2end fps ----------------===')
    X, y = get_data('resnet50-dense-fp16.txt')
    print(len(X), len(y))
    clf.fit(X, y)
    print(clf.coef_)
    print('===---------------- dense fp16 hardware fps ----------------===')
    X, y = get_data('resnet50-dense-fp16-hw.txt')
    print(len(X), len(y))
    clf.fit(X, y)
    print(clf.coef_)
