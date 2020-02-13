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

def get_layer_shape(net_file_path, weight_file_path):
    net = caffe.Net(net_file_path, caffe.TEST)
    net_shape_dict = {}
    for li in xrange(len(net.layers)):  # for each layer in the net
        layer = {}  # store layer's information
        layer_name = net._layer_names[li]
        # for each input to the layer (aka "bottom") store its shape(type tuple)
        layer['bottoms'] = [net.blobs[net._blob_names[bi]].data.shape
                             for bi in list(net._bottom_ids(li))]
        # for each output of the layer (aka "top") store its shape
        layer['tops'] = [(net.blobs[net._blob_names[bi]].data.shape)
                          for bi in list(net._top_ids(li))]
        # type of the layer
        layer['type'] = net.layers[li].type
        # the internal parameters of the layer, not all layers has weights.
        #layer['weights'] = [net.layers[li].blobs[bi].data[...]
        #                    for bi in xrange(len(net.layers[li].blobs))]
        #print(layer)
        net_shape_dict[layer_name] = layer

    parsible_net = caffe_pb2.NetParameter()
    google.protobuf.text_format.Merge(open(net_file_path).read(), parsible_net)
    for layer in parsible_net.layer:
        if layer.type == 'Convolution':
            #print('Convolution')
            #print('kernel_size:', layer.convolution_param.kernel_size[0] if len(layer.convolution_param.kernel_size) else 1)
            #print('stride:', layer.convolution_param.stride[0] if len(layer.convolution_param.stride) else 1)
            #print('pad:', layer.convolution_param.pad[0] if len(layer.convolution_param.pad) else 0)
            net_shape_dict[layer.name]['kernel_size'] = layer.convolution_param.kernel_size[0] if len(layer.convolution_param.kernel_size) else 1
            net_shape_dict[layer.name]['stride'] = layer.convolution_param.stride[0] if len(layer.convolution_param.stride) else 1
            net_shape_dict[layer.name]['pad'] = layer.convolution_param.pad[0] if len(layer.convolution_param.pad) else 0
        if layer.type == 'Pooling':
            #print('Pooling')
            #print('kernel size:', int(layer.pooling_param.kernel_size))
            #print('stride:', int(layer.pooling_param.stride))
            #print('pad:', int(layer.pooling_param.pad))
            net_shape_dict[layer.name]['kernel_size'] = layer.pooling_param.kernel_size
            net_shape_dict[layer.name]['stride'] = layer.pooling_param.stride
            net_shape_dict[layer.name]['pad'] = layer.pooling_param.pad
    print(net_shape_dict)

    max_tops_length = max_bottoms_length = 0
    for k, v in net_shape_dict.items():
        #print(k, v)
        max_tops_length = max(max_tops_length, len(v['tops']))
        max_bottoms_length = max(max_bottoms_length, len(v['bottoms']))
    print(max_tops_length, max_bottoms_length)
    return net_shape_dict

if __name__ == '__main__':
    #net_file = 'squeezenet-sparse-fp16/squeezenet_float16_dense_1batch-0.10.prototxt.sparse'
    #net_file = 'mobilenet-sparse-fp16/mobilenet_float16_dense_1batch-0.10.prototxt.sparse'
    #net_file = 'mobilenet_float16_dense_1batch-online.prototxt'
    #net_file = 'squeezenet_float16_dense_1batch-online.prototxt'
    net_file = 'resnet50_float16_dense_1batch-online.prototxt'
    weight_file = '/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/mobilenet_float16_dense.caffemodel'
    #extract_layer_info(net_file)
    get_layer_shape(net_file, weight_file)
