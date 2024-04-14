import random

# points = x, y
BLOCK_SIZE = 20


class BaseObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BLOCK_SIZE


def get_direction(action: int):
    # going clockwise
    if action == 0:
        return "right"
    elif action == 1:
        return "down"
    elif action == 2:
        return "left"
    elif action == 3:
        return "up"
    else:
        return "right"


class Snake(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = "right"
        self.body = [[self.x, self.y]]

    def change_direction(self, action: int):
        direction = get_direction(action)
        if direction == self.direction:
            return
        if direction == "right" and self.direction == "left":
            return
        if direction == "left" and self.direction == "right":
            return
        if direction == "up" and self.direction == "down":
            return
        if direction == "down" and self.direction == "up":
            return
        self.direction = direction

    def move(self):
        head = self.body[0][:]  # Make a shallow copy of the head coordinates
        if self.direction == "right":
            head[0] += self.size
        elif self.direction == "left":
            head[0] -= self.size
        elif self.direction == "up":
            head[1] -= self.size
        elif self.direction == "down":
            head[1] += self.size

        # Insert the new head at the beginning of the body list
        self.body.insert(0, head)
        # Remove the last segment, unless growing
        self.body.pop()

        # Update the current position with the new head's position
        self.x, self.y = head[0], head[1]

    def grow(self):
        tail = self.body[-1]
        # print(f"Tail: {tail}")
        new_segment = [tail[0], tail[1]]  # Initialize new_segment to be the same as tail

        # Adjust new_segment based on the direction to place it behind the tail
        if self.direction == "right":
            new_segment[0] = tail[0] - self.size  # Move new segment to the left of the tail
        elif self.direction == "left":
            new_segment[0] = tail[0] + self.size  # Move new segment to the right of the tail
        elif self.direction == "up":
            new_segment[1] = tail[1] + self.size  # Move new segment below the tail
        elif self.direction == "down":
            new_segment[1] = tail[1] - self.size  # Move new segment above the tail

        # print(f"Adding new segment: {new_segment}")
        self.body.append(new_segment)  # Append the new segment behind the current tail
        # print(f"Body: {self.body}")
        # print(f'Current length: {len(self.body)}')


class Food(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y)


