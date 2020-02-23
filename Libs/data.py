import os
import codecs
import xml.etree.ElementTree  as ET
from lxml import etree

def Label_get_instance(filename):
    file_label = {}
    assert os.path.isfile(filename), "{} in not a right filepath!".format(filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    size = root.find('size')
    width = float(size.find('width').text)
    height = float(size.find('height').text)
    instance_labels = []
    for instance_label in root.iter("object"):
        box = instance_label.find('bndbox')
        name = instance_label.find('name').text
        xmin = float((box.find('xmin').text))
        ymin = float((box.find('ymin').text))
        xmax = float((box.find('xmax').text))
        ymax = float((box.find('ymax').text))
        instance_labels.append({'name':name, "bndbox":[xmin, ymin, xmax, ymax]})

    file_label['filename'] = os.path.basename(filename)
    file_label['size'] = (width, height)
    file_label['instance'] = instance_labels

    return file_label

def Label_add_attritute(base_data, attribute_data):
    base_data['instance']['face_attribute']=  attribute_data['face_attribute']
    base_data['instance']['body_attribute'] = attribute_data['body_attribute']
    return base_data


from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString


def Label_write_instance(localImgPaths, size, instances, savename, databaseSrc='Mk1501_attri', ):
    top = Element('annotation')

    img_path, img_name = os.path.split(localImgPaths)
    folder = SubElement(top, 'folder')
    folder.text = os.path.split(img_path)[1]

    file = SubElement(top, 'filename')
    file.text = img_name

    localImgPath = SubElement(top, 'path')
    localImgPath.text = localImgPaths

    source = SubElement(top, 'source')
    database = SubElement(source, 'database')
    database.text = databaseSrc

    size_part = SubElement(top, 'size')
    width = SubElement(size_part, 'width')
    height = SubElement(size_part, 'height')
    depth = SubElement(size_part, 'depth')
    width.text = str(size[0])
    height.text = str(size[1])
    depth.text = '3'

    segmented = SubElement(top, 'segmented')
    segmented.text = '0'

    for instance in instances:
        object = SubElement(top, "object")

        name = SubElement(object, "name")
        name.text = 'Human_instance'
        pose = SubElement(object, "pose")
        pose.text = 'Unspecified'
        truncated = SubElement(object, "truncated")
        truncated.text = '1'
        difficult = SubElement(object, "difficult")
        difficult.text = '0'

        head_box = SubElement(object, "head_box")
        hxmin = SubElement(head_box, "xmin")
        hymin = SubElement(head_box, "ymin")
        hxmax = SubElement(head_box, "xmax")
        hymax = SubElement(head_box, "ymax")

        hxmin.text = str(instance[0][0][0])
        hymin.text = str(instance[0][0][1])
        hxmax.text = str(instance[0][0][2])
        hymax.text = str(instance[0][0][3])


        head_attri = SubElement(object, "head_attri")
        Blackhair = SubElement(head_attri, "Blackhair")
        Blury = SubElement(head_attri, "Blury")
        Eyeglass = SubElement(head_attri, "Eyeglass")
        Male = SubElement(head_attri, "Male")
        Smile = SubElement(head_attri, "Smile")
        Younge = SubElement(head_attri, "Younge")

        Blackhair.text = str(instance[1][0])
        Blury.text     = str(instance[1][1])
        Eyeglass.text  = str(instance[1][2])
        Male.text      = str(instance[1][3])
        Smile.text     = str(instance[1][4])
        Younge.text    = str(instance[1][5])

        body_box = SubElement(object, "body_box")
        bxmin = SubElement(body_box, "xmin")
        bymin = SubElement(body_box, "ymin")
        bxmax = SubElement(body_box, "xmax")
        bymax = SubElement(body_box, "ymax")

        bxmin.text = str(instance[0][1][0])
        bymin.text = str(instance[0][1][1])
        bxmax.text = str(instance[0][1][2])
        bymax.text = str(instance[0][1][3])

        body_attri = SubElement(object, "body_attri")
        gender = SubElement(body_attri, "gender")
        hat = SubElement(body_attri, "hat")
        backpack = SubElement(body_attri, "backpack")
        bag = SubElement(body_attri, "bag")
        age = SubElement(body_attri, "age")

        gender.text   = str(instance[1][6])
        hat.text      = str(instance[1][7])
        backpack.text = str(instance[1][8])
        bag.text      = str(instance[1][9])
        age.text      = str(instance[1][10])

    # return top
    with codecs.open(savename, 'w', encoding="utf-8") as out_file:
        rough_string = tostring(top)
        root = etree.fromstring(rough_string)
        prettifyResult = etree.tostring(root, pretty_print=True, encoding="utf-8").replace("  ".encode(), "\t".encode())
        out_file.write(prettifyResult.decode('utf8'))


if __name__ == "__main__":
    # Label_get_instance("./VOC2007_100.xml")
    Label_write_instance()



