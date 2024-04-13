import pygame
import random
import numpy as np
from .objects import Snake, Food

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class SnakeGame:
    def __init__(self, render=False):
        self.render = render
        if self.render:
            pygame.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Snake Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 30)

        self.reset()
        self.state_dimensions = len(self.get_game_state())

    def reset(self):
        snake_start_x = WINDOW_WIDTH // 2
        snake_start_y = WINDOW_HEIGHT // 2

        self.snake = Snake(snake_start_x, snake_start_y)
        food_start_x, food_start_y = self.get_random_position()
        self.food = Food(food_start_x, food_start_y)

        self.score = 0
        return self.get_game_state()

    def get_random_position(self):
        x = random.randrange(0, WINDOW_WIDTH // self.snake.size) * self.snake.size
        y = random.randrange(0, WINDOW_HEIGHT // self.snake.size) * self.snake.size
        return x, y

    def step(self, action):
        """
        Executes one step in the game based on the given action, updates the game state, and returns the result of the step.

        Parameters:
        - action: The direction in which the snake should move.

        Returns:
        - done: A boolean indicating whether the game is over (True if the game is over, otherwise False).
        - reward: An integer representing the reward obtained in this step. Eating food gives a positive reward, hitting a wall or itself gives a negative reward.
        - self.score: The current score of the game.
        - state: The current state of the game, represented as a numpy array.
        """
        done = False
        self.snake.change_direction(action)  # Change the direction of the snake based on the action
        self.snake.move()  # Move the snake in the new direction

        head = self.snake.body[0]  # Get the new head position after moving
        food_eaten = (head[0] == self.food.x and head[1] == self.food.y)  # Check if the snake has eaten the food

        reward = 0  # Initialize reward

        if food_eaten:  # If food is eaten
            self.score += 1  # Increase score
            self.snake.grow()  # Grow the snake
            reward = 10  # Assign positive reward
            # print("Eaten")

        if self.check_collision():  # Check for collision with walls or itself
            done = True  # End the game if a collision is detected
            reward = -10  # Assign negative reward

        state = self.get_game_state()  # Get the current game state

        if food_eaten:  # If food was eaten
            self.respawn_food()  # Respawn food at a new location

        if self.render:  # If rendering is enabled
            self.update_ui()  # Update the game UI

        return done, reward, self.score, state  # Return the step result

    def update_ui(self):
        self.screen.fill((0, 0, 0))

        # drawing snake

        for segment in self.snake.body:
            border_size = 2  # Adjust the border size as needed
            # Draw the red rectangle (border)
            pygame.draw.rect(self.screen, (0, 0, 255),
                             pygame.Rect(segment[0], segment[1], self.snake.size, self.snake.size))
            # Draw the black rectangle (inner) slightly smaller and centered within the red rectangle
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(segment[0] +
                                                                 border_size, segment[1] + border_size,
                                                                 self.snake.size - 2 * border_size,
                                                                 self.snake.size - 2 * border_size))

        # drawing food
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(
            self.food.x, self.food.y, self.food.size, self.food.size
        ))

        # drawing score
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.update()
        self.clock.tick(30)

    def check_collision(self, point=None):
        if point is None:
            point = self.snake.body[0]

        if point[0] < 0 or point[0] >= WINDOW_WIDTH or point[1] < 0 or point[1] >= WINDOW_HEIGHT:
            return True

        if point in self.snake.body[1:]:
            return True

        return False

    def respawn_food(self):
        self.food.x, self.food.y = self.get_random_position()

    def get_game_state(self):
        head = self.snake.body[0]
        size = self.snake.size
        directions = {
            'right': (size, 0),
            'left': (-size, 0),
            'up': (0, -size),
            'down': (0, size)
        }
        danger = {
            'right': [0, 0, 0, 0],
            'left': [0, 0, 0, 0],
            'up': [0, 0, 0, 0],
            'down': [0, 0, 0, 0]
        }

        # Check for danger in each direction and fill danger distances
        for direction, (dx, dy) in directions.items():
            for step in range(1, 5):  # Check up to 4 blocks away
                check_point = (head[0] + dx * step, head[1] + dy * step)
                if self.check_collision(check_point):
                    for i in range(step, 5):  # Mark all steps from here to max as dangerous
                        danger[direction][i - 1] = 1 / step  # Normalize by inverse of distance (closer = higher value)
                    break

        # Euclidean distance between head and food
        point_1 = np.array([head[0], head[1]])
        point_2 = np.array([self.food.x, self.food.y])
        euclidean_distance = np.linalg.norm(point_1 - point_2)
        max_distance = np.sqrt(WINDOW_WIDTH ** 2 + WINDOW_HEIGHT ** 2)
        normalized_distance_to_food = euclidean_distance / max_distance

        # normalized angle between head and food
        angle_to_food = np.arctan2(point_2[1] - point_1[1], point_2[0] - point_1[0]) * 180 / np.pi
        normalized_angle_to_food = (angle_to_food + 180) / 360

        state = [
            *danger['right'],
            *danger['left'],
            *danger['up'],
            *danger['down'],
            normalized_distance_to_food,
            normalized_angle_to_food
        ]

        return np.array(state)
