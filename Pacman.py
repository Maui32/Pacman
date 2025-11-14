import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((900,700))
pygame.display.set_caption("Pacman")


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

def generate_new_level():
    """Generiert ein neues Level-Layout basierend auf der Level-Nummer"""
    global Maze, level
    
    # Verschiedene Level-Layouts
    level_layouts = [
        # Level 1 (Original)
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
        # Level 2 - Anderes Layout
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
    
    # Wähle Layout basierend auf Level (mit Wiederholung für höhere Level)
    layout_index = (level - 1) % len(level_layouts)
    Maze = [row[:] for row in level_layouts[layout_index]]  # Deep copy

def reset_ghosts():
    """Setzt alle Geister auf ihre Startpositionen zurück"""
    start_positions = [
        (450, 350),  # Rot - Tile-Mitte
        (425, 325),  # Pink - Tile-Mitte
        (475, 325),  # Orange - Tile-Mitte  
        (425, 375)   # Cyan - Tile-Mitte
    ]
    release_times = [0, 90, 180, 270]
    
    for i, ghost in enumerate(ghosts):
        ghost.x, ghost.y = start_positions[i]
        ghost.direction_x, ghost.direction_y = 0, -5  # Moderate Geschwindigkeit
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
    
    # Überprüfe ob Tile begehbar ist (0 = frei, 2 = Geister-Box auch erlaubt, 3 = Punkte, 4 = Power-Ups)
    tile_value = Maze[tile_y][tile_x]
    return tile_value != 1  # Nicht Wand

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
    
    # Geister können durch freie Bereiche (0) und Geister-Box (2) gehen
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
        self.direction_y = -5  # Startet mit moderater Bewegung nach oben
        self.speed = 5  # Moderate Geschwindigkeit passend zu Pacman
        self.in_box = True  # Startet in der Geister-Box
        self.release_timer = release_delay  # Verzögerung bevor Geist die Box verlässt
        self.original_release_delay = release_delay  # Original-Verzögerung merken
        self.eaten = False  # Wurde der Geist gefressen?
        
    def find_path_to_pacman(self):
        """Finde den direktesten Weg zu Pacman - aggressive Verfolgung"""
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
                Maze[next_tile_y][next_tile_x] != 1):  # Nicht Wand
                
                valid_directions.append((dx, dy))
        
        if not valid_directions:
            return (1, 0)  # Default: rechts
        
        # Entferne Rückwärtsrichtung nur wenn mehr als eine Option verfügbar ist
        opposite_dir = (-current_dir_x, -current_dir_y)
        if len(valid_directions) > 1 and opposite_dir in valid_directions:
            valid_directions.remove(opposite_dir)
        
        # Finde die Richtung mit der kleinsten Entfernung zu Pacman
        best_direction = valid_directions[0]
        best_distance = float('inf')
        
        for dx, dy in valid_directions:
            next_tile_x = current_tile_x + dx
            next_tile_y = current_tile_y + dy
            
            # Berechne Manhattan-Entfernung zu Pacman
            distance = abs(next_tile_x - pacman_tile_x) + abs(next_tile_y - pacman_tile_y)
            
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
            # Bewege dich einfach nach oben aus der Box
            self.direction_x = 0
            self.direction_y = -self.speed
        else:
            # Kontinuierliche Bewegung - ändere Richtung bei Kollision oder regelmäßig
            # Berechne neue Position
            test_x = self.x + self.direction_x
            test_y = self.y + self.direction_y
            
            # Prüfe ob aktuelle Richtung blockiert ist mit einfacher Tile-Prüfung
            if not is_valid_position(test_x, test_y):
                # Finde neue Richtung
                direction = self.find_path_to_pacman()
                self.direction_x = direction[0] * self.speed
                self.direction_y = direction[1] * self.speed
            
            # Regelmäßig Richtung neu berechnen (alle 45 Frames)
            elif pygame.time.get_ticks() % 45 == 0:
                direction = self.find_path_to_pacman()
                new_dir_x = direction[0] * self.speed
                new_dir_y = direction[1] * self.speed
                
                # Ändere Richtung wenn sie anders ist (aktive Verfolgung!)
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
            # Zeige blaue Farbe wenn Power-Up aktiv ist, sonst normale Farbe
            color = Blue if power_up_active else self.original_color
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 18)
    
    def respawn(self):
        """Lässt den Geist nach dem Power-Up wieder in der Box erscheinen"""
        self.x = self.start_x
        self.y = self.start_y
        self.direction_x = 0
        self.direction_y = -5  # Moderate Geschwindigkeit
        self.in_box = True
        self.release_timer = self.original_release_delay  # Mit ursprünglicher Verzögerung
        self.eaten = False
        print(f"DEBUG: Geist respawned in Box bei ({self.start_x}, {self.start_y})")

# Erstelle Geister (mit unterschiedlichen Release-Zeiten)
ghosts = [
    Ghost(450, 350, Red, 0),      # Rote Geist - sofort
    Ghost(425, 325, Pink, 90),    # Pinke Geist - nach 3 Sekunden
    Ghost(475, 325, Orange, 180), # Orange Geist - nach 6 Sekunden
    Ghost(425, 375, Cyan, 270)    # Cyan Geist - nach 9 Sekunden
]

# Spiel-Status
game_over = False
score = 0
power_up_active = False
power_up_timer = 0
level = 1
level_completed = False

# Font für Score-Anzeige
pygame.font.init()
score_font = pygame.font.Font(None, 36)

# Initialisiere das erste Level
generate_new_level()


Pacman_x = 75  # Position in einem freien Bereich (1*50 + 25) - Tile-Mitte
Pacman_y = 75  # Position in einem freien Bereich (1*50 + 25) - Tile-Mitte
pacman_speed = 5  # Moderate tile-basierte Bewegung
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
                if event.key == pygame.K_LEFT:
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
                if event.key == pygame.K_SPACE:
                    # Nächstes Level starten
                    print(f"Starte Level {level + 1}")
                    level_completed = False
                    level += 1
                    power_up_active = False
                    power_up_timer = 0
                    
                    # Neues Level-Layout generieren
                    generate_new_level()
                    print(f"Neues Layout für Level {level} geladen")
                    
                    # Pacman zurücksetzen - in Tile-Mitte
                    Pacman_x = 75  # Tile-Mitte
                    Pacman_y = 75  # Tile-Mitte
                    direction_x = 0  # Startet stillstehend
                    direction_y = 0
                    
                    # Geister zurücksetzen
                    reset_ghosts()
    
    else:
        # Game Over Bildschirm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Spiel neu starten - Original-like Reset
                    game_over = False
                    level_completed = False
                    score = 0
                    level = 1
                    power_up_active = False
                    power_up_timer = 0
                    Pacman_x = 75  # Tile-Mitte
                    Pacman_y = 75  # Tile-Mitte
                    direction_x = 0  # Startet stillstehend
                    direction_y = 0
                    next_direction_x = 0  # Reset Input Buffer
                    next_direction_y = 0
                    
                    # Maze zurücksetzen (Level 1 wiederherstellen)
                    generate_new_level()
                    
                    # Geister zurücksetzen
                    reset_ghosts()

    screen.fill(Black)

    for row_idx, row in enumerate(Maze):
        for col_idx, tile in enumerate(row):
            if tile == 1: 
                pygame.draw.rect(screen, Blue, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 2:  # Geister-Box
                pygame.draw.rect(screen, Gray, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 3:  # Punkte
                # Zeichne kleine weiße Punkte in der Mitte der Tiles
                center_x = col_idx * TILE_SIZE + TILE_SIZE // 2
                center_y = row_idx * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, White, (center_x, center_y), 3)
            elif tile == 4:  # Power-Ups
                # Zeichne große gelbe Punkte
                center_x = col_idx * TILE_SIZE + TILE_SIZE // 2
                center_y = row_idx * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, Yellow, (center_x, center_y), 8)
    
    if not game_over and not level_completed:
        # Zeichne Pacman
        pygame.draw.circle(screen, Yellow, (Pacman_x, Pacman_y), pacman_radius)
        
        # Zeichne Geister
        for ghost in ghosts:
            ghost.draw(screen)
        
        # Score anzeigen
        score_text = score_font.render(f"Score: {score}", True, White)
        screen.blit(score_text, (10, 10))
        
        # Level anzeigen
        level_text = score_font.render(f"Level: {level}", True, White)
        screen.blit(level_text, (10, 50))
        
        # Power-Up Status anzeigen
        if power_up_active:
            remaining_time = max(0, (power_up_timer - pygame.time.get_ticks()) // 1000)
            power_text = score_font.render(f"Power-Up: {remaining_time}s", True, Yellow)
            screen.blit(power_text, (10, 90))
    
    elif level_completed:
        # Level Completed Text
        font = pygame.font.Font(None, 74)
        completed_text = font.render("LEVEL COMPLETED!", True, Yellow)
        score_display = font.render(f"Score: {score}", True, White)
        next_level_text = font.render(f"Next: Level {level + 1}", True, Green)
        continue_text = score_font.render("Drücke SPACE um fortzufahren", True, White)
        
        screen.blit(completed_text, (200, 250))
        screen.blit(score_display, (300, 320))
        screen.blit(next_level_text, (280, 390))
        screen.blit(continue_text, (250, 460))
    
    elif game_over:
        # Game Over Text
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("GAME OVER", True, Red)
        restart_text = font.render("Drücke SPACE zum Neustart", True, White)
        
        screen.blit(game_over_text, (300, 300))
        screen.blit(restart_text, (200, 400))
    
    pygame.display.flip()
    clock.tick(30)
                            
            
                        
