from sklearn import linear_model
import matplotlib.pyplot as plt

def get_data(file_name):
    size_list = []
    in_time_list = []
    out_time_list = []
    with open(file_name, 'r') as file_reader:
        # skip the first line
        next(file_reader)
        data_lines = file_reader.readlines()
        for line in data_lines:
            line = line.rstrip('\n')
            line = line.split(',')
            size, in_time, out_time = int(line[0]), int(line[1]), int(line[2])
            size_list.append([size])
            in_time_list.append([in_time])
            out_time_list.append([out_time])

    return size_list, in_time_list, out_time_list


if __name__ == '__main__':
    clf = linear_model.LinearRegression()
    X, in_y, out_y = get_data('swap-io-new.txt')
    print(len(X), len(in_y), len(out_y))

    print('===---------------- swap in ----------------===')
    clf.fit(X, in_y)
    print('k:', clf.coef_)
    print('b:', clf.predict([[0]]))
    print('f(1):', clf.predict([[1]]))

    plt.scatter(X, in_y,  color='black')
    print('===---------------- swap out ----------------===')
    clf.fit(X, out_y)
    print('k:', clf.coef_)
    print('b:', clf.predict([[0]]))
    print('f(1):', clf.predict([[1]]))
    plt.scatter(X, out_y,  color='blue')
    plt.show()
