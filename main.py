import pygame
from Animace.animace_setup import setup_animations

def pil_to_pygame(image):
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

def main():
    width = 1980
    height = 1080
    title = "Divitaris Game"

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    # Get all animations from setup
    manager = setup_animations()
    pil_frames = manager.get_animation("run")
    pg_frames = [pil_to_pygame(f) for f in pil_frames]

    clock = pygame.time.Clock()
    running = True
    frame_idx = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((100, 100, 100))
        if pg_frames:
            frame = pg_frames[frame_idx]
            rect = frame.get_rect(center=(width // 2, height // 2))
            screen.blit(frame, rect)
            frame_idx = (frame_idx + 1) % len(pg_frames)
        pygame.display.flip()
        clock.tick(4)

    pygame.quit()

if __name__ == "__main__":
    main()