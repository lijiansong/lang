from caffe.proto import caffe_pb2
import google.protobuf.text_format
import caffe

def extract_layer_info(net_file_path):
    net_name = str(net_file_path).split('.')[0]
    if 'int8' in net_name:
        # get sparsity
        net_name = net_name.split('_')[0]
        net_name += '-dense-int8'
    else:
        net_name = net_name.split('_')[0]
        net_name += '-dense-fp16'
    print(net_name)
    layer_info_dict = {}
    layer_info_dict['name'] = net_name
    net = caffe_pb2.NetParameter()
    net_file = open(net_file_path, 'r')
    net = google.protobuf.text_format.Merge(str(net_file.read()), net)
    for i in range(0, len(net.layer)):
        print('--->', net.layer[i].name, net.layer[i].type)
        print(len(net.layer[i].top), len(net.layer[i].bottom))
        layer_info_dict[net.layer[i].name] = net.layer[i].type
    net_file.close()
    #print(layer_info_dict)
    return layer_info_dict

# REF: https://stackoverflow.com/questions/45199643/how-do-i-load-a-caffe-model-and-convert-to-a-numpy-array/45208380#45208380
def get_layer_shape(net_file_path, weight_file_path):
    # read the net + weights
    #net = caffe.Net(net_file_path, weight_file_path, caffe.TEST)
    # read the net + weights
    net = caffe.Net(net_file_path, caffe.TEST)
    pynet_ = []
    # for each layer in the net
    for li in xrange(len(net.layers)):
        # store layer's information
        layer = {}
        layer['name'] = net._layer_names[li]
        # for each input to the layer (aka "bottom") store its name and shape
        layer['bottoms'] = [(net._blob_names[bi], net.blobs[net._blob_names[bi]].data.shape)
                             for bi in list(net._bottom_ids(li))]
        # for each output of the layer (aka "top") store its name and shape
        layer['tops'] = [(net._blob_names[bi], net.blobs[net._blob_names[bi]].data.shape)
                          for bi in list(net._top_ids(li))]
        layer['type'] = net.layers[li].type  # type of the layer
        # the internal parameters of the layer. not all layers has weights.
        #layer['weights'] = [net.layers[li].blobs[bi].data[...]
        #                    for bi in xrange(len(net.layers[li].blobs))]
        print(layer)
        pynet_.append(layer)
    return pynet_

if __name__ == '__main__':
    #net_file = 'squeezenet-sparse-fp16/squeezenet_float16_dense_1batch-0.10.prototxt.sparse'
    #net_file = 'mobilenet-sparse-fp16/mobilenet_float16_dense_1batch-0.10.prototxt.sparse'
    net_file = 'mobilenet_float16_dense_1batch-online.prototxt'
    weight_file = '/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/mobilenet_float16_dense.caffemodel'
    #extract_layer_info(net_file)
    get_layer_shape(net_file, weight_file)
