# dataLoaders.py

import json
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np

class GameDataset(Dataset):
    def __init__(self, data):
        self.data = data

        # Calculate mean and standard deviation for remaining score
        remaining_scores = np.array([item['remaining_score'] for item in data])
        self.score_mean = remaining_scores.mean()
        self.score_std = remaining_scores.std()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_item = self.data[idx]
        

        board_state = torch.tensor(data_item['board_state'], dtype=torch.float32).unsqueeze(0)

        remaining_score = np.array(data_item['remaining_score'], dtype=np.float32)
        normalized_remaining_score = (remaining_score - self.score_mean) / self.score_std
        remaining_score_tensor = torch.tensor([normalized_remaining_score], dtype=torch.float32)
        
        # remaining_score_tensor = torch.tensor([data_item['remaining_score']], dtype=torch.float32)
        
        return board_state, remaining_score_tensor

def read_jsonl_file(path):
    data = []
    with open(path, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))  # Parse each line individually
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {e}")
                continue
    return data

def get_data_loaders(path, batch_size=564, test_size=0.2):
    game_data = read_jsonl_file(path)

    train_data, val_data = train_test_split(game_data, test_size=test_size)

    train_dataset = GameDataset(train_data)
    val_dataset = GameDataset(val_data)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader

