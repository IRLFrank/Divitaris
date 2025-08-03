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
    width = 1980  # šířka okna
    height = 1080  # výška okna
    title = "Divitaris Game"  # titulek okna

    pygame.init()  # inicializace pygame
    screen = pygame.display.set_mode((width, height))  # vytvoření okna
    pygame.display.set_caption(title)  # nastavení titulku okna
    font = pygame.font.SysFont(None, 80)  # font pro texty

    # Rozměry tlačítek v rohu
    button_width = 250  # šířka tlačítek v rohu
    button_height = 100  # výška tlačítek v rohu
    button_margin = 30  # mezera mezi tlačítky a okrajem

    # Pravý dolní roh - tlačítko Výpravy
    btn_vypravy = pygame.Rect(
        width - button_width - button_margin,
        height - button_height - button_margin,
        button_width, button_height
    )

    # PLAY tlačítko doprostřed
    play_width = 400  # šířka play tlačítka
    play_height = 140  # výška play tlačítka
    btn_play = pygame.Rect(
        (width - play_width) // 2,
        (height - play_height) // 2,
        play_width, play_height
    )

    # Generování cest pro výpravy
    num_paths = random.randint(3, 5)  # Počet cest (náhodně 3-5)
    end_point = (width - 300, height // 2)  # Koncový bod cest
    box_size = 64  # Velikost kostičky
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

    # Načtení textur pro mapu
    MAPA_TEMP_PATH = os.path.join("Textury", "Mapa", "mapa_temp.png")  # cesta k obrázku pozadí mapy
    MAPA_TEMP_IMG = pygame.image.load(MAPA_TEMP_PATH).convert()  # načtení obrázku pozadí mapy
    MAPA_TEMP_IMG = pygame.transform.scale(MAPA_TEMP_IMG, (width, height))  # roztáhnutí pozadí na celou obrazovku

    # Načtení textur pro jednotlivé typy kostiček
    MAPA_BOJ_IMG = pygame.image.load(os.path.join("Textury", "Mapa", "mapa_boj.png")).convert_alpha()  # textura boj
    MAPA_SHOP_IMG = pygame.image.load(os.path.join("Textury", "Mapa", "mapa_shop.png")).convert_alpha()  # textura obchod
    MAPA_EVENT_IMG = pygame.image.load(os.path.join("Textury", "Mapa", "mapa_event.png")).convert_alpha()  # textura event
    MAPA_ELITE_IMG = pygame.image.load(os.path.join("Textury", "Mapa", "mapa_elite.png")).convert_alpha()  # textura elite
    MAPA_BOSS_IMG = pygame.image.load(os.path.join("Textury", "Mapa", "mapa_boss.png")).convert_alpha()  # textura boss

    state = "menu"  # výchozí stav hry
    running = True  # hlavní smyčka

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # zavření okna
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # stisknutí ESC
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and state == "menu":  # kliknutí v menu
                mx, my = event.pos
                if btn_vypravy.collidepoint(mx, my):  # klik na Výpravy
                    state = "vypravy"
                    print("Přepnuto na výpravy")
                elif btn_play.collidepoint(mx, my):  # klik na PLAY
                    state = "play"  # nový stav pro play
                    print("Play pressed")

        if state == "menu":
            screen.fill((60, 60, 80))  # pozadí menu
            # Tlačítko Výpravy v rohu
            pygame.draw.rect(screen, (200, 200, 80), btn_vypravy, border_radius=20)  # vykresli Výpravy
            screen.blit(font.render("Výpravy", True, (30, 30, 30)), (btn_vypravy.x + 30, btn_vypravy.y + 25))  # text Výpravy
            # PLAY tlačítko doprostřed
            pygame.draw.rect(screen, (80, 200, 120), btn_play, border_radius=30)  # vykresli PLAY
            play_text = font.render("PLAY", True, (30, 30, 30))  # text PLAY
            screen.blit(
                play_text,
                (btn_play.x + (play_width - play_text.get_width()) // 2,
                 btn_play.y + (play_height - play_text.get_height()) // 2)
            )
        elif state == "vypravy":
            screen.blit(MAPA_TEMP_IMG, (0, 0))  # vykresli pozadí mapy

            # Reset all boss tiles first
            for tile_types in tile_types_list:
                for i in range(len(tile_types)):
                    if tile_types[i] == 4:
                        tile_types[i] = 0

            # Najdi nejdelší cestu
            max_length = 0
            boss_path_idx = -1
            
            # Zjisti index nejdelší cesty
            for idx, path in enumerate(paths):
                path_length = len(path)
                if path_length > max_length:
                    max_length = path_length
                    boss_path_idx = idx

            # Nastav boss na poslední kostičku nejdelší cesty
            if boss_path_idx >= 0:
                path = paths[boss_path_idx]
                last_tile_idx = len(path) - 1
                tile_types_list[boss_path_idx][last_tile_idx] = 4
                print(f"Boss set on path {boss_path_idx}, tile {last_tile_idx + 1} of {len(path)}")

            # Vykreslení všech cest
            for path_points, tile_types in zip(paths, tile_types_list):
                draw_path(
                    screen, path_points, tile_types,
                    box_size=box_size,
                    start_point=path_points[0],
                    end_point=end_point,
                    mapa_boj_img=MAPA_BOJ_IMG,
                    mapa_shop_img=MAPA_SHOP_IMG,
                    mapa_event_img=MAPA_EVENT_IMG,
                    mapa_elite_img=MAPA_ELITE_IMG,
                    mapa_boss_img=MAPA_BOSS_IMG
                )
        elif state == "play":
            screen.fill((20, 20, 40))  # pozadí pro play stav
            play_mode_text = font.render("PLAY MODE", True, (255, 255, 255))
            screen.blit(
                play_mode_text,
                ((width - play_mode_text.get_width()) // 2,
                 (height - play_mode_text.get_height()) // 2)
            )

        pygame.display.flip()  # aktualizace obrazovky
        pygame.time.Clock().tick(60)  # omezení FPS

    pygame.quit()  # ukončení pygame

if __name__ == "__main__":
    main()