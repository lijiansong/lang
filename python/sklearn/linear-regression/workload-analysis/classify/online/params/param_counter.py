import caffe
from numpy import prod, sum
from pprint import pprint
import os

def print_param_info(net_name, net_file):
    net = caffe.Net(net_file, caffe.TEST)
    print('Layer-wise params:')
    pprint([(k, v[0].data.shape) for k, v in net.params.items()])
    print('--> {} total number of params: {}'.format(net_name, sum([prod(v[0].data.shape) for k, v in net.params.items()])/1024.0/1024.0))

if __name__ == '__main__':
    net_list = ['mobilenet_v2-github', 'mobilenet', 'squeezenet', 'densenet121', 'resnet50', 'ssd_mobilenetv1', 'ssd_vgg16']
    for net in net_list:
        net_file_blob = net + '/' + net + '_float16_dense_1batch.prototxt'
        if not os.path.exists(net_file_blob):
            print('{} NOT exists!!!'.format(net_file_blob))
            exit(-1)
        print_param_info(net, net_file_blob)

