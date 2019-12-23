
import xml.etree.cElementTree as ET
import sys
import os

# please put this parser in 'VOC2012/Annotations' directory.

def parse_xml(input):

    tree = ET.ElementTree(file = input)
    root = tree.getroot()

    width = 0
    height = 0
    objs = []

    for elem in root.iterfind('size/width'):
        width = int(elem.text)

    for elem in root.iterfind('size/height'):
        height = int(elem.text)

    for elem in root.iterfind('object'):
        tmp = []
        for chd_elem in elem.iterfind('name'):
            tmp.append(chd_elem.text)
        for chd_elem in elem.iterfind('bndbox/xmin'):
            xmin = float(chd_elem.text) / width
            tmp.append(xmin)
        for chd_elem in elem.iterfind('bndbox/ymin'):
            ymin = float(chd_elem.text) / height
            tmp.append(ymin)
        for chd_elem in elem.iterfind('bndbox/xmax'):
            xmax = float(chd_elem.text) / width
            tmp.append(xmax)
        for chd_elem in elem.iterfind('bndbox/ymax'):
            ymax = float(chd_elem.text) / height
            tmp.append(ymax)
        objs.append(tmp)
    return objs

def parse_output(input):
    objs = []
    for line in open(input).readlines():
        objs.append(line.split(' '))
    return objs

def IoU(obj1, obj2):
    overlap_x = min(float(obj1[3]), float(obj2[3])) - \
        max(float(obj1[1]), float(obj2[1]))
    overlap_y = min(float(obj1[4]), float(obj2[4])) - \
        max(float(obj1[2]), float(obj2[2]))
    overlap = (overlap_x > 0 and overlap_x or 0) * \
        (overlap_y > 0 and overlap_y or 0);
    box_square = (float(obj1[3]) - float(obj1[1])) * \
                 (float(obj1[4]) - float(obj1[2])) + \
                 (float(obj2[3]) - float(obj2[1])) * \
                 (float(obj2[4]) - float(obj2[2]));
    return overlap / (box_square - overlap)

def average_precision(golden_objs, result_objs):
    precision = 0
    for i in range(len(result_objs)):
        for j in range(len(golden_objs)):
            if result_objs[i][0] == golden_objs[j][0] and \
            IoU(result_objs[i], golden_objs[j]) > 0.5:
                precision += 1
    return precision / len(golden_objs)

def meanAP(image_list, result_dir, golden_dir):
    result_dir = result_dir.rstrip('/')
    golden_dir = golden_dir.rstrip('/')
    meanAP = 0
    images_num = 0
    for img in open(image_list).readlines():
        images_num += 1
        img_name = os.path.splitext(os.path.basename(img))[0]
        golden_objs = parse_xml(golden_dir + '/' + img_name + '.xml')
        result_objs = parse_output(result_dir + '/' + img_name + '.txt')

        ap = average_precision(golden_objs, result_objs)
        meanAP += ap
    return meanAP / images_num

if __name__ == "__main__":
   print  meanAP(sys.argv[1], sys.argv[2], sys.argv[3])
