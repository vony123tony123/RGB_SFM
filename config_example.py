import torch
from utils import increment_path
from pathlib import Path
import shutil
import os

project = "paper experiment"
name = "SFMCNN"
group = "1/25"
tags = ["SFMCNN", "Rewrite"]
description = "1/25 測試 face 資料集"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

lr_scheduler = {
    "name": "ReduceLROnPlateau",
    "args":{
        "patience": 100
    }
}

optimizer = {
    "name":"Adam",
    "args":{

    }
}

arch = {
    "name": 'SFMCNN',
    "args":{
        "in_channels": 1,
        "out_channels": 2,
        "Conv2d_kernel": [(23,23), (1, 1), (1, 1), (1, 1), (1, 1)],
        "SFM_filters": [(3, 3), (2, 1), (1, 2)],
        "channels": [1, 100, 225, 625, 1225],
        "strides": [1, 1, 1, 1, 1],
        "paddings": [0, 0, 0, 0, 0],
        "w_arr": [25.45, 12.45, 17.45, 27.45],
        "percent": [0.5, 0.4, 0.3, 0.2, 0.2],
        "fc_input": 60025,
        "device": device
    }
}

# arch = {
#     "name": 'SFMCNN_old',
#     "args":{
#         "in_channels": 1,
#         "out_channels": 10,
#     }
# }

# arch = {
#     "name": 'AlexNet',
#     "args":{
#         "num_classes":15
#     }
# }

config = {
    "device": device,
    "root": os.path.dirname(__file__),
    "save_dir": './runs/train/exp',
    "model": arch,
    "dataset": 'face_dataset',
    "input_shape": (64, 64),
    "rbf": "triangle",
    "batch_size": 128,
    "epoch" : 10,
    "lr" : 0.001,
    "lr_scheduler": lr_scheduler,
    "optimizer": optimizer,
    "loss_fn": "CrossEntropyLoss",
}