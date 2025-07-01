import pygame
from animace import AnimationLoader

def pil_to_pygame(image):
    """Convert PIL Image to Pygame Surface."""
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

def test_animation(spritesheet, row, frame_count, frame_width, frame_height, fps=10):
    pygame.init()
    screen = pygame.display.set_mode((frame_width * 2, frame_height * 2))
    pygame.display.set_caption("Animation Test")

    loader = AnimationLoader(spritesheet, frame_width, frame_height)
    frames = loader.load_animation(row, frame_count)
    pg_frames = [pil_to_pygame(f) for f in frames]

    clock = pygame.time.Clock()
    running = True
    frame_idx = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        frame = pg_frames[frame_idx]
        # Center the frame
        rect = frame.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(frame, rect)
        pygame.display.flip()

        frame_idx = (frame_idx + 1) % len(pg_frames)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    # Example usage: change parameters as needed
    test_animation(
        spritesheet="Animace/spritesheets/test_sheet.png",  # path to your spritesheet (inside Animace)
        row=0,                # which row to use
        frame_count=2,        # how many frames in the animation
        frame_width=16,       # width of each frame
        frame_height=16,      # height of each frame
        fps=2                 # animation speed
    )