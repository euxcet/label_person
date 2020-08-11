import os
import random
import pandas as pd
from shutil import copyfile
from model import ResNet50

import torch
import torch.nn as nn
import torch.optim as optim
import time
from torch.optim import lr_scheduler
from torch.autograd import Variable

from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision import transforms
from trochvision import models

import matplotlib.pyplot as plt
from PIL import Image

def make_weights_for_balanced_classes(images, nclasses):
    count = [0] * nclasses
    for item in images:
        count[item[1]] += 1
    weight_per_class = [0.] * nclasses
    N = float(sum(count))
    for i in range(nclasses):
        weight_per_class[i] = N / max(1.0, float(count[i]))
    weight = [0] * len(images)
    for idx, val in enumerate(images):
        weight[idx] = weight_per_class[val[1]]
    return weight

def train_model(model, data_sizes, num_epochs, scheduler, dataloaders,criterion, optimizer, ):
    device1 = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    since = time.time()

    best_model_wts = model.state_dict()
    best_acc = 0.0

    for epoch in range(num_epochs):
        begin_time = time.time()
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('*'*20)

        for phase in ['train', 'val']:
            count_batch = 0
            if phase == 'train':
                model.train(True)
            else:
                model.train(False)
            running_loss = 0.0
            running_corrects = 0.0
            for i, data in enumerate(dataloaders[phase]):
                count_batch += 1

                inputs, labels = data
                
                #print(labels)
                #print(inputs, labels)

                if use_gpu:
                    inputs = Variable(inputs.cuda())
                    labels = Variable(labels.cuda())
                    #inputs = inputs.cuda()
                    #labels = labels.cuda()
                    #labels = Variable(torch.from_numpy(np.array(labels)).long()).cuda()
                else:
                    inputs, labels = Variable(inputs), Variable(labels)
                optimizer.zero_grad()
                outputs = model(inputs)
                out = torch.argmax(outputs.data, 1)
                #print(torch.argmax(outputs.data, 1))
                _, preds = torch.max(outputs.data, 1)

                #print('labels:', labels)
                #print('preds:', preds)
                loss = criterion(outputs, labels)
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
                    scheduler.step()

                running_loss += loss.data
                running_corrects += torch.sum(preds == labels.data).to(torch.float32)

                if count_batch % 10==0:
                    #print('batch_size * count_batch:', batch_size * count_batch)
                    batch_loss = running_loss / (batch_size * count_batch)
                    batch_acc = running_corrects / (batch_size * count_batch)
                    print('{} Epoch [{}] Batch Loss: {:.4f} Acc:{:.4f} Time: {:.4f}s'.format(
                        phase, epoch, batch_loss, batch_acc, time.time()-begin_time
                    ))
                    begin_time = time.time()
        epoch_loss = running_loss / data_sizes[phase]
        epoch_acc = running_corrects / data_sizes[phase]
        print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

        if phase == 'train':
            if not os.path.exists(model_path):
                os.mkdir(model_path)
            torch.save(model, os.path.join(model_path, 'resnet_epoch{}.pkl').format(epoch))

        if phase == 'val' and epoch_acc > best_acc:

            best_acc = epoch_acc
            best_model_wts = model.state_dict()

        time_elapsed = time.time() - since
        print('Training completed in {:.0f}mins {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:.4f}'.format(best_acc))

        model.load_state_dict(best_model_wts)
    return(model)



if __name__ == '__main__':
    batch_size = 2
    transform = {
        'train': transforms.Compose([
            transforms.Resize((224, 224)),
            #transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[.485, .456, .406], std=[.229, .224, .225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((224, 224)),
            #transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[.485, .456, .406], std=[.229, .224, .225])
        ]),
        'test': transforms.Compose([
            transforms.Resize((224, 224)),
            #transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[.485, .456, .406], std=[.229, .224, .225])
        ])
    }
    dataset = {
        name : datasets.ImageFolder(os.path.join('./data/face', name), transform[name]) for name in ['train', 'val', 'test']
    }
    weights = make_weights_for_balanced_classes(dataset['train'].imgs, len(dataset['train'].classes))
    weights = torch.DoubleTensor(weights)
    print(weights)
    exit(0)
    sampler = torch.utils.data.sampler.WeightedRandomSampler(weights, len(weights))
    dataloader = {
        'train': DataLoader(dataset['train'], batch_size=batch_size, sampler=sampler),
        'val': DataLoader(dataset['val'], batch_size=batch_size, shuffle=True),
        'test': DataLoader(dataset['test'], batch_size=1, shuffle=False)
    }
    data_size = {name:len(dataset[name]) for name in ['train', 'val']}

    use_gpu = torch.cuda.is_available()

    model = ResNet50()
    if use_gpu:
        model.cuda()
    

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(),lr = 0.005, momentum=0.9)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=5,gamma=0.2)

    num_epochs = 10

    
    model = train_model(model=model,
                        data_sizes = data_size,
                        dataloaders=dataloader,
                        num_epochs = num_epochs,
                        scheduler=exp_lr_scheduler,
                        criterion=criterion,
                        optimizer= optimizer)

