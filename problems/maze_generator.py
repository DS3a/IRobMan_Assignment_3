import numpy as np
from typing import Tuple
import random


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        obstacle_density: float = 0.3,
        safety_distance: float = 5.0,
    ):
        self.width = width
        self.height = height
        self.safety_distance = safety_distance
        self.avg_rectangle_area = 20 * 20
        self.obstacle_density = obstacle_density
        self.maze = np.zeros((height, width))
        self.start = None
        self.goal = None

    def generate_random_rectangles(self, num_rectangles: int) -> None:
        for _ in range(num_rectangles):
            w = random.randint(15, 25)
            h = random.randint(15, 25)
            x = random.randint(0, self.width - w)
            y = random.randint(0, self.height - h)
            self.maze[y: y + h, x: x + w] = 1

    def check_safety_distance(self, x: float, y: float) -> bool:
        """Check if a point maintains safe distance from obstacles"""
        # Check points in a circle around (x,y)
        for dx in np.linspace(-self.safety_distance,
                              self.safety_distance, 8):
            for dy in np.linspace(-self.safety_distance,
                                  self.safety_distance, 8):
                check_x = int(x + dx)
                check_y = int(y + dy)
                # Check if point is within maze bounds
                if (
                    check_x < 0
                    or check_x >= self.width
                    or check_y < 0
                    or check_y >= self.height
                ):
                    return False
                # Check if point is too close to obstacle
                if self.maze[check_y, check_x] == 1:
                    return False
        return True

    def is_position_valid(self, x: float, y: float) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.maze[int(y), int(x)] == 0

    def find_valid_position(self) -> Tuple[float, float]:
        """Find a random valid position in the maze"""

        buffer = max(self.safety_distance, 0.0)

        max_attempts = 1000

        for _ in range(max_attempts):
            x = random.uniform(buffer, self.width - buffer)
            y = random.uniform(buffer, self.height - buffer)

            if self.is_position_valid(x, y) and self.check_safety_distance(x, y):
                return (x, y)

        return (0, 0)

    def generate(
        self,
    ) -> Tuple[np.ndarray, Tuple[float, float], Tuple[float, float]]:
        """Generate maze and return maze, start position, and goal position"""
        # Generate obstacles
        total_area = self.width * self.height
        desired_obstacle_area = total_area * self.obstacle_density
        num_rectangles = int(desired_obstacle_area / self.avg_rectangle_area)
        self.generate_random_rectangles(num_rectangles)

        # Generate valid start and goal positions
        start_x, start_y = self.find_valid_position()
        self.start = (start_x, start_y)

        # Ensure goal is sufficiently far from start
        while True:
            goal_x, goal_y = self.find_valid_position()
            # Check if goal is far enough from start (e.g., at least 40 units)
            if (((goal_x - start_x) ** 2 + (goal_y - start_y) ** 2) ** 0.5) >= 40:
                self.goal = (goal_x, goal_y)
                break

        return self.maze, self.start, self.goal

    def get_start_goal(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Return the start and goal positions"""
        if self.start is None or self.goal is None:
            raise ValueError("Maze hasn't been generated yet. Call generate() first.")
        return self.start, self.goal
