from sklearn import linear_model

# https://www.liaoxuefeng.com/wiki/1016959663602400

def read_in_chunks(file_path, chunk_size=512):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 512
    """
    file_object = open(file_path)
    while True:
        chunk_data = file_object.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data

if __name__ == "__main__":
    file_path = 'sparse-0.1-fp16-fifo.txt'
    counter = 0
    for chunk in read_in_chunks(file_path):
        counter += 1
        print(type(chunk))
        print(chunk)
    print("counter: ", counter)

    X = []
    y = []
    # line based file
    with open(file_path) as f:
        for line in f:
            print(line)
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            X.append([batch_size, data_parallel, model_parallel, thread_num, fifo_size])
            y.append(end2end_fps)
    print(len(X), len(y))
    clf = linear_model.LinearRegression()
    clf.fit(X, y)
    print(clf.coef_)
