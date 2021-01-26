import matplotlib.pyplot as plt

idea_data_list = []
with open('load_ideal.csv', 'r') as load_reader:
    data = load_reader.readlines()
    for i in data:
        i = float(i)
        idea_data_list.append(i)

plt.plot(idea_data_list)
plt.show()
