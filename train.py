# train.py

import torch
import torch.optim as optim
import torch.nn as nn
import matplotlib.pyplot as plt
from dataLoaders import get_data_loaders
from model import GameCNN
from main_game import score_five

def validate_model(model, val_loader, criterion):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
    return total_loss / len(val_loader)

def main():
    # train_loader, val_loader = get_data_loaders('game_data.jsonl', batch_size=2048, test_size=0.2)
    train_loader, val_loader = get_data_loaders('game_data_heuristic.jsonl', batch_size=512, test_size=0.01)
    model = GameCNN()
    criterion = nn.MSELoss()
    # optimizer = optim.Adam(model.parameters(), lr=0.00005)  # Smaller learning rate
    optimizer = optim.Adam(model.parameters(), lr=0.00005)

    train_losses = []
    val_losses = []
    game_score = 0
    for epoch in range(15):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)
        val_loss = validate_model(model, val_loader, criterion)

        train_losses.append(train_loss)
        val_losses.append(val_loss)

        model_path = "game_cnn_model.pth"
        torch.save({
            'model_state_dict': model.state_dict(),
            'model_architecture': GameCNN.__name__,
        }, model_path)
        if epoch % 5 == 0:
            game_score = score_five()
        print(f"Epoch {epoch+1}, Training Loss: {train_loss}, Validation Loss: {val_loss}, Game Score: {game_score}")



    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.title('Training and Validation Losses')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()