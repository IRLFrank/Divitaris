import pygame
import random
from Animace.animace_setup import setup_animations
from Vypravy.mapa.mapa_vypravy import (
    generate_start_points, generate_end_point, generate_path_between,
    generate_paths_no_overlap, generate_tile_types, draw_path
)

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
    font = pygame.font.SysFont(None, 80)

    # Menu button setup
    btn_story = pygame.Rect(width//2 - 300, height//2 - 100, 250, 100)
    btn_vypravy = pygame.Rect(width//2 + 50, height//2 - 100, 250, 100)

    # Path points for vypravy
    num_paths = random.randint(3, 5)  
    end_point = (width - 300, height // 2)
    start_points, end_point, paths = generate_paths_no_overlap(
        num_paths=num_paths,
        screen_width=width,
        screen_height=height,
        y_barrier=100,
        x_start=300,
        x_end_offset=200,
        min_dist=60,
        min_path_dist=120,
        min_count=6,      # zde změna
        max_count=8,      # zde změna
        box_size=48,
        max_offset=40,
        end_point=end_point   # <-- zde předáš pevný bod
    )
    tile_types_list = [generate_tile_types(len(path)) for path in paths]

    state = "menu"  # "menu" or "vypravy"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
                mx, my = event.pos
                if btn_story.collidepoint(mx, my):
                    state = "story"  # Zatím nic nedělá
                elif btn_vypravy.collidepoint(mx, my):
                    state = "vypravy"
                    print("Přepnuto na výpravy")

        if state == "menu":
            screen.fill((60, 60, 80))
            pygame.draw.rect(screen, (180, 180, 200), btn_story)
            pygame.draw.rect(screen, (200, 200, 80), btn_vypravy)
            screen.blit(font.render("Příběh", True, (30, 30, 30)), (btn_story.x + 30, btn_story.y + 25))
            screen.blit(font.render("Výpravy", True, (30, 30, 30)), (btn_vypravy.x + 30, btn_vypravy.y + 25))
        elif state == "vypravy":
            screen.fill((40, 70, 40))  # nové pozadí pro výpravy
            for path_points, tile_types in zip(paths, tile_types_list):
                # Pro každou cestu:
                draw_path(screen, path_points, tile_types, box_size=40, start_point=path_points[0], end_point=end_point)


        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()