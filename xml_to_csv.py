import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import random


def xml_to_csv(path):
    xml_train = []
    xml_test = []
    for xml_file in glob.glob(path + '/*.xml'):
        if np.random.rand() < 0.8:
            train = True
        else:
            train = False
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            if train:
                xml_train.append(value)
            else:
                xml_test.append(value)

    column_name = ['filename', 'width', 'height',
                   'class', 'xmin', 'ymin', 'xmax', 'ymax']
    train_df = pd.DataFrame(xml_train, columns=column_name)
    test_df = pd.DataFrame(xml_test, columns=column_name)

    return train_df, test_df


def main():
    image_path = os.path.join(os.getcwd(), 'Images')
    train, test = xml_to_csv(image_path)

    train_path = os.path.join(os.getcwd(), 'train_cat_labels.csv')
    test_path = os.path.join(os.getcwd(), 'test_cat_labels.csv')

    train.to_csv(train_path, index=None)
    test.to_csv(test_path, index=None)

    print('Successfully converted xml to csv.')


main()
