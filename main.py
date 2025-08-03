import pygame
import random
import os
import json
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

def save_game(save_file, data):
    """
    Uloží herní data do zvoleného save souboru
    """
    save_path = os.path.join(saves_dir, save_file)
    with open(save_path, "w") as f:
        json.dump(data, f)

def create_empty_save():
    """Creates empty save data structure"""
    return {
        "game_state": "new",
        "paths": [],
        "tile_types": [],
        "score": 0
    }

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

    # Save file selection buttons
    save_button_width = 300
    save_button_height = 100
    save_button_margin = 50
    save_buttons = []

    for i in range(3):
        btn = pygame.Rect(
            (width - save_button_width) // 2,
            height//2 - save_button_height*1.5 + i*(save_button_height + save_button_margin),
            save_button_width,
            save_button_height
        )
        save_buttons.append(btn)

    # Mode selection buttons
    mode_button_width = 300
    mode_button_height = 100
    mode_button_margin = 50

    btn_story = pygame.Rect(
        (width//2 - mode_button_width) - mode_button_margin,
        height//2 - mode_button_height//2,
        mode_button_width,
        mode_button_height
    )

    btn_vypravy = pygame.Rect(
        (width//2) + mode_button_margin,
        height//2 - mode_button_height//2,
        mode_button_width,
        mode_button_height
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

    # Create Saves directory if it doesn't exist
    saves_dir = os.path.join(os.path.dirname(__file__), "Saves")
    os.makedirs(saves_dir, exist_ok=True)

    # Create empty save files if they don't exist
    for i in range(1, 4):
        save_path = os.path.join(saves_dir, f"save{i}.json")
        if not os.path.exists(save_path):
            with open(save_path, "w") as f:
                json.dump(create_empty_save(), f)

    state = "menu"  # výchozí stav hry
    running = True  # hlavní smyčka
    current_save = None  # Will store which save file is selected

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == "save_select":
                    state = "menu"  # Návrat do menu
                elif state == "vypravy":
                    state = "save_select"  # Návrat na výběr save file
                elif state == "mode_select":
                    state = "save_select"  # Návrat na výběr save file
                else:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if state == "menu":
                    if btn_play.collidepoint(mx, my):
                        state = "save_select"
                        print("Select save file")
                elif state == "save_select":
                    for i, btn in enumerate(save_buttons):
                        if btn.collidepoint(mx, my):
                            current_save = f"save{i+1}.json"
                            state = "mode_select"  # Change to mode selection instead of výpravy
                            print(f"Selected {current_save}")
                elif state == "mode_select":
                    if btn_story.collidepoint(mx, my):
                        state = "story"
                        print("Story mode selected")
                    elif btn_vypravy.collidepoint(mx, my):
                        state = "vypravy"
                        print("Výpravy mode selected")

        # Vykreslování podle stavu
        if state == "menu":
            screen.fill((60, 60, 80))
            # Pouze PLAY tlačítko
            pygame.draw.rect(screen, (80, 200, 120), btn_play, border_radius=30)
            play_text = font.render("PLAY", True, (30, 30, 30))
            screen.blit(
                play_text,
                (btn_play.x + (play_width - play_text.get_width()) // 2,
                 btn_play.y + (play_height - play_text.get_height()) // 2)
            )

        elif state == "save_select":
            screen.fill((40, 40, 60))
            # Pouze save tlačítka
            for i, btn in enumerate(save_buttons):
                save_path = os.path.join(saves_dir, f"save{i+1}.json")
                try:
                    with open(save_path, "r") as f:
                        save_data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    # If file is corrupted or missing, create new empty save
                    save_data = create_empty_save()
                    with open(save_path, "w") as f:
                        json.dump(save_data, f)
                
                # Save file is empty if it only has default values
                is_empty = save_data.get("game_state") == "new"
                color = (100, 180, 100) if not is_empty else (180, 180, 180)
                
                pygame.draw.rect(screen, color, btn, border_radius=20)
                text = font.render(f"Save {i+1}", True, (30, 30, 30))
                screen.blit(
                    text,
                    (btn.x + (save_button_width - text.get_width()) // 2,
                     btn.y + (save_button_height - text.get_height()) // 2)
                )

        elif state == "mode_select":
            screen.fill((40, 40, 60))
            # Draw mode selection buttons
            pygame.draw.rect(screen, (180, 180, 200), btn_story, border_radius=20)
            pygame.draw.rect(screen, (200, 200, 80), btn_vypravy, border_radius=20)
            
            # Draw button texts
            story_text = font.render("Příběh", True, (30, 30, 30))
            vypravy_text = font.render("Výpravy", True, (30, 30, 30))
            
            screen.blit(story_text, 
                (btn_story.x + (mode_button_width - story_text.get_width()) // 2,
                 btn_story.y + (mode_button_height - story_text.get_height()) // 2))
            
            screen.blit(vypravy_text,
                (btn_vypravy.x + (mode_button_width - vypravy_text.get_width()) // 2,
                 btn_vypravy.y + (mode_button_height - vypravy_text.get_height()) // 2))

        elif state == "vypravy":
            # Vykreslení výprav zůstává stejné
            screen.blit(MAPA_TEMP_IMG, (0, 0))

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
        elif state == "load_game" and current_save is not None:
            # Načtení hry ze souboru
            save_path = os.path.join(saves_dir, f"save{current_save}.json")
            if os.path.exists(save_path):
                with open(save_path, "r") as f:
                    save_data = json.load(f)
                    # Zpracování načtených dat (předpokládá se, že obsahují potřebné informace o hře)
                    # Např. obnovit pozice jednotek, stav hry atd.
                    print(f"Game loaded from {save_path}")
                    # Přepni stav zpět na hru nebo na jiný vhodný stav
                    state = "play"
            else:
                print(f"Save file {save_path} not found")

        elif state == "story":
            screen.fill((40, 60, 40))
            story_text = font.render("Story Mode - Coming Soon", True, (255, 255, 255))
            screen.blit(story_text,
                ((width - story_text.get_width()) // 2,
                 (height - story_text.get_height()) // 2))

        pygame.display.flip()  # aktualizace obrazovky
        pygame.time.Clock().tick(60)  # omezení FPS

    pygame.quit()  # ukončení pygame

if __name__ == "__main__":
    main()