from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision import transforms
import pandas as pd
import pymongo
import random
import os
from shutil import copyfile
import model

def makedirs(path):
    try:
        os.makedirs(path)
    except:
        pass

def argmax(value):
    res = 0
    maxv = 0
    for i in range(0, 5):
        if value[i] > maxv:
            maxv = value[i]
            res = i
    return res

def pack_face(save_folder):
    random.seed(123456)
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['face']
    figure_meta = db['figure']
    #  path face times width height x y
    score_col = db['score']
    # id path score 0 error 1 up 2 down 3 left 4 right

    folder = dict()

    for x in ['train', 'val', 'test']:
        folder[x] = {
            'left_folder': os.path.join(os.path.join(save_folder, x), 'left'),
            'right_folder': os.path.join(os.path.join(save_folder, x), 'right'),
            'up_folder': os.path.join(os.path.join(save_folder, x), 'up'),
            'down_folder': os.path.join(os.path.join(save_folder, x), 'down')
        }
        makedirs(folder[x]['left_folder'])
        makedirs(folder[x]['right_folder'])
        makedirs(folder[x]['up_folder'])
        makedirs(folder[x]['down_folder'])

    score_dict = dict()

    score_cnt = 0

    for x in score_col.find():
        score_cnt += 1
        face = None
        p = 0.0

        for y in figure_meta.find({'path': x['path']}):
            face = y['face']
            p = float(y['x']) / float(y['width'])

        if p < 0.4 or p > 0.5:
            continue

        if face is not None:
            if face not in score_dict:
                value = [0, 0, 0, 0, 0]
                value[x['score']] = 1
                score_dict[face] = value
            else:
                score_dict[face][x['score']] += 1

    for (key, value) in score_dict.items():
        score = argmax(value)
        new_filename = key.split('\\')[-3] + '_' + key.split('\\')[-1]
        rand_v = random.randint(0, 9)
        x = 'train'
        if rand_v > 8:
            x = 'test'
        elif rand_v > 7:
            x = 'val'

        if score == 1:
            copyfile(key, os.path.join(folder[x]['up_folder'], new_filename))
        elif score == 2:
            copyfile(key, os.path.join(folder[x]['down_folder'], new_filename))
        elif score == 3:
            copyfile(key, os.path.join(folder[x]['left_folder'], new_filename))
        elif score == 4:
            copyfile(key, os.path.join(folder[x]['right_folder'], new_filename))
            

    print('Label times:', score_cnt)
    print('Valid figures:', len(score_dict))


if __name__ == '__main__':
    pack_face('data\\face')