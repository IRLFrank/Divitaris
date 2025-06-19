import os
from PIL import Image

class AnimationLoader:
    def __init__(self, spritesheet_path, frame_width, frame_height):
        self.image = Image.open(spritesheet_path)
        self.frame_width = frame_width
        self.frame_height = frame_height

    def load_animation(self, row, frame_count):
        frames = []
        for i in range(frame_count):
            x = i * self.frame_width
            y = row * self.frame_height
            box = (x, y, x + self.frame_width, y + self.frame_height)
            frame = self.image.crop(box)
            frames.append(frame)
        return frames

class AnimationManager:
    def __init__(self):
        self.animations = {}

    def add_animation(self, name, spritesheet_path, row, frame_count, frame_width, frame_height):
        loader = AnimationLoader(spritesheet_path, frame_width, frame_height)
        frames = loader.load_animation(row, frame_count)
        self.animations[name] = frames

    def get_animation(self, name):
        return self.animations.get(name, [])

# Example usage:
# manager = AnimationManager()
# manager.add_animation("run", "spritesheets/test_sheet.png", 0, 6, 64, 64)
# frames = manager.get_animation("run")
