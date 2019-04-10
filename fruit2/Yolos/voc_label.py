import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


classes = ["apple", "banana", "orange"]


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
    in_file = open('/home/ubuntu/yolo_train/fruit2/Yolos/%s.xml'%(image_id))
    out_file = open('/home/ubuntu/yolo_train/fruit2/Yolos/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

with open('/home/ubuntu/yolo_train/fruit2/cfg/test.txt', 'r', encoding='utf-8') as f:
    for i in range(303):
        s = f.readline()
        if "jpg" not in s:
            print(s)
            break
        else:
            image_ids = s.strip().split("/")
            print(image_ids[-1][:-4])
            convert_annotation(image_ids[-1][:-4])  
