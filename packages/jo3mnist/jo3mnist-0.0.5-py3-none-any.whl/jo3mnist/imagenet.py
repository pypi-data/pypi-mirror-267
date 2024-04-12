#! /usr/bin/env python3
# vim:fenc=utf-8


from pathlib import Path
from typing import Union

import cv2
import datasets
import numpy as np
import torch
from torch import Tensor
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.transforms import functional as F_vision


def download_imagenet(directory):
    ds = datasets.load_dataset('imagenet-1k')
    ds.save_to_disk(directory)


class ImageNet(Dataset):
    def __init__(self, directory, image_size=224):
        self.set = datasets.Dataset.load_from_disk(str(directory))

        self.pre_transform = transforms.Compose([
            transforms.Resize(256, antialias=True),
            transforms.CenterCrop([224, 224]),
            transforms.Resize(image_size, antialias=True),
        ])
        self.post_transform = transforms.Compose([
            transforms.ConvertImageDtype(torch.float),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])

    def __getitem__(self, i):
        image_label = self.set[i]
        image, label = image_label["image"], image_label["label"]
        # Data preprocess
        image = self.pre_transform(image)
        # Convert image data into Tensor stream format (PyTorch).
        # Note: The range of input and output is between [0, 1]
        image = F_vision.to_tensor(image)
        # Data postprocess
        if image.shape[0] == 1:
            image = image.repeat(3, 1, 1)
        image = self.post_transform(image)
        return image, label

    def __len__(self):
        return len(self.set)
