import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('train'), ('val')]

classes = ["pig01", "pig02","pig03","pig04","pig05","pig06","pig07","pig08","pig09","pig10","pig10","pig11","pig12","pig13","pig14","pig15","pig16","pig17","pig18","pig19","pig20","pig21","pig22","pig23","pig24","pig25","pig26","pig27","pig28","pig29","pig30"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('/Users/matt/Downloads/train/outputXML/%s.xml'%(image_id))
    out_file = open('/Users/matt/Downloads/train/outputTXT/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    print root
    for obj in root.iter('object'):
        print "=====" + obj.find("name").text
        # difficult = obj.find('difficult').text
        difficult = 0
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for image_set in sets:
    if not os.path.exists('VOCdevkit/VOC/labels/'):
        os.makedirs('VOCdevkit/VOC/labels/')
    image_ids = open('/Users/matt/Downloads/train/outputXML/%s.txt'%(image_set)).read().strip().split()
    list_file = open('/Users/matt/Downloads/train/%s.txt'%(image_set), 'w')
    for image_id in image_ids:
        list_file.write('/Users/matt/Downloads/train/output/%s.jpg\n'%(image_id))
        convert_annotation(image_id)
    list_file.close()

# os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
# os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")

