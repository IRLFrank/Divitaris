import pygame
import random
import os
from Animace.animace_setup import setup_animations
from Vypravy.mapa.mapa_vypravy import (
    generate_start_points, generate_end_point, generate_path_between,
    generate_paths_no_overlap, generate_tile_types, draw_path
)

def pil_to_pygame(image):
    # Pomocná funkce pro převod PIL obrázku na pygame Surface
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

def main():
    width = 1980
    height = 1080
    title = "Divitaris Game"

    pygame.init()  # Inicializace pygame
    screen = pygame.display.set_mode((width, height))  # Vytvoření okna
    pygame.display.set_caption(title)  # Nastavení titulku okna
    font = pygame.font.SysFont(None, 80)  # Font pro texty

    # Nastavení tlačítek v menu
    btn_story = pygame.Rect(width//2 - 300, height//2 - 100, 250, 100)
    btn_vypravy = pygame.Rect(width//2 + 50, height//2 - 100, 250, 100)

    # Generování cest pro výpravy
    num_paths = random.randint(3, 5)  # Počet cest (náhodně 3-5)
    end_point = (width - 300, height // 2)  # Koncový bod cest
    box_size = 54  # Velikost kostičky
    start_points, end_point, paths = generate_paths_no_overlap(
        num_paths=num_paths,
        screen_width=width,
        screen_height=height,
        y_barrier=100,
        x_start=300,
        x_end_offset=200,
        min_dist=60,
        min_path_dist=120,
        min_count=6,      # minimální počet kostiček v cestě
        max_count=8,      # maximální počet kostiček v cestě
        box_size=box_size,
        max_offset=40,
        end_point=end_point   # pevně daný koncový bod
    )
    tile_types_list = [generate_tile_types(len(path)) for path in paths]  # Typy kostiček pro každou cestu

    # Načtení obrázků pro různé typy kostiček
    MAPA_BOJ_PATH = os.path.join("Textury", "Mapa", "mapa_boj.png")
    MAPA_BOJ_IMG = pygame.image.load(MAPA_BOJ_PATH).convert_alpha()
    MAPA_ELITE_PATH = os.path.join("Textury", "Mapa", "mapa_elite.png")
    MAPA_ELITE_IMG = pygame.image.load(MAPA_ELITE_PATH).convert_alpha()
    MAPA_BOSS_PATH = os.path.join("Textury", "Mapa", "mapa_boss.png")
    MAPA_BOSS_IMG = pygame.image.load(MAPA_BOSS_PATH).convert_alpha()

    state = "menu"  # Stav hry ("menu" nebo "vypravy")
    running = True

    while running:
        # Zpracování událostí (klávesnice, myš, zavření okna)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":
                mx, my = event.pos
                if btn_story.collidepoint(mx, my):
                    state = "story"  # Přepnutí na příběh (zatím neimplementováno)
                elif btn_vypravy.collidepoint(mx, my):
                    state = "vypravy"
                    print("Přepnuto na výpravy")

        # Vykreslení menu
        if state == "menu":
            screen.fill((60, 60, 80))  # Barva pozadí menu
            pygame.draw.rect(screen, (180, 180, 200), btn_story)
            pygame.draw.rect(screen, (200, 200, 80), btn_vypravy)
            screen.blit(font.render("Příběh", True, (30, 30, 30)), (btn_story.x + 30, btn_story.y + 25))
            screen.blit(font.render("Výpravy", True, (30, 30, 30)), (btn_vypravy.x + 30, btn_vypravy.y + 25))
        # Vykreslení výprav
        elif state == "vypravy":
            screen.fill((40, 70, 40))  # Barva pozadí pro výpravy

            # Zruš všechny staré bossy (typ 4)
            for tile_types in tile_types_list:
                for i in range(len(tile_types)):
                    if tile_types[i] == 4:
                        tile_types[i] = 0

            # Najdi cestu a index kostičky nejblíže end_point
            min_dist = float('inf')
            boss_path_idx = -1
            boss_tile_idx = -1

            for path_idx, path in enumerate(paths):
                for tile_idx, (x, y) in enumerate(path):
                    dist = ((x - end_point[0]) ** 2 + (y - end_point[1]) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        boss_path_idx = path_idx
                        boss_tile_idx = tile_idx

            # Bezpečně nastav boss typ jen pokud index existuje
            if (
                boss_path_idx != -1 and
                boss_tile_idx != -1 and
                boss_path_idx < len(tile_types_list) and
                boss_tile_idx < len(tile_types_list[boss_path_idx])
            ):
                # Nastav typ 4 (boss) pouze této kostičce
                tile_types_list[boss_path_idx][boss_tile_idx] = 4
            else:
                print("Boss kostička nebyla nalezena nebo index mimo rozsah!")

            # Najdi všechny cesty s maximální délkou
            max_len = max(len(path) for path in paths)
            max_paths = [i for i, path in enumerate(paths) if len(path) == max_len]

            # Nastav boss na poslední kostičku v POSLEDNÍ cestě s max délkou
            if max_paths:
                last_idx = max_paths[-1]
                tile_types_list[last_idx][-1] = 4

            # Vykreslení všech cest
            for path_points, tile_types in zip(paths, tile_types_list):
                # Pro každou cestu vykresli kostičky
                draw_path(
                    screen, path_points, tile_types,
                    box_size=box_size,
                    start_point=path_points[0],
                    end_point=end_point,
                    mapa_boj_img=MAPA_BOJ_IMG,
                    mapa_elite_img=MAPA_ELITE_IMG,
                    mapa_boss_img=MAPA_BOSS_IMG
                )

        pygame.display.flip()  # Aktualizace obrazovky
        pygame.time.Clock().tick(60)  # Omezení FPS na 60

    pygame.quit()  # Ukončení pygame

if __name__ == "__main__":
    main()