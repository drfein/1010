import pygame
import random
from shapes import ALL_SHAPES
from model import load_model
import torch

# Constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 10
BLOCK_SIZE = 30  # Size of each block in pixels


# Colors
EMPTY_COLOR = (255, 255, 255)  # White
FILLED_COLOR = (0, 128, 255)   # Some shade of blue, change as needed

# Centering the board on screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_START_X = (SCREEN_WIDTH - (BOARD_WIDTH * BLOCK_SIZE)) // 2
BOARD_START_Y = 50


class Board:

    def __init__(self):
        # Initialize an empty board with all zeros
        self.grid = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def draw(self, screen, color_key):
        """
        Draw the board on the given screen.
        """
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                # Adjust the x and y positions by BOARD_START_X and BOARD_START_Y
                rect = pygame.Rect(BOARD_START_X + col*BLOCK_SIZE, BOARD_START_Y + row*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if self.grid[row][col] == 0:
                    pygame.draw.rect(screen, EMPTY_COLOR, rect)
                    pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw border
                else:
                    color = color_key[self.grid[row][col]]
                    pygame.draw.rect(screen, color, rect)

    def game_over(self, shapes):
        for shape in shapes:
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT):
                    if self.can_place_shape(shape, x, y):
                        return False
        return True

    def place_shape(self, shape, x, y, color):
        """
        Place a shape on the board at the given (x, y) position.
        Returns True if successful, False otherwise.
        """
        # First check if the placement is valid
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    # Check bounds
                    if row+y >= BOARD_HEIGHT or col+x >= BOARD_WIDTH:
                        return False
                    # Check if space is not occupied
                    if self.grid[row+y][col+x] != 0:
                        return False
        
        # Now place the shape
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    self.grid[row+y][col+x] = color

        self.clear_complete_lines()
        return True
    
    def simulate_place_shape(self, shape, x, y, color, grid=None):
        """
        Simulate placing a shape on the board at the given (x, y) position and return the hypothetical resultant board.
        """
        # Use the hypothetical grid if provided, else create a copy of the board to simulate the placement
        simulated_board = grid if grid else [row[:] for row in self.grid]

        # Simulate placing the shape
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    # Check bounds
                    if row+y >= BOARD_HEIGHT or col+x >= BOARD_WIDTH:
                        return None  # Return None if placement is out of bounds
                    # Check if space is not occupied
                    if simulated_board[row+y][col+x] != 0:
                        return None  # Return None if placement overlaps with existing shape
                    simulated_board[row+y][col+x] = color
    
        shape_size = sum(1 for row in shape for block in row if block)
        lines_cleared = self.clear_complete_lines(simulated_board)
        reward = (lines_cleared * 10 - shape_size) * 100 + self.get_density_reward_bonus(shape, x, y, color, simulated_board) * 10

        return (simulated_board, lines_cleared, reward)
    
    def get_density_reward_bonus(self, shape, x, y, color, grid=None):
        """
        For each block of the grid which the shape will newly occupy, the density reward adds a bonus for each existing block in that block's row and column.
        """
        board = grid if grid else [row[:] for row in self.grid]

        density_reward = 0
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col] == 1:
                    density_reward += sum(1 for block in board[row + y] if block != 0)
                    density_reward += sum(1 for row in board if row[col + x] != 0)
        return density_reward
    


    def can_place_shape(self, shape, x, y, grid=None):
        """
        Check if a shape can be placed at the given (x, y) position without overlap or out of bounds.
        """
        grid = grid if grid else [row[:] for row in self.grid]

        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    # Check bounds
                    if row + y >= BOARD_HEIGHT or col + x >= BOARD_WIDTH or row + y < 0 or col + x < 0:
                        return False
                    # Check if space is not occupied
                    if grid[row + y][col + x] != 0:
                        return False
        return True

    
    def clear_complete_lines(self, grid=None):
        """
        Clear any complete rows or columns.
        Returns the number of lines cleared.
        """
        lines_cleared = 0
        grid_to_clear = grid if grid else self.grid
        # Check rows
        for row in range(BOARD_HEIGHT):
            if all(grid_to_clear[row][col] != 0 for col in range(BOARD_WIDTH)):
                # Clear this row
                for col in range(BOARD_WIDTH):
                    grid_to_clear[row][col] = 0
                lines_cleared += 1
        
        # Check columns
        for col in range(BOARD_WIDTH):
            if all(grid_to_clear[row][col] != 0 for row in range(BOARD_HEIGHT)):
                # Clear this column
                for row in range(BOARD_HEIGHT):
                    grid_to_clear[row][col] = 0
                lines_cleared += 1
        
        return lines_cleared
    
    def clear_board(self):
        self.grid = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def shape_capacity(self, grid):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if grid[row][col] == 0:
                    grid[row][col] = 1
                else:
                    grid[row][col] = 0

        valid_positions = []
        for x in range(BOARD_WIDTH - 1):
            for y in range(BOARD_HEIGHT - 1):
                shapes_sample = ALL_SHAPES
                for shape in shapes_sample:
                    if not self.can_place_shape(shape, x, y, grid):
                        continue
                    else:
                        valid_positions.append((x, y))

        return len(valid_positions)
    
    def heuristic_score(self, grid, lines_cleared):
        shape_capacity_score = self.shape_capacity(grid)
        return shape_capacity_score + 100 * 300
    
    def empty_cells(self, grid):
        count = 0
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if grid[row][col] == 0:
                    count += 1
        return count
    
    def init_model(self, model_path="game_cnn_model.pth"):
        self.model = load_model(model_path)
        self.model.eval()
    
    def utility_approximation_cnn(self, grid=None):
        board = grid if grid else self.grid
        grid_state = [[1 if cell > 0 else 0 for cell in row] for row in board]

        # Convert the preprocessed board state to a PyTorch tensor with an added channel dimension
        board_state_tensor = torch.tensor(grid_state, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        
        # Use the model to estimate utility
        with torch.no_grad():
            estimated_utility = self.model(board_state_tensor).item()
        
        return estimated_utility
