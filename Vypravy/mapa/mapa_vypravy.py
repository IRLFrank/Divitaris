import pygame
import random
import math

def generate_tile_types(num_tiles):
    """
    Vygeneruje typy kostiček podle pravděpodobností.
    0 = základní (50%), 1 = speciální (30%), 2 = vzácná (10%), 3 = zbytek (10%)
    """
    types = []
    for _ in range(num_tiles):
        r = random.random()
        if r < 0.5:
            types.append(0)
        elif r < 0.8:
            types.append(1)
        elif r < 0.9:
            types.append(2)
        else:
            types.append(3)
    return types

def generate_path_points(
    start_x=240, start_y=600, box_size=50, count=18, step_x=90, step_y_range=(-30, 30), min_dist=50,
    screen_height=1080, y_barrier=100
):
    """
    Vygeneruje body cesty pro zadaný počet kostiček.
    Každý další bod je posunutý doprava a náhodně nahoru/dolů.
    Žádné dvě kostičky nejsou blíž než min_dist pixelů.
    Kostičky se neobjeví blíž než y_barrier od horního/dolního okraje.
    """
    points = []
    x, y = start_x, start_y
    min_y = y_barrier
    max_y = screen_height - y_barrier - box_size
    for _ in range(count):
        found = False
        for _ in range(100):  # max 100 pokusů, pak to vzdá
            new_x = x
            new_y = y + random.randint(*step_y_range)
            # Omez Y na bariéry
            new_y = max(min_y, min(max_y, new_y))
            too_close = False
            for px, py in points:
                if math.hypot(new_x - px, new_y - py) < min_dist:
                    too_close = True
                    break
            if not too_close:
                found = True
                break
        if not found:
            new_x, new_y = x, y
        points.append((new_x, new_y))
        x += step_x
        y = new_y
    return points

def generate_multiple_paths(
    num_paths=3,
    start_x=240,
    start_y=600,
    box_size=50,
    min_count=12,
    max_count=22,
    step_x=90,
    step_y_range=(-30, 30),
    y_offset=100,
    x_offset_range=(-30, 30),
    min_dist=150,
    min_path_dist=100,  # minimální vzdálenost mezi začátky cest
    screen_height=1080,
    y_barrier=100
):
    """
    Vygeneruje více cest (každá je list bodů).
    Žádné dvě kostičky (ani mezi cestami) nejsou blíž než min_dist.
    Začátky cest jsou od sebe alespoň min_path_dist.
    """
    all_paths = []
    all_points = []
    start_points = []
    for i in range(min(num_paths, 10)):
        count = random.randint(min_count, max_count)
        # Najdi vhodný start pro cestu, který není blíž než min_path_dist k ostatním startům
        for _ in range(100):
            x_off = random.randint(*x_offset_range)
            y_off = random.randint(-y_offset//2, y_offset//2)
            start = (start_x + x_off, start_y + i * y_offset + y_off)
            too_close = False
            for sx, sy in start_points:
                if math.hypot(start[0] - sx, start[1] - sy) < min_path_dist:
                    too_close = True
                    break
            if not too_close:
                break
        start_points.append(start)
        x, y = start
        min_y = y_barrier
        max_y = screen_height - y_barrier - box_size
        path = []
        for _ in range(count):
            found = False
            for _ in range(100):
                new_x = x
                new_y = y + random.randint(*step_y_range)
                new_y = max(min_y, min(max_y, new_y))
                too_close = False
                for px, py in all_points:
                    if math.hypot(new_x - px, new_y - py) < min_dist:
                        too_close = True
                        break
                if not too_close:
                    found = True
                    break
            if not found:
                new_x, new_y = x, y
            path.append((new_x, new_y))
            all_points.append((new_x, new_y))
            x += step_x
            y = new_y
        all_paths.append(path)
    return all_paths

def generate_start_points(num_points, screen_height, y_barrier=100, x=300, min_dist=120):
    """
    Vygeneruje startovní body dál od levého okraje (x=300 místo x=200).
    """
    points = []
    attempts = 0
    while len(points) < num_points and attempts < 1000:
        y = random.randint(y_barrier, screen_height - y_barrier)
        if all(abs(y - py) >= min_dist for _, py in points):
            points.append((x, y))
        attempts += 1
    return points

def generate_end_point(screen_width, screen_height, y_barrier=100):
    x = screen_width - 300
    y = random.randint(y_barrier, screen_height - y_barrier)
    return (x, y)

def generate_path_between(start, end, num_tiles=15, max_offset=40):
    points = []
    for i in range(num_tiles):
        t = i / (num_tiles - 1)
        x = int(start[0] + t * (end[0] - start[0]))
        y = int(start[1] + t * (end[1] - start[1]))
        # Přidej náhodnou odchylku pro "klikatost", kromě startu a cíle
        if 0 < i < num_tiles - 1:
            y += random.randint(-max_offset, max_offset)
        points.append((x, y))
    return points

def draw_path(screen, path_points, tile_types=None, box_size=40, start_point=None, end_point=None):
    colors = {
        0: (200, 200, 50),
        1: (80, 180, 250),
        2: (220, 80, 80),
        3: (180, 80, 220)
    }
    if tile_types is None:
        tile_types = [0] * len(path_points)
    font = pygame.font.SysFont(None, int(box_size * 0.7))  # velikost fontu podle box_size
    for i, (x, y) in enumerate(path_points):
        t = tile_types[i]
        color = colors.get(t, (200, 200, 50))
        rect = pygame.Rect(x, y, box_size, box_size)
        pygame.draw.rect(screen, color, rect)
        # Vykresli číslo kostičky doprostřed
        text = font.render(str(i + 1), True, (30, 30, 30))
        text_rect = text.get_rect(center=(x + box_size // 2, y + box_size // 2))
        screen.blit(text, text_rect)

    # Zvýraznění start pointu (první bod cesty)
    if start_point:
        sx, sy = start_point
        pygame.draw.ellipse(
            screen, (0, 255, 0),
            (sx - box_size//4, sy - box_size//4, box_size + box_size//2, box_size + box_size//2), 4
        )

    # Zvýraznění end pointu (poslední bod cesty)
    if end_point:
        ex, ey = end_point
        pygame.draw.ellipse(
            screen, (255, 0, 0),
            (ex - box_size//4, ey - box_size//4, box_size + box_size//2, box_size + box_size//2), 4
        )

def generate_paths_no_overlap(
    num_paths=3,
    screen_width=1980,
    screen_height=1080,
    y_barrier=100,
    x_start=300,
    x_end_offset=200,
    min_dist=60,
    min_path_dist=120,
    min_count=8,
    max_count=10,
    box_size=40,
    max_offset=40,
    end_point=None
):
    # 1. Vygeneruj start pointy
    start_points = []
    attempts = 0
    while len(start_points) < num_paths and attempts < 1000:
        y = random.randint(y_barrier, screen_height - y_barrier - box_size)
        if all(abs(y - py) >= min_path_dist for _, py in start_points):
            x = max(0, min(x_start, screen_width - box_size))
            start_points.append((x, y))
        attempts += 1

    # 2. Vygeneruj end point pouze pokud není zadaný
    if end_point is None:
        end_point = (screen_width - x_end_offset, random.randint(y_barrier, screen_height - y_barrier))

    # 3. Vygeneruj X souřadnice pro všechny pozice v cestě
    max_tiles = random.randint(min_count, max_count)
    x_positions = []
    for i in range(max_tiles):
        t = i / (max_tiles - 1)
        x = int(start_points[0][0] + t * (end_point[0] - start_points[0][0]))
        x_positions.append(x)

    # 4. Generuj cesty a kontroluj překrývání
    all_points = []
    paths = []
    for start in start_points:
        num_tiles = max_tiles  # všechny cesty budou mít stejný počet kostiček (můžeš upravit na různé délky)
        path = []
        for i in range(num_tiles):
            x = x_positions[i] + random.randint(-10, 10)  # malá odchylka
            t = i / (num_tiles - 1)
            y = int(start[1] + t * (end_point[1] - start[1]))
            if 0 < i < num_tiles - 1:
                y += random.randint(-max_offset, max_offset)
            found = False
            for _ in range(200):
                too_close = False
                for px, py in all_points:
                    if math.hypot(x - px, y - py) < min_dist:
                        too_close = True
                        break
                if not too_close:
                    found = True
                    break
                y = int(start[1] + t * (end_point[1] - start[1]))
                if 0 < i < num_tiles - 1:
                    y += random.randint(-max_offset, max_offset)
            if found:
                path.append((x, y))
                all_points.append((x, y))
        paths.append(path)
    return start_points, end_point, paths