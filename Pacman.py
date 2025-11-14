import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((900,700))
pygame.display.set_caption("Pacman")

# *** VOLLBILD-MODUS VARIABLEN ***
fullscreen = False
original_screen_size = (900, 700)
current_screen_size = (900, 700)


Black = (0,0,0)
Yellow = (255,255,0)
Blue = (0,0,255)
White = (255,255,255)
Red = (255,0,0)
Pink = (255,192,203)
Orange = (255,165,0)
Cyan = (0,255,255)
Gray = (128,128,128)
Green = (0,255,0)

Maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,4,3,3,3,3,3,3,3,1,3,3,3,3,3,3,4,1],
    [1,3,1,1,3,1,1,1,3,1,3,1,1,1,3,1,3,1],
    [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
    [1,3,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1],
    [1,3,3,3,3,3,1,3,3,3,3,3,1,3,3,3,3,1],
    [1,1,1,1,1,3,1,1,2,2,2,1,1,3,1,1,1,1],
    [1,3,3,3,3,3,3,3,2,2,2,3,3,3,3,3,3,1],
    [1,3,1,1,3,1,3,1,2,2,2,1,3,1,3,1,1,1],
    [1,3,3,3,3,1,3,3,3,1,3,3,3,1,3,3,3,1],
    [1,1,1,1,3,1,1,1,3,1,3,1,1,1,3,1,3,1],
    [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,3,1],
    [1,3,1,1,1,1,3,1,1,3,1,1,3,1,1,1,3,1],
    [1,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
TILE_SIZE = 50

clock = pygame.time.Clock()

def generate_random_maze():
    """Generiert ein zufälliges Maze-Layout ähnlich den ersten beiden Leveln"""
    width = 18
    height = 15
    
    # Basis-Template: Äußere Wände
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Innere Bereiche erstmal frei machen (mit Punkten füllen)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            maze[y][x] = 3  # Direkt mit Punkten füllen
    
    # Ghost-Box in der Mitte hinzufügen
    center_x = width // 2
    center_y = height // 2
    
    # Ghost-Box (3x3) mit dünnen Wänden drumherum
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if 0 <= center_y + dy < height and 0 <= center_x + dx < width:
                maze[center_y + dy][center_x + dx] = 2
    
    # Dünne Wände um die Ghost-Box (Typ 5 = Geister-Wand)
    # Oben und unten
    for dx in range(-2, 3):
        if 0 <= center_x + dx < width:
            if 0 <= center_y - 2 < height:
                maze[center_y - 2][center_x + dx] = 5
            if 0 <= center_y + 2 < height:
                maze[center_y + 2][center_x + dx] = 5
    
    # Links und rechts
    for dy in range(-1, 2):
        if 0 <= center_y + dy < height:
            if 0 <= center_x - 2 < width:
                maze[center_y + dy][center_x - 2] = 5
            if 0 <= center_x + 2 < width:
                maze[center_y + dy][center_x + 2] = 5
    
    # Strukturierte Wandplatzierung ähnlich den ersten beiden Leveln
    # 1. Vertikale Säulen in regelmäßigen Abständen
    for x in [3, 6, 11, 14]:  # Ähnliche Positionen wie in Level 1&2
        for y in range(2, height - 2):
            # Nicht in Ghost-Box-Bereich
            if abs(x - center_x) <= 3 and abs(y - center_y) <= 3:
                continue
            
            # Zufällige Unterbrechungen für Gänge (60% Chance für Wand)
            if random.random() < 0.6:
                maze[y][x] = 1
    
    # 2. Horizontale Balken
    for y in [3, 5, 9, 11]:  # Ähnliche Positionen
        for x in range(3, width - 3):
            # Nicht in Ghost-Box-Bereich oder bei vertikalen Säulen
            if (abs(x - center_x) <= 3 and abs(y - center_y) <= 3) or x in [3, 6, 11, 14]:
                continue
            
            # 50% Chance für horizontale Wand-Segmente
            if random.random() < 0.5:
                maze[y][x] = 1
    
    # 3. Kleine Wand-Cluster für zusätzliche Komplexität
    num_clusters = random.randint(4, 7)
    for _ in range(num_clusters):
        cluster_x = random.randint(2, width - 3)
        cluster_y = random.randint(2, height - 3)
        cluster_size = random.randint(1, 3)  # Kleine Cluster
        
        # Nicht in Ghost-Box oder zu nah an den Ecken
        if (abs(cluster_x - center_x) <= 4 and abs(cluster_y - center_y) <= 4) or \
           cluster_x < 3 or cluster_x > width - 4 or cluster_y < 3 or cluster_y > height - 4:
            continue
        
        # Kleinen Wand-Cluster platzieren
        for dy in range(cluster_size):
            for dx in range(cluster_size):
                new_x = cluster_x + dx
                new_y = cluster_y + dy
                if (2 <= new_x < width - 2 and 2 <= new_y < height - 2 and 
                    maze[new_y][new_x] == 3):  # Nur auf Punkt-Tiles
                    maze[new_y][new_x] = 1
    
    # 4. Öffnungen in Wänden für bessere Begehbarkeit schaffen
    # Zufällige Löcher in zu lange Wand-Segmente
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            if maze[y][x] == 1:
                # Prüfe ob diese Wand von langen Wand-Segmenten umgeben ist
                surrounding_walls = 0
                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    if (0 <= x+dx < width and 0 <= y+dy < height and 
                        maze[y+dy][x+dx] == 1):
                        surrounding_walls += 1
                
                # Wenn zu viele Wände drumherum, manchmal eine Öffnung schaffen
                if surrounding_walls >= 3 and random.random() < 0.3:
                    maze[y][x] = 3  # Wand zu Punkt machen
    
    # Power-Ups in den Ecken platzieren (wie in den ersten Leveln)
    power_up_positions = [
        (1, 1),  # Oben links
        (width - 2, 1),  # Oben rechts  
        (1, height - 2),  # Unten links
        (width - 2, height - 2)  # Unten rechts
    ]
    
    for x, y in power_up_positions:
        if maze[y][x] == 3:  # Nur wenn es ein normaler Punkt ist
            maze[y][x] = 4  # Power-Up
    
    return maze

def generate_new_level():
    """Generiert ein neues Level-Layout basierend auf der Level-Nummer"""
    global Maze, level
    
    if level <= 2:
        # Erste 2 Level sind vordefiniert für sanften Einstieg
        level_layouts = [
            # Level 1 (Original - einfacher Start)
            [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,4,3,3,3,3,3,3,3,1,3,3,3,3,3,3,4,1],
                [1,3,1,1,3,1,1,1,3,1,3,1,1,1,3,1,3,1],
                [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
                [1,3,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1],
                [1,3,3,3,3,3,1,3,3,3,3,3,1,3,3,3,3,1],
                [1,1,1,1,1,3,1,1,2,2,2,1,1,3,1,1,1,1],
                [1,3,3,3,3,3,3,3,2,2,2,3,3,3,3,3,3,1],
                [1,3,1,1,3,1,3,1,2,2,2,1,3,1,3,1,1,1],
                [1,3,3,3,3,1,3,3,3,1,3,3,3,1,3,3,3,1],
                [1,1,1,1,3,1,1,1,3,1,3,1,1,1,3,1,3,1],
                [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,3,1],
                [1,3,1,1,1,1,3,1,1,3,1,1,3,1,1,1,3,1],
                [1,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ],
            # Level 2 - Anderes vordefiniertes Layout
            [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,1],
                [1,3,1,1,1,3,1,1,1,1,1,1,3,1,1,1,3,1],
                [1,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,1],
                [1,3,1,3,1,1,3,1,3,1,3,1,3,1,1,3,1,1],
                [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
                [1,1,1,3,1,1,1,1,2,2,2,1,1,1,1,3,1,1],
                [1,3,3,3,3,3,3,3,2,2,2,3,3,3,3,3,3,1],
                [1,3,1,3,1,1,1,1,2,2,2,1,1,1,1,3,1,1],
                [1,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,1],
                [1,3,1,3,1,1,3,1,3,1,3,1,3,1,1,3,1,1],
                [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
                [1,3,1,1,1,3,1,1,1,1,1,1,3,1,1,1,3,1],
                [1,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ]
        ]
        
        layout_index = (level - 1) % len(level_layouts)
        Maze = [row[:] for row in level_layouts[layout_index]]  # Deep copy
    else:
        # Ab Level 3: Zufällig generierte Level
        print(f"Generiere zufälliges Level {level}...")
        Maze = generate_random_maze()
        print(f"Zufälliges Level {level} erstellt!")

def get_random_spawn_position():
    """Finde eine zufällige freie Position für Pacman"""
    free_positions = []
    
    # Sammle alle freien Positionen (nicht Wand, nicht Ghost-Box)
    for y in range(len(Maze)):
        for x in range(len(Maze[0])):
            tile_value = Maze[y][x]
            # Freie Bereiche: 0=leer, 3=Punkte, 4=Power-Ups (nicht 1=Wand, nicht 2=Ghost-Box)
            if tile_value in [0, 3, 4]:
                # Konvertiere zu Pixel-Position (Tile-Mitte)
                pixel_x = x * TILE_SIZE + TILE_SIZE // 2
                pixel_y = y * TILE_SIZE + TILE_SIZE // 2
                free_positions.append((pixel_x, pixel_y))
    
    # Wähle zufällige Position aus den freien Positionen
    if free_positions:
        return random.choice(free_positions)
    else:
        # Fallback: Standard-Position falls keine freien Plätze gefunden
        return (75, 75)

def toggle_fullscreen():
    """Wechselt zwischen Vollbild und Fenster-Modus"""
    global screen, fullscreen, current_screen_size
    
    if fullscreen:
        # Zurück zum Fenster-Modus
        screen = pygame.display.set_mode(original_screen_size)
        fullscreen = False
        current_screen_size = original_screen_size
        print("Fenster-Modus aktiviert")
    else:
        # Zu Vollbild-Modus wechseln
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        fullscreen = True
        current_screen_size = screen.get_size()
        print(f"Vollbild-Modus aktiviert: {current_screen_size}")

def get_scale_factors():
    """Berechnet Skalierungsfaktoren für verschiedene Bildschirmgrößen"""
    if fullscreen:
        scale_x = current_screen_size[0] / original_screen_size[0]
        scale_y = current_screen_size[1] / original_screen_size[1]
        # Verwende den kleineren Faktor für gleichmäßige Skalierung
        scale = min(scale_x, scale_y)
        return scale, scale
    return 1.0, 1.0

def scale_position(x, y):
    """Skaliert eine Position für den aktuellen Bildschirm"""
    scale_x, scale_y = get_scale_factors()
    if fullscreen:
        # Zentriere das Spiel auf dem Bildschirm
        offset_x = (current_screen_size[0] - (original_screen_size[0] * scale_x)) // 2
        offset_y = (current_screen_size[1] - (original_screen_size[1] * scale_y)) // 2
        return int(x * scale_x + offset_x), int(y * scale_y + offset_y)
    return x, y

def scale_size(width, height=None):
    """Skaliert eine Größe für den aktuellen Bildschirm"""
    if height is None:
        height = width
    scale_x, scale_y = get_scale_factors()
    return int(width * scale_x), int(height * scale_y)

def draw_walls(screen, scale_x, scale_y):
    """Zeichnet Wände als komplett zusammenhängende Fläche ohne Blockgrenzen"""
    # Erstelle ein Bitmap für normale Wände
    wall_bitmap = []
    for row_idx in range(len(Maze)):
        wall_row = []
        for col_idx in range(len(Maze[0])):
            wall_row.append(Maze[row_idx][col_idx] == 1)
        wall_bitmap.append(wall_row)
    
    # Zeichne horizontale Streifen für zusammenhängende normale Wände
    for row_idx in range(len(wall_bitmap)):
        col_idx = 0
        while col_idx < len(wall_bitmap[0]):
            if wall_bitmap[row_idx][col_idx]:
                # Finde Ende des horizontalen Wandstreifens
                start_col = col_idx
                while col_idx < len(wall_bitmap[0]) and wall_bitmap[row_idx][col_idx]:
                    col_idx += 1
                end_col = col_idx
                
                # Zeichne den horizontalen Streifen
                x = start_col * TILE_SIZE
                y = row_idx * TILE_SIZE
                width = (end_col - start_col) * TILE_SIZE
                height = TILE_SIZE
                
                # Skalierung anwenden
                scaled_x, scaled_y = scale_position(x, y)
                scaled_width = int(width * scale_x)
                scaled_height = int(height * scale_y)
                
                pygame.draw.rect(screen, Blue, (scaled_x, scaled_y, scaled_width, scaled_height))
            else:
                col_idx += 1
    
    # Zeichne Geister-Wände (Typ 5) separat als dunklere Wände
    for row_idx, row in enumerate(Maze):
        for col_idx, tile in enumerate(row):
            if tile == 5:  # Geister-Wand
                scaled_x, scaled_y = scale_position(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                scaled_width, scaled_height = scale_size(TILE_SIZE, TILE_SIZE)
                # Dunklere blaue Farbe für Geister-Wände
                pygame.draw.rect(screen, (0, 0, 128), (scaled_x, scaled_y, scaled_width, scaled_height))

def draw_maze_elements(screen, scale_x, scale_y):
    """Zeichnet alle Maze-Elemente außer Wände"""
    for row_idx, row in enumerate(Maze):
        for col_idx, tile in enumerate(row):
            scaled_x, scaled_y = scale_position(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
            scaled_width, scaled_height = scale_size(TILE_SIZE, TILE_SIZE)
            
            if tile == 2:  # Geister-Box
                pygame.draw.rect(screen, Gray, (scaled_x, scaled_y, scaled_width, scaled_height))
            elif tile == 3:  # Punkte
                # Zeichne kleine weiße Punkte in der Mitte der Tiles
                center_x, center_y = scale_position(col_idx * TILE_SIZE + TILE_SIZE // 2, row_idx * TILE_SIZE + TILE_SIZE // 2)
                point_radius = max(1, int(3 * scale_x))
                pygame.draw.circle(screen, White, (center_x, center_y), point_radius)
            elif tile == 4:  # Power-Ups
                # Zeichne große gelbe Punkte mit pulsierendem Effekt
                center_x, center_y = scale_position(col_idx * TILE_SIZE + TILE_SIZE // 2, row_idx * TILE_SIZE + TILE_SIZE // 2)
                pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0  # Pulsiert zwischen 0 und 1
                powerup_radius = max(3, int((8 + pulse * 3) * scale_x))
                pygame.draw.circle(screen, Yellow, (center_x, center_y), powerup_radius)

def reset_ghosts():
    """Setzt alle Geister auf ihre Startpositionen zurück"""
    current_speed = get_current_speed()
    start_positions = [
        (450, 350),  # Rot - Tile-Mitte
        (425, 325),  # Pink - Tile-Mitte
        (475, 325),  # Orange - Tile-Mitte  
        (425, 375)   # Cyan - Tile-Mitte
    ]
    release_times = [0, 90, 180, 270]
    
    for i, ghost in enumerate(ghosts):
        ghost.x, ghost.y = start_positions[i]
        ghost.direction_x, ghost.direction_y = 0, -current_speed  # Level-angepasste Geschwindigkeit
        ghost.speed = current_speed  # Aktualisiere Geister-Geschwindigkeit
        ghost.in_box = True
        ghost.release_timer = release_times[i]
        ghost.eaten = False

def is_valid_position(x, y):
    """Überprüft ob eine Position gültig ist - Grid-basiert wie im Original"""
    # Konvertiere Position zu Tile-Koordinaten
    tile_x = int(x) // TILE_SIZE
    tile_y = int(y) // TILE_SIZE
    
    # Überprüfen ob Tile in gültigen Bereichen ist
    if (tile_x < 0 or tile_x >= len(Maze[0]) or 
        tile_y < 0 or tile_y >= len(Maze)):
        return False
    
    # Überprüfe ob Tile begehbar ist für Pacman
    tile_value = Maze[tile_y][tile_x]
    # Pacman kann nicht durch normale Wände (1) oder Geister-Wände (5) gehen
    return tile_value not in [1, 5]

def can_move_in_direction(current_x, current_y, direction_x, direction_y):
    """Prüft ob Bewegung in eine bestimmte Richtung möglich ist"""
    # Berechne Ziel-Tile basierend auf aktueller Position und Richtung
    current_tile_x = current_x // TILE_SIZE
    current_tile_y = current_y // TILE_SIZE
    
    target_tile_x = current_tile_x
    target_tile_y = current_tile_y
    
    if direction_x > 0:  # Rechts
        target_tile_x += 1
    elif direction_x < 0:  # Links
        target_tile_x -= 1
    elif direction_y > 0:  # Unten
        target_tile_y += 1
    elif direction_y < 0:  # Oben
        target_tile_y -= 1
    
    # Prüfe ob Ziel-Tile gültig ist
    target_x = target_tile_x * TILE_SIZE + TILE_SIZE // 2
    target_y = target_tile_y * TILE_SIZE + TILE_SIZE // 2
    
    return is_valid_position(target_x, target_y)

def is_valid_ghost_position(x, y):
    """Überprüft ob eine Position für Geister gültig ist"""
    ghost_radius = 18
    
    left = (x - ghost_radius) // TILE_SIZE
    right = (x + ghost_radius) // TILE_SIZE
    top = (y - ghost_radius) // TILE_SIZE
    bottom = (y + ghost_radius) // TILE_SIZE
    
    if (left < 0 or right >= len(Maze[0]) or 
        top < 0 or bottom >= len(Maze)):
        return False
    
    # Geister können durch freie Bereiche (0), Geister-Box (2) und Geister-Wände (5) gehen
    # aber nicht durch normale Wände (1)
    if (Maze[top][left] == 1 or 
        Maze[top][right] == 1 or 
        Maze[bottom][left] == 1 or 
        Maze[bottom][right] == 1):
        return False
    
    return True

class Ghost:
    def __init__(self, x, y, color, release_delay=0):
        self.x = x
        self.y = y
        self.start_x = x  # Startposition merken
        self.start_y = y  # Startposition merken
        self.color = color
        self.original_color = color  # Für Power-Up Zustand
        self.direction_x = 0
        self.direction_y = -get_current_speed()  # Level-angepasste Startgeschwindigkeit
        self.speed = get_current_speed()  # Level-angepasste Geschwindigkeit
        self.in_box = True  # Startet in der Geister-Box
        self.release_timer = release_delay  # Verzögerung bevor Geist die Box verlässt
        self.original_release_delay = release_delay  # Original-Verzögerung merken
        self.eaten = False  # Wurde der Geist gefressen?
        
    def find_path_to_pacman(self):
        """Finde den direktesten Weg zu Pacman - oder laufe weg wenn Power-Up aktiv"""
        current_tile_x = self.x // TILE_SIZE
        current_tile_y = self.y // TILE_SIZE
        
        pacman_tile_x = Pacman_x // TILE_SIZE
        pacman_tile_y = Pacman_y // TILE_SIZE
        
        # Mögliche Richtungen: rechts, links, unten, oben
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_directions = []
        
        # Aktuelle Richtung normalisieren (für Anti-Rückwärts-Logik)
        current_dir_x = 0
        current_dir_y = 0
        if self.direction_x != 0:
            current_dir_x = 1 if self.direction_x > 0 else -1
        if self.direction_y != 0:
            current_dir_y = 1 if self.direction_y > 0 else -1
        
        # Sammle alle gültigen Richtungen
        for dx, dy in directions:
            next_tile_x = current_tile_x + dx
            next_tile_y = current_tile_y + dy
            
            # Prüfe ob das nächste Tile gültig ist
            if (0 <= next_tile_x < len(Maze[0]) and 
                0 <= next_tile_y < len(Maze) and 
                Maze[next_tile_y][next_tile_x] not in [1]):  # Nur normale Wände blockieren Geister
                
                valid_directions.append((dx, dy))
        
        if not valid_directions:
            return (1, 0)  # Default: rechts
        
        # Entferne Rückwärtsrichtung nur wenn mehr als eine Option verfügbar ist
        opposite_dir = (-current_dir_x, -current_dir_y)
        if len(valid_directions) > 1 and opposite_dir in valid_directions:
            valid_directions.remove(opposite_dir)
        
        # *** FLUCHTVERHALTEN: Wenn Power-Up aktiv ist, laufe WEG von Pacman ***
        if power_up_active and not self.eaten:
            best_direction = valid_directions[0]
            best_distance = -1  # Wir wollen die GRÖSSTE Entfernung
            
            for dx, dy in valid_directions:
                next_tile_x = current_tile_x + dx
                next_tile_y = current_tile_y + dy
                
                # Berechne Manhattan-Entfernung zu Pacman
                distance = abs(next_tile_x - pacman_tile_x) + abs(next_tile_y - pacman_tile_y)
                
                # *** WICHTIG: Wähle die Richtung mit der GRÖSSTEN Entfernung ***
                if distance > best_distance:
                    best_distance = distance
                    best_direction = (dx, dy)
            
            return best_direction
        
        else:
            # *** JAGDVERHALTEN: Normales Verhalten - Jage Pacman ***
            best_direction = valid_directions[0]
            best_distance = float('inf')
            
            for dx, dy in valid_directions:
                next_tile_x = current_tile_x + dx
                next_tile_y = current_tile_y + dy
                
                # Berechne Manhattan-Entfernung zu Pacman
                distance = abs(next_tile_x - pacman_tile_x) + abs(next_tile_y - pacman_tile_y)
                
                # *** WICHTIG: Wähle die Richtung mit der KLEINSTEN Entfernung ***
                if distance < best_distance:
                    best_distance = distance
                    best_direction = (dx, dy)
            
            return best_direction
        
    def move(self):
        # Warten bis Release-Timer abgelaufen ist
        if self.release_timer > 0:
            self.release_timer -= 1
            return
        
        # Prüfe ob Geist noch in der Box ist
        current_tile_x = self.x // TILE_SIZE
        current_tile_y = self.y // TILE_SIZE
        
        # Wenn Geist aus der Box-Area (Tile-Wert 2) raus ist
        if self.in_box and Maze[current_tile_y][current_tile_x] != 2:
            self.in_box = False
        
        if self.in_box:
           
            self.direction_x = 0
            self.direction_y = -self.speed
        else:
            
            test_x = self.x + self.direction_x
            test_y = self.y + self.direction_y
            
           
            if not is_valid_position(test_x, test_y):
               
                direction = self.find_path_to_pacman()
                self.direction_x = direction[0] * self.speed
                self.direction_y = direction[1] * self.speed
            
            # *** RICHTUNGS-UPDATE: Alle 20 Frames - sowohl beim Jagen als auch beim Weglaufen ***
            elif pygame.time.get_ticks() % 20 == 0:
                direction = self.find_path_to_pacman()
                new_dir_x = direction[0] * self.speed
                new_dir_y = direction[1] * self.speed
                
                # Richtung ändern (sowohl für Jagd- als auch für Fluchtverhalten)
                if new_dir_x != self.direction_x or new_dir_y != self.direction_y:
                    self.direction_x = new_dir_x
                    self.direction_y = new_dir_y
        
        # Bewege in aktuelle Richtung
        new_x = self.x + self.direction_x
        new_y = self.y + self.direction_y
        
        # Prüfe ob neue Position gültig ist
        if is_valid_position(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def draw(self, screen):
        if not self.eaten:
            # *** VISUELLER INDIKATOR: Zeige blaue Farbe wenn Power-Up aktiv ist (= Geister laufen weg) ***
            color = Blue if power_up_active else self.original_color
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 18)
    
    def respawn(self):
        """Lässt den Geist nach dem Power-Up wieder in der Box erscheinen"""
        self.x = self.start_x
        self.y = self.start_y
        self.direction_x = 0
        self.direction_y = -self.speed  # Verwende aktuelle Level-Geschwindigkeit
        self.in_box = True
        self.release_timer = self.original_release_delay  # Mit ursprünglicher Verzögerung
        self.eaten = False
        print(f"DEBUG: Geist respawned in Box bei ({self.start_x}, {self.start_y})")

# Spiel-Status
game_over = False
score = 0
power_up_active = False
power_up_timer = 0
level = 1
level_completed = False

# *** GESCHWINDIGKEITS-SYSTEM ***
base_speed = 4  # Basis-Geschwindigkeit für Level 1
speed_increase_per_level = 0.50  # 50% Erhöhung pro Level

def get_current_speed():
    """Berechnet die aktuelle Geschwindigkeit basierend auf dem Level"""
    current_speed = base_speed * (1 + speed_increase_per_level) ** (level - 1)
    return int(current_speed)  # Als Integer für pixelgenaue Bewegung

# Font für Score-Anzeige
pygame.font.init()
score_font = pygame.font.Font(None, 36)

# Initialisiere das erste Level
generate_new_level()

# Erstelle Geister NACH der Level-Initialisierung (mit unterschiedlichen Release-Zeiten)
ghosts = [
    Ghost(450, 350, Red, 0),      # Rote Geist - sofort
    Ghost(425, 325, Pink, 90),    # Pinke Geist - nach 3 Sekunden
    Ghost(475, 325, Orange, 180), # Orange Geist - nach 6 Sekunden
    Ghost(425, 375, Cyan, 270)    # Cyan Geist - nach 9 Sekunden
]

# *** ZUFÄLLIGE PACMAN SPAWN-POSITION ***
spawn_pos = get_random_spawn_position()
Pacman_x = spawn_pos[0]  # Zufällige Position - Tile-Mitte
Pacman_y = spawn_pos[1]  # Zufällige Position - Tile-Mitte
pacman_speed = get_current_speed()  # Level-angepasste Geschwindigkeit
pacman_radius = 20  # Größer, damit Gänge gut gefüllt werden
direction_x = 0  # Startet stillstehend
direction_y = 0  # Startet stillstehend
next_direction_x = 0  # Gewünschte nächste Richtung X (Input Buffer)
next_direction_y = 0  # Gewünschte nächste Richtung Y (Input Buffer)

while True:
    if not game_over and not level_completed:
        keys = pygame.key.get_pressed()
        
        # Richtung ändern basierend auf Tasteneingabe (Input Buffering wie im Original)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Input Buffering - speichere gewünschte Richtung
                # *** VOLLBILD-TOGGLE MIT F11 ***
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_LEFT:
                    next_direction_x = -pacman_speed
                    next_direction_y = 0
                elif event.key == pygame.K_RIGHT:
                    next_direction_x = pacman_speed
                    next_direction_y = 0
                elif event.key == pygame.K_UP:
                    next_direction_x = 0
                    next_direction_y = -pacman_speed
                elif event.key == pygame.K_DOWN:
                    next_direction_x = 0
                    next_direction_y = pacman_speed
        
        # Prüfe ob gewünschte Richtung (Input Buffer) möglich ist
        if next_direction_x != 0 or next_direction_y != 0:
            # Teste die gewünschte neue Position
            test_x = Pacman_x + next_direction_x
            test_y = Pacman_y + next_direction_y
            if is_valid_position(test_x, test_y):
                # Ändere Richtung nur wenn möglich
                direction_x = next_direction_x
                direction_y = next_direction_y
                next_direction_x = 0
                next_direction_y = 0
        
        # Normale Bewegung in aktuelle Richtung
        new_x = Pacman_x
        new_y = Pacman_y
        
        # Bewege nur wenn eine Richtung aktiv ist
        if direction_x != 0 or direction_y != 0:
            # Berechne neue Position
            test_x = Pacman_x + direction_x
            test_y = Pacman_y + direction_y
            
            # Prüfe ob Bewegung in aktuelle Richtung möglich ist
            if is_valid_position(test_x, test_y):
                new_x = test_x
                new_y = test_y
            else:
                # Stoppe an Wand - wie im Original
                direction_x = 0
                direction_y = 0

        # Bewegung ausführen - Grid-basiert
        Pacman_x = new_x
        Pacman_y = new_y
        
        # Prüfe ob Pacman einen Punkt oder Power-Up einsammelt
        pacman_tile_x = Pacman_x // TILE_SIZE
        pacman_tile_y = Pacman_y // TILE_SIZE
        if (0 <= pacman_tile_x < len(Maze[0]) and 
            0 <= pacman_tile_y < len(Maze)):
            
            tile_value = Maze[pacman_tile_y][pacman_tile_x]
            
            if tile_value == 3:  # Normaler Punkt
                Maze[pacman_tile_y][pacman_tile_x] = 0  # Punkt entfernen
                score += 10  # Punkte hinzufügen
                
            elif tile_value == 4:  # Power-Up
                Maze[pacman_tile_y][pacman_tile_x] = 0  # Power-Up entfernen
                score += 50  # Mehr Punkte für Power-Up
                power_up_active = True
                power_up_timer = pygame.time.get_ticks() + 10000  # 10 Sekunden Power-Up
                
                # Setze alle Geister zurück (sie können wieder gefressen werden)
                for ghost in ghosts:
                    ghost.eaten = False
        
        # Power-Up Timer überprüfen
        if power_up_active and pygame.time.get_ticks() > power_up_timer:
            power_up_active = False
            # Respawn alle gefressenen Geister in der Box
            for ghost in ghosts:
                if ghost.eaten:
                    ghost.respawn()
        
        # Prüfe ob Level komplett ist (alle Punkte und Power-Ups eingesammelt)
        points_remaining = 0
        for row in Maze:
            for tile in row:
                if tile == 3 or tile == 4:  # Punkte oder Power-Ups
                    points_remaining += 1
        
        # Debug: Zeige verbleibende Punkte an (nur alle 60 Frames)
        if pygame.time.get_ticks() % 2000 == 0:  # Alle 2 Sekunden
            print(f"Verbleibende Punkte: {points_remaining}")
        
        if points_remaining == 0:
            level_completed = True
            print(f"Level {level} abgeschlossen!")
        
        # Bewege Geister
        for ghost in ghosts:
            ghost.move()
        
        # Kollisionserkennung: Geister vs Pacman
        for ghost in ghosts:
            if not ghost.eaten:
                distance = ((ghost.x - Pacman_x)**2 + (ghost.y - Pacman_y)**2)**0.5
                if distance < 30:  # Kollision erkannt
                    if power_up_active:
                        # Pacman frisst Geist
                        ghost.eaten = True
                        score += 100  # Bonus für Geist fressen
                    else:
                        # Geist frisst Pacman
                        game_over = True
    
    
    elif level_completed:
        # Level Completed Bildschirm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # *** VOLLBILD-TOGGLE AUCH IM LEVEL COMPLETE MENÜ ***
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    # Nächstes Level starten
                    print(f"Starte Level {level + 1}")
                    level_completed = False
                    level += 1
                    power_up_active = False
                    power_up_timer = 0
                    
                    # *** GESCHWINDIGKEIT FÜR NEUES LEVEL ANPASSEN ***
                    pacman_speed = get_current_speed()
                    print(f"Neue Geschwindigkeit für Level {level}: {pacman_speed}")
                    
                    # Neues Level-Layout generieren (jetzt mit Zufalls-Generierung ab Level 3)
                    generate_new_level()
                    if level <= 2:
                        print(f"Vordefiniertes Layout für Level {level} geladen")
                    else:
                        print(f"Zufälliges Layout für Level {level} generiert!")
                    
                    # *** PACMAN ZUFÄLLIG SPAWNEN ***
                    spawn_pos = get_random_spawn_position()
                    Pacman_x = spawn_pos[0]  # Zufällige Position - Tile-Mitte
                    Pacman_y = spawn_pos[1]  # Zufällige Position - Tile-Mitte
                    direction_x = 0  # Startet stillstehend
                    direction_y = 0
                    
                    # Geister zurücksetzen (mit neuer Geschwindigkeit)
                    reset_ghosts()
    
    else:
        # Game Over Bildschirm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # *** VOLLBILD-TOGGLE AUCH IM GAME OVER MENÜ ***
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    # Spiel neu starten - Original-like Reset
                    game_over = False
                    level_completed = False
                    score = 0
                    level = 1  # Zurück zu Level 1
                    power_up_active = False
                    power_up_timer = 0
                    
                    # *** GESCHWINDIGKEIT ZURÜCKSETZEN ***
                    pacman_speed = get_current_speed()  # Level 1 Geschwindigkeit
                    print(f"Spiel neugestartet - Geschwindigkeit zurückgesetzt: {pacman_speed}")
                    
                    # *** PACMAN ZUFÄLLIG SPAWNEN BEI NEUSTART ***
                    spawn_pos = get_random_spawn_position()
                    Pacman_x = spawn_pos[0]  # Zufällige Position - Tile-Mitte
                    Pacman_y = spawn_pos[1]  # Zufällige Position - Tile-Mitte
                    direction_x = 0  # Startet stillstehend
                    direction_y = 0
                    next_direction_x = 0  # Reset Input Buffer
                    next_direction_y = 0
                    
                    # Maze zurücksetzen (Level 1 wiederherstellen)
                    generate_new_level()
                    
                    # Geister zurücksetzen (mit Level 1 Geschwindigkeit)
                    reset_ghosts()

    # *** VOLLBILD-KOMPATIBLES RENDERING ***
    if fullscreen:
        # Schwarzen Hintergrund für Vollbild
        screen.fill(Black)
    else:
        screen.fill(Black)

    # Skalierungsfaktoren berechnen
    scale_x, scale_y = get_scale_factors()

    # *** VERBESSERTE WAND-DARSTELLUNG FÜR VOLLBILD ***
    draw_walls(screen, scale_x, scale_y)
    draw_maze_elements(screen, scale_x, scale_y)
    
    if not game_over and not level_completed:
        # *** SKALIERTES PACMAN RENDERING ***
        scaled_pacman_x, scaled_pacman_y = scale_position(Pacman_x, Pacman_y)
        scaled_pacman_radius = max(5, int(pacman_radius * scale_x))
        pygame.draw.circle(screen, Yellow, (scaled_pacman_x, scaled_pacman_y), scaled_pacman_radius)
        
        # *** SKALIERTE GEISTER RENDERING ***
        for ghost in ghosts:
            if not ghost.eaten:
                scaled_ghost_x, scaled_ghost_y = scale_position(ghost.x, ghost.y)
                scaled_ghost_radius = max(4, int(18 * scale_x))
                color = Blue if power_up_active else ghost.original_color
                pygame.draw.circle(screen, color, (scaled_ghost_x, scaled_ghost_y), scaled_ghost_radius)
        
        # *** SKALIERTE UI ELEMENTE ***
        font_size = max(18, int(36 * scale_x))
        ui_font = pygame.font.Font(None, font_size)
        
        score_text = ui_font.render(f"Score: {score}", True, White)
        level_text = ui_font.render(f"Level: {level}", True, White)
        
        ui_x, ui_y = scale_position(10, 10)
        screen.blit(score_text, (ui_x, ui_y))
        
        level_y = ui_y + int(40 * scale_y)
        screen.blit(level_text, (ui_x, level_y))
        
        # Power-Up Status anzeigen
        if power_up_active:
            remaining_time = max(0, (power_up_timer - pygame.time.get_ticks()) // 1000)
            power_text = ui_font.render(f"Power-Up: {remaining_time}s", True, Yellow)
            power_y = level_y + int(40 * scale_y)
            screen.blit(power_text, (ui_x, power_y))
            
        # Vollbild-Hinweis
        if fullscreen:
            hint_font = pygame.font.Font(None, max(16, int(24 * scale_x)))
            hint_text = hint_font.render("F11: Vollbild beenden", True, White)
            hint_x = current_screen_size[0] - hint_text.get_width() - 10
            hint_y = 10
            screen.blit(hint_text, (hint_x, hint_y))
        else:
            hint_font = pygame.font.Font(None, 24)
            hint_text = hint_font.render("F11: Vollbild", True, White)
            screen.blit(hint_text, (original_screen_size[0] - hint_text.get_width() - 10, 10))
    
    elif level_completed:
        # *** SKALIERTES LEVEL COMPLETED MENÜ ***
        menu_font_size = max(37, int(74 * min(scale_x, scale_y)))
        small_font_size = max(18, int(36 * min(scale_x, scale_y)))
        
        font = pygame.font.Font(None, menu_font_size)
        small_font = pygame.font.Font(None, small_font_size)
        
        completed_text = font.render("LEVEL COMPLETED!", True, Yellow)
        score_display = font.render(f"Score: {score}", True, White)
        next_level_text = font.render(f"Next: Level {level + 1}", True, Green)
        continue_text = small_font.render("Drücke SPACE um fortzufahren", True, White)
        
        # Zentriere die Texte horizontal und vertikal
        screen_center_x = current_screen_size[0] // 2
        screen_center_y = current_screen_size[1] // 2
        
        completed_rect = completed_text.get_rect(center=(screen_center_x, screen_center_y - int(80 * scale_y)))
        score_rect = score_display.get_rect(center=(screen_center_x, screen_center_y - int(20 * scale_y)))
        next_rect = next_level_text.get_rect(center=(screen_center_x, screen_center_y + int(40 * scale_y)))
        continue_rect = continue_text.get_rect(center=(screen_center_x, screen_center_y + int(100 * scale_y)))
        
        screen.blit(completed_text, completed_rect)
        screen.blit(score_display, score_rect)
        screen.blit(next_level_text, next_rect)
        screen.blit(continue_text, continue_rect)
    
    elif game_over:
        # *** SKALIERTES GAME OVER MENÜ ***
        menu_font_size = max(37, int(74 * min(scale_x, scale_y)))
        
        font = pygame.font.Font(None, menu_font_size)
        game_over_text = font.render("GAME OVER", True, Red)
        restart_text = font.render("Drücke SPACE zum Neustart", True, White)
        
        # Zentriere die Texte horizontal und vertikal
        screen_center_x = current_screen_size[0] // 2
        screen_center_y = current_screen_size[1] // 2
        
        game_over_rect = game_over_text.get_rect(center=(screen_center_x, screen_center_y - int(40 * scale_y)))
        restart_rect = restart_text.get_rect(center=(screen_center_x, screen_center_y + int(40 * scale_y)))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    clock.tick(30)
                            
            
                        
