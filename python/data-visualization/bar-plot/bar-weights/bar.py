import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        if height > 0.0:
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        else:
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, -15),  # 15 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


def draw_e2e_lr():
    labels = ['BS', 'DP', 'MP', 'TN']
    mobilenet_lr = [17.0, -20.0, -10.1, 19.8]
    squeezenet_lr = [-9.8, -17.2, -7.4, 37.2]
    ssd_mobilenet_lr = [-10.6, -21.0, -13.9, 31.8]
    densenet121_lr = [-0.5, 16.8, -7.1, 55.9]
    resnet50_lr = [8.9, 2.4, -8.6, 47.4]
    ssd_vgg16_lr = [5.3, 24.4, -27.0, 51.2]

    net_num = 6
    width = 0.35
    x0 = [(1+(net_num+1)*i)*width for i in range(len(labels))]
    x1 = [(2+(net_num+1)*i)*width for i in range(len(labels))]
    x2 = [(3+(net_num+1)*i)*width for i in range(len(labels))]
    x3 = [(4+(net_num+1)*i)*width for i in range(len(labels))]
    x4 = [(5+(net_num+1)*i)*width for i in range(len(labels))]
    x5 = [(6+(net_num+1)*i)*width for i in range(len(labels))]

    fig, ax = plt.subplots()
    rects_mobilenet = ax.bar(x0, mobilenet_lr, width, label='MobileNet')
    rects_squeezenet = ax.bar(x1, squeezenet_lr, width, label='SqueezeNet')
    rects_ssd_mobilenet = ax.bar(x2, ssd_mobilenet_lr, width, label='SSD_MobileNetV1')
    rects_densenet121 = ax.bar(x3, densenet121_lr, width, label='DenseNet121')
    rects_resnet50 = ax.bar(x4, resnet50_lr, width, label='ResNet50')
    rects_ssd_vgg16 = ax.bar(x5, ssd_vgg16_lr, width, label='SSD_VGG16')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('LR weights(%)')
    ax.set_title('LR weights of hyper-parameters over end-to-end throughput')
    ax.set_xticks(x3)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(ax, rects_mobilenet)
    autolabel(ax, rects_squeezenet)
    autolabel(ax, rects_ssd_mobilenet)
    autolabel(ax, rects_densenet121)
    autolabel(ax, rects_resnet50)
    autolabel(ax, rects_ssd_vgg16)

    fig.tight_layout()
    plt.show()

def draw_hw_lr():
    labels = ['BS', 'DP', 'MP', 'TN']
    mobilenet_lr = [-1.4, 16.9, 13.8, 29.0]
    squeezenet_lr = [-2.5, 21.5, 20.1, 29.7]
    ssd_mobilenet_lr = [-0.7, 20.1, 7.7, 23.3]
    densenet121_lr = [0.3, 27.4, 17.4, 51.0]
    resnet50_lr = [2.2, 22.7, 12.1, 38.0]
    ssd_vgg16_lr = [-0.3, 20.1, 5.0, 23.2]

    net_num = 6
    width = 0.35
    x0 = [(1+(net_num+1)*i)*width for i in range(len(labels))]
    x1 = [(2+(net_num+1)*i)*width for i in range(len(labels))]
    x2 = [(3+(net_num+1)*i)*width for i in range(len(labels))]
    x3 = [(4+(net_num+1)*i)*width for i in range(len(labels))]
    x4 = [(5+(net_num+1)*i)*width for i in range(len(labels))]
    x5 = [(6+(net_num+1)*i)*width for i in range(len(labels))]

    fig, ax = plt.subplots()
    rects_mobilenet = ax.bar(x0, mobilenet_lr, width, label='MobileNet')
    rects_squeezenet = ax.bar(x1, squeezenet_lr, width, label='SqueezeNet')
    rects_ssd_mobilenet = ax.bar(x2, ssd_mobilenet_lr, width, label='SSD_MobileNetV1')
    rects_densenet121 = ax.bar(x3, densenet121_lr, width, label='DenseNet121')
    rects_resnet50 = ax.bar(x4, resnet50_lr, width, label='ResNet50')
    rects_ssd_vgg16 = ax.bar(x5, ssd_vgg16_lr, width, label='SSD_VGG16')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('LR weights(%)')
    ax.set_title('LR weights of hyper-parameters over hardware throughput')
    ax.set_xticks(x3)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(ax, rects_mobilenet)
    autolabel(ax, rects_squeezenet)
    autolabel(ax, rects_ssd_mobilenet)
    autolabel(ax, rects_densenet121)
    autolabel(ax, rects_resnet50)
    autolabel(ax, rects_ssd_vgg16)

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    draw_e2e_lr()
    draw_hw_lr()
