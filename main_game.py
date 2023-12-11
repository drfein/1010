import pygame
from gameAPI import GameAPI  # Import the GameAPI class
from gameAPI import RandomAgent, GreedyHeuristicAgent, BellmanAgent, LookaheadRolloutAgent, DeepAgent, DeepBellmanAgent
# from policy_x import PolicyXAgent  # Import other agent classes as needed
from board import Board, BLOCK_SIZE, BOARD_HEIGHT, BOARD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from shapes import ALL_SHAPES, SHAPE_COLORS, COLOR_KEY 
from tqdm import tqdm
import json
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('1010 Game')

game_board = Board()
api = GameAPI(game_board, ALL_SHAPES, SHAPE_COLORS)

# AGENT_CLASS = GreedyHeuristicAgent
# AGENT_CLASS = LookaheadRolloutAgent
AGENT_CLASS = BellmanAgent
# AGENT_CLASS = DeepAgent
# AGENT_CLASS = DeepBellmanAgent
# AGENT_CLASS = RandomAgent
SIMULATIONS = 100

# Initialize the agent
agent = AGENT_CLASS(api)

# Function to draw the game state
def draw_game(screen, game_board, next_shapes, score):  # Add 'score' as a parameter
    # Clear screen
    screen.fill((255, 255, 255))  # Fill screen with white or any background color
    
    # Draw the board
    game_board.draw(screen, COLOR_KEY)
    
    # Draw the next shapes
    for i, shape in enumerate(next_shapes):
        draw_shape(screen, shape, i)
        
    # Draw the score
    font = pygame.font.Font(None, 36)  # You can choose a different font and size
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Render the score text
    screen.blit(score_text, (10, 10))  # Draw the text on the screen at position (10, 10)

    pygame.display.flip()  # Update the full display


def draw_shape(screen, shape, index):
    shape_color = COLOR_KEY[SHAPE_COLORS[shape]]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    shape_color,
                    pygame.Rect(
                        (index * 100 + 20 + x * BLOCK_SIZE, 
                         SCREEN_HEIGHT - 100 + y * BLOCK_SIZE), 
                        (BLOCK_SIZE, BLOCK_SIZE)
                    )
                )
            else:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),  # White to 'remove' the shape
                    pygame.Rect(
                        (index * 100 + 20 + x * BLOCK_SIZE, 
                         SCREEN_HEIGHT - 100 + y * BLOCK_SIZE), 
                        (BLOCK_SIZE, BLOCK_SIZE)
                    ),
                    0  # Fill the rectangle to 'remove' the shape
                )



# Initial draw of the game state, including the first set of three shapes
# Update the display after each move
draw_game(screen, game_board, agent.next_shapes, api.get_score())

# Main game loop

def play_one_game():
    running = True
    game_data = []
    final_score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # If there are no more shapes to place, get new shapes and draw them before continuing
        if not agent.next_shapes:
            agent.next_shapes = agent.api.get_new_shapes(3)  # Get a new set of three shapes
            # Update the display after each move
            draw_game(screen, game_board, agent.next_shapes, api.get_score())
            # Draw the new shapes
            pygame.display.flip()  # Update the display

        current_board_state = [[1 if cell > 0 else 0 for cell in row] for row in game_board.grid]
        current_score = api.get_score()

        # Let the agent make its move
        # pygame.time.delay(100)
        if not agent.play_turn():
            final_score = api.get_score()
            running = False
        else:
            # Update the display after each move
            draw_game(screen, game_board, agent.next_shapes, api.get_score())
            pygame.display.flip()  # Update the display

        game_data.append({'board_state': current_board_state, 'remaining_score': current_score})

    for turn in game_data:
        turn['remaining_score'] = final_score - turn['remaining_score']

    return game_data


def append_jsonl(data_list, file_path):
    with open(file_path, 'a') as file:  # Open file in append mode
        for data in data_list:
            json_line = json.dumps(data)  # Convert each data item to JSON string
            file.write(json_line + '\n')  # Write JSON string as a new line

def score_five():
    scores = []
    for i in tqdm(range(5)):
        game_data = play_one_game()
        scores.append(game_data[0].get('remaining_score'))
        api.reset_game()
    return np.array(scores).mean()

if __name__ == "__main__":
    scores = []
    file_path = 'game_data.jsonl'  # Use .jsonl extension for JSON Lines format

    for i in tqdm(range(SIMULATIONS)):
        game_data = play_one_game()
        scores.append(game_data[0].get('remaining_score'))
        append_jsonl(game_data, file_path)
        api.reset_game()
        
    avg_score = sum(scores) / len(scores)
    print(f"Average score: {avg_score}")
    import matplotlib.pyplot as plt
    import numpy as np

    avg_score = sum(scores) / len(scores)
    print(f"Average score: {avg_score}")
    import matplotlib.pyplot as plt
    import numpy as np

    plt.hist(scores, bins=10)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Distribution of Scores')
    plt.show()



    pygame.quit()

