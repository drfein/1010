import random
import itertools
import copy  # Import copy module for deep copy
from board import BOARD_HEIGHT, BOARD_WIDTH

class GameAPI:
    def __init__(self, board, shapes, shape_colors):
        self.board = board
        self.score = 0
        self.shapes = shapes
        self.shape_colors = shape_colors
        self.next_shapes = [random.choice(self.shapes) for _ in range(3)]

    def view_next_pieces(self):
        """Return a list of the next shapes to b``e played."""
        return self.next_shapes

    def get_valid_positions(self, shape, grid=None):
        """Get all valid positions for the given shape."""
        grid = grid if grid else self.board.grid
        valid_positions = []
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.board.can_place_shape(shape, x, y, grid=grid):
                    valid_positions.append((x, y))
        return valid_positions

    def place_piece(self, shape, position):
        """Attempt to place a piece at the specified position."""
        if self.board.can_place_shape(shape, position[0], position[1]):
            color = self.shape_colors[shape]
            self.board.place_shape(shape, position[0], position[1], color)
            self.score += sum(1 for row in shape for block in row if block)
            return True
        return False
    
    def simulate_placement(self, shape, position, grid=None):
        """ Returns the hypothetical grid and score if a placement was made"""
        if grid is None:
            grid = [row[:] for row in self.board.grid]
        if self.board.can_place_shape(shape, position[0], position[1], grid=grid):
            color = self.shape_colors[shape]
            hypothetical_result = self.board.simulate_place_shape(shape, position[0], position[1], color)
            result_grid = hypothetical_result[0]
            reward = hypothetical_result[2]
            lines_cleared = hypothetical_result[1]
            return (reward, result_grid, lines_cleared)
        return None

    def clear_lines(self):
        """Clear complete lines on the board."""
        return self.board.clear_complete_lines()
    
    def get_score(self):
        """Get the current score."""
        return self.score
    
    def reset_game(self):
        self.score = 0
        self.board.clear_board()
        return True

    def is_game_over(self):
        """Check if the game is over."""
        return self.board.game_over(self.next_shapes)

    def get_new_shapes(self, count):
        """Get a new set of random shapes."""
        return [random.choice(self.shapes) for _ in range(count)]

class RandomAgent:
    def __init__(self, api):
        self.api = api
        self.next_shapes = self.api.get_new_shapes(3)  # Initialize with three random shapes

    def play_turn(self):
        """Play a single turn using a random move."""
        if not self.next_shapes:  # If no shapes are left, get a new set of three shapes
            self.next_shapes = self.api.get_new_shapes(3)
        
        shape = random.choice(self.next_shapes)
        valid_positions = self.api.get_valid_positions(shape)
        
        if valid_positions:
            position = random.choice(valid_positions)
            self.api.place_piece(shape, position)
            self.next_shapes.remove(shape)

        else:
            return False
        return True



class GreedyHeuristicAgent:
    def __init__(self, api):
        self.api = api
        self.board = api.board
        self.next_shapes = self.api.get_new_shapes(3)  # Initialize with three random shapes

    def play_turn(self):
        """Play a single turn using a random move."""
        if not self.next_shapes:  # If no shapes are left, get a new set of three shapes
            self.next_shapes = self.api.get_new_shapes(3)
        
        best_shape = None
        best_position = None
        max_score = float('-inf')
        for shape in self.next_shapes:
            valid_positions = self.api.get_valid_positions(shape)
            for position in valid_positions:
                simulation = self.api.simulate_placement(shape, position)
                reward = simulation[0]
                hypothetical_board = simulation[1]
                lines_cleared = simulation[2]
                if hypothetical_board:
                    score = self.board.heuristic_score(hypothetical_board, lines_cleared)
                    if score > max_score:
                        max_score = score
                        best_shape = shape
                        best_position = position
        if best_shape and best_position:
            self.api.place_piece(best_shape, best_position)
            self.next_shapes.remove(best_shape)
        else:
            return False
        return True
    
class BellmanAgent:
    def __init__(self, api):
        self.api = api
        self.board = api.board
        self.next_shapes = self.api.get_new_shapes(3)  # Initialize with three random shapes

    def play_turn(self):
        """Play a single turn using a random move."""
        if not self.next_shapes:  # If no shapes are left, get a new set of three shapes
            self.next_shapes = self.api.get_new_shapes(3)
        
        best_shape = None
        best_position = None
        max_score = float('-inf')
        for shape in self.next_shapes:
            valid_positions = self.api.get_valid_positions(shape)
            for position in valid_positions:
                simulation = self.api.simulate_placement(shape, position)
                reward = simulation[0]
                hypothetical_board = simulation[1]
                lines_cleared = simulation[2]
                if hypothetical_board:
                    score = reward
                    score += self.board.heuristic_score(hypothetical_board, lines_cleared)
                    if score > max_score:
                        max_score = score
                        best_shape = shape
                        best_position = position
        if best_shape and best_position:
            self.api.place_piece(best_shape, best_position)
            self.next_shapes.remove(best_shape)
        else:
            return False
        return True



class LookaheadRolloutAgent:
    def __init__(self, api, lookahead_depth=4, rollout_depth=4, num_rollouts=5):
        self.api = api
        self.lookahead_depth = lookahead_depth
        self.rollout_depth = rollout_depth
        self.num_rollouts = num_rollouts
        self.next_shapes = self.api.get_new_shapes(3)  # Initialize with three random shapes

    def play_turn(self):
        if not self.next_shapes:
            self.next_shapes = self.api.get_new_shapes(3)

        best_move = None
        best_score = float('-inf')

        for move in self.get_possible_moves(self.next_shapes, self.lookahead_depth):
            simulated_api = copy.deepcopy(self.api)
            simulated_api.next_shapes = self.next_shapes[:]  # Copy current shapes for the simulation
            score = self.simulate_rollouts(simulated_api, move, self.rollout_depth, self.num_rollouts)
            
            if score > best_score:
                best_score = score
                best_move = move

        if best_move:
            shape, position = best_move
            self.api.place_piece(shape, position)
            self.next_shapes.remove(shape)
            return True
        else:
            return False

    def get_possible_moves(self, shapes, depth):
        if depth == 0 or not shapes:
            return []
        
        moves = []
        for shape in shapes:
            valid_positions = self.api.get_valid_positions(shape)
            for position in valid_positions:
                moves.append((shape, position))

        return moves

    def simulate_rollouts(self, api, initial_move, depth, num_rollouts):
        total_score = 0
        for _ in range(num_rollouts):
            simulated_api = copy.deepcopy(api)
            simulated_shapes = self.next_shapes[:]  # Copy the shapes for each simulation
            if initial_move in simulated_shapes:
                simulated_shapes.remove(initial_move[0])
                simulated_api.place_piece(*initial_move)

            for _ in range(depth):
                if not simulated_shapes:
                    simulated_shapes = simulated_api.get_new_shapes(3)

                best_move = self.heuristic_move(simulated_api, simulated_shapes)
                if best_move:
                    shape, position = best_move
                    simulated_api.place_piece(shape, position)
                    simulated_shapes.remove(shape)
                else:
                    break

            total_score += simulated_api.get_score()

        return total_score / num_rollouts

    def heuristic_move(self, api, shapes):
        best_shape = None
        best_position = None
        max_score = float('-inf')
        for shape in shapes:
            valid_positions = api.get_valid_positions(shape)
            for position in valid_positions:
                simulation = api.simulate_placement(shape, position)
                reward = simulation[0]
                hypothetical_board = simulation[1]
                lines_cleared = simulation[2]
                if hypothetical_board:
                    score = reward
                    if score > max_score:
                        max_score = score
                        best_shape = shape
                        best_position = position
        return (best_shape, best_position) if best_shape and best_position else None
    

class DeepAgent:
    def __init__(self, api):
        self.api = api
        self.board = api.board
        self.next_shapes = self.api.get_new_shapes(3)  # Initialize with three random shapes

    def play_turn(self):
        """Play a single turn using a random move."""
        if not self.next_shapes:  # If no shapes are left, get a new set of three shapes
            self.next_shapes = self.api.get_new_shapes(3)
        
        best_shape = None
        best_position = None
        max_score = float('-inf')
        for shape in self.next_shapes:
            valid_positions = self.api.get_valid_positions(shape)
            for position in valid_positions:
                simulation = self.api.simulate_placement(shape, position)
                hypothetical_board = simulation[1]
                if hypothetical_board:
                    self.board.init_model()
                    score = self.board.utility_approximation_cnn(hypothetical_board)
                    if score > max_score:
                        max_score = score
                        best_shape = shape
                        best_position = position
        if best_shape and best_position:
            self.api.place_piece(best_shape, best_position)
            self.next_shapes.remove(best_shape)
        else:
            return False
        return True
    


class DeepBellmanAgent:
    def __init__(self, api):
        self.api = api
        self.board = api.board
        self.next_shapes = self.api.get_new_shapes(3)  # Initialize with three random shapes

    def play_turn(self):
        """Play a single turn using a random move."""
        if not self.next_shapes:  # If no shapes are left, get a new set of three shapes
            self.next_shapes = self.api.get_new_shapes(3)
        
        best_shape = None
        best_position = None
        max_score = float('-inf')
        for shape in self.next_shapes:
            valid_positions = self.api.get_valid_positions(shape)
            for position in valid_positions:
                simulation = self.api.simulate_placement(shape, position)
                reward = simulation[0]
                hypothetical_board = simulation[1]
                if hypothetical_board:
                    score = reward
                    self.board.init_model()
                    score += self.board.utility_approximation_cnn(hypothetical_board) * 300
                    if score > max_score:
                        max_score = score
                        best_shape = shape
                        best_position = position
        if best_shape and best_position:
            self.api.place_piece(best_shape, best_position)
            self.next_shapes.remove(best_shape)
        else:
            return False
        return True