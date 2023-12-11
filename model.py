# model.py

import torch.nn as nn
import torch.nn.functional as F
import torch

class GameCNN(nn.Module):
    def __init__(self):
        self.training = False
        super(GameCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.fc1 = nn.Linear(128, 256)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 1)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2)
        if self.training:
            x = self.dropout(x)
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2)
        x = x.view(-1, 32 * 2 * 2)
        x = F.relu(self.fc1(x))
        if self.training:
            x = self.dropout(x)
        x = self.fc2(x)
        return x


def load_model(model_path):
    checkpoint = torch.load(model_path)
    model = GameCNN()
    model.load_state_dict(checkpoint['model_state_dict'])
    return model
