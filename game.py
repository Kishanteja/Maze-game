import pygame
import random
import time

#starting pygame
pygame.init()

#creating all fonts
font1 = pygame.font.SysFont("comicsansms", 49, True)
font2 = pygame.font.SysFont("comicsansms", 150, True)
font3 = pygame.font.SysFont("comicsansms", 28, True)

# Function to displays time
def get_time(hours, minutes, seconds):
    a = str(hours).zfill(2)
    b = str(minutes).zfill(2)
    c = str(seconds).zfill(2)
    return a + ":" + b + ":" + c

# Function to create the time counter
def draw_time(start_time, timer_duration):
    elapsed_time = time.time() - start_time
    remaining_time = max(0, timer_duration - elapsed_time)
    hours, remainder = divmod(remaining_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    return font1.render(get_time(int(hours), int(minutes), int(seconds)), True, (255, 255, 255))

# creating cell
class Cell:
    def __init__(self, up, down, left, right):
        self.visited = False
        self.walls = [up, down, left, right]

'''
this code is based on prim's algorithm 
'''
class Labyrinth:
    def __init__(self, id):
        self.id = id
        self.walls = []
        self.maze_walls = []
        self.cells = []
        self.obstacle = []

        x = 0
        t = 0
        # changing difficult levels by making changes in no of rows and columns
        if self.id == 1:
            rows = 6
            cols = 8
            cell_size = 120
            wall_offset = 40
            travel = 80
            text_space = (0, )
        elif self.id == 2:
            rows = 12
            cols = 16
            cell_size = 60
            wall_offset = 20
            travel = 40
            text_space = (0, 1,)
        elif self.id == 3:
            rows = 24
            cols = 32
            cell_size = 30
            wall_offset = 10
            travel = 20
            text_space = (0, 1, 2, 3,)

        for f in range(rows):
            for s in range(cols):
                # i added this part to make sure there is no maze generated where score,lives and timer is present
                if not (f in text_space and s >= 0):
                    self.cells.append(
                        Cell((x + wall_offset, t, travel, wall_offset), 
                             (x + wall_offset, t + cell_size, travel, wall_offset), 
                             (x, t + wall_offset, wall_offset, travel), 
                             (x + cell_size, t + wall_offset, wall_offset, travel)))
                x += cell_size
            x = 0
            t += cell_size

        # Generates maze using Prim's algorithm
        for v in self.cells[0].walls:
            self.maze_walls.append(v)
            self.walls.append(v)

        self.cells[0].visited = True

        while len(self.walls) > 0:
            wall = random.choice(self.walls)
            # Checks which cells are divided by the wall
            divided_cells = []
            for u in self.cells:
                if wall in u.walls:
                    divided_cells.append(u)

            if len(divided_cells) > 1 and (
                    not ((divided_cells[0].visited and divided_cells[1].visited) or (
                    (not divided_cells[0].visited) and (not divided_cells[1].visited)))):
                # Checks which cells have been visited
                for k in divided_cells:
                    k.walls.remove(wall)

                    if not k.visited:
                        k.visited = True

                    for q in k.walls:
                        if q not in self.walls:
                            self.walls.append(q)

                        if q not in self.maze_walls:
                            self.maze_walls.append(q)

                    if wall in self.maze_walls:
                        self.maze_walls.remove(wall)

            self.walls.remove(wall)

        # Add obstacle to the maze
        self.add_obstacle()

        for j in range(0, 730, cell_size):
            for i in range(0, 970, cell_size):
                self.maze_walls.append((i, j, wall_offset, wall_offset))

    # Function to add obstacle to the maze
    def add_obstacle(self):
        obstacle_count = 0
        if self.id == 1:
            obstacle_count = 5
        elif self.id == 2:
            obstacle_count = 15
        elif self.id == 3:
            obstacle_count = 25

        while obstacle_count > 0:
            cell = random.choice(self.cells)
            if cell not in self.obstacle:
                self.obstacle.append(cell)
                obstacle_count -= 1

    def draw(self, goal, screen, player_x, player_y):
        screen.fill((0, 0, 0))

        # Define the size of the visible range around the player
        visible_x = 465  
        visible_y = 305

        # Calculate the visible area around the player
        visible_area = pygame.Rect(player_x - visible_x // 2, player_y - visible_y // 2, visible_x, visible_y)

        for k in self.maze_walls:
            if visible_area.colliderect(pygame.Rect(k[0], k[1], k[2], k[3])):
                pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(k[0], k[1], k[2], k[3]))

        # Draw obstacle within the visible area
        for cell in self.obstacle:
            for wall in cell.walls:
                if visible_area.colliderect(pygame.Rect(wall[0], wall[1], wall[2], wall[3])):
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(wall[0], wall[1], wall[2], wall[3]))

        #leaving space for other objects

        if self.id == 1:
            text_height = 120
        elif self.id == 2:
            text_height = 120
        elif self.id == 3:
            text_height = 120

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 970, text_height))  # Clock background
        pygame.draw.rect(screen, (0, 255, 0), goal)  # Finish


class Button:
    def __init__(self, x, y, width, height, color_button, text, color_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_button = color_button
        self.text = text
        self.color_text = color_text
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color_button, (self.x, self.y, self.width, self.height))
        font = font3
        text_rendered = font.render(self.text, True, self.color_text)
        text_rect = text_rendered.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_rendered, text_rect)
    
    def mouse_clicked(self, mouse_pos):
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height
    

def help_window():
    screen = pygame.display.set_mode((970, 730))
    done = False
    help_image = pygame.image.load("help.jpg")
    resized_help = pygame.transform.scale(help_image,(970,730))
    message = pygame.image.load("map_horizontal.png")
    resized_message = pygame.transform.scale(message,(530,700))
    template = pygame.image.load("template_3.png")
    resized_template = pygame.transform.scale(template,(100,50))

    # Define button for back
    back_button = Button(860, 10, 100, 50, (255, 255, 0), "Back", (0, 0, 0))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None
                if event.key == pygame.K_b:  # Added key event for going back to opening window
                    return opening_window()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.mouse_clicked(mouse_pos):
                    return opening_window()

        screen.fill((0, 0, 0))
        screen.blit(resized_help,(0,0))
        screen.blit(resized_message,(5,5))
        screen.blit(resized_template,(860,10))
        help_text = font3.render("Help:", True, (255, 255, 255))
        text_1 = font3.render("1. Move the player using arrow", True, (255, 255, 255))
        text_2 = font3.render("   keys or WASD keys.", True, (255, 255, 255))
        text_3 = font3.render("2. Guide the player to the", True, (255, 255, 255))
        text_4 = font3.render("   finish while avoiding obstacles.", True, (255, 255, 255))
        text_5 = font3.render("3. Three levels offer varying ", True, (255, 255, 255))
        text_6 = font3.render("   difficulty and challenges.", True, (255, 255, 255))
        text_7 = font3.render("4. Score is based on time and", True, (255, 255, 255))
        text_8 = font3.render("   distance traveled.", True, (255, 255, 255))
        text_9 = font3.render("5. You start with a limited number ", True, (255, 255, 255))
        text_10 = font3.render("   of lives, and collisions with", True, (255, 255, 255))
        text_11 = font3.render("   obstacles reduce them.", True, (255, 255, 255))
        screen.blit(help_text, (30, 50))
        screen.blit(text_1, (30, 100))
        screen.blit(text_2, (30, 140))
        screen.blit(text_3,(30,190))
        screen.blit(text_4,(30,230))
        screen.blit(text_5,(30,280))
        screen.blit(text_6,(30,320))
        screen.blit(text_7,(30,370))
        screen.blit(text_8,(30,410))
        screen.blit(text_9,(30,460))
        screen.blit(text_10,(30,510))
        screen.blit(text_11,(30,550))
        back_button.draw(screen)

        pygame.display.flip()

def opening_window():

    screen = pygame.display.set_mode((970, 730))

    opening_screen = True
    selected_level = None

    # Define buttons
    play_button = Button(435, 400, 100, 50, (0, 255, 0), "Play", (255, 255, 255))
    quit_button = Button(800, 30, 100, 50, (255, 0, 0), "Quit", (255, 255, 255))
    help_button = Button(300, 600, 100, 50, (0, 0, 255), "Help", (255, 255, 255))
    high_scores_button = Button(550, 600, 200, 50, (255, 255, 0), "High Scores", (0, 0, 0))
    intro = pygame.image.load("intro.jpg")
    resized_intro = pygame.transform.scale(intro,(970,730))
    message = pygame.image.load("map_horizontal.png")
    resized_message = pygame.transform.scale(message,(900,350))

    while opening_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if any button is clicked
                if play_button.mouse_clicked(mouse_pos):
                    opening_screen = False
                    return level_window()
                elif quit_button.mouse_clicked(mouse_pos):
                    pygame.quit()
                    return None
                elif help_button.mouse_clicked(mouse_pos):
                    return help_window()
                elif high_scores_button.mouse_clicked(mouse_pos):
                    return high_scores_window()

        # Draw opening window
        screen.fill((0, 0, 0))
        # Draw buttons
        screen.blit(resized_intro,(0,0))
        screen.blit(resized_message,(35,350))
        play_button.draw(screen)
        quit_button.draw(screen)
        help_button.draw(screen)
        high_scores_button.draw(screen)
        pygame.display.flip()

    return selected_level, screen

def read_high_scores():
    try:
        with open("highscore.txt", "r") as file:
            lines = file.readlines()
            high_scores = [(float(line.split(",")[0]), int(line.split(",")[1])) for line in lines]
            high_scores = sorted(high_scores, key=lambda x: x[0], reverse=True)[:5]  # Return top 5 high scores
            return high_scores
    except FileNotFoundError:
        return []

def write_high_score(score_value, level):
    try:
        with open("highscore.txt", "a") as file:
            file.write("{:.2f},{:d}\n".format(score_value, level))
    except FileNotFoundError:
        print("High score file not found. Could not save high score.")



def high_scores_window():
    high_scores = read_high_scores()
    screen = pygame.display.set_mode((970, 730))
    done = False

    # Define button for back
    back_button = Button(10, 10, 100, 50, (255, 255, 0), "Back", (0, 0, 0))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None
                if event.key == pygame.K_b:  # Added key event for going back to opening window
                    return opening_window()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if back button is clicked
                if back_button.mouse_clicked(mouse_pos):
                    return opening_window()

        screen.fill((0, 0, 0))
        # Draw text
        title_text = font3.render("High Scores:", True, (255, 255, 255))
        screen.blit(title_text, (50, 50))
        y_offset = 100
        for i, score in enumerate(high_scores, 1):
            score_text = font3.render(f"{i}. {score}", True, (255, 255, 255))
            screen.blit(score_text, (50, 50 + y_offset * i))
        
        # Draw back button
        back_button.draw(screen)

        pygame.display.flip()

    return screen


def level_window():
    # Initialize screen
    screen = pygame.display.set_mode((970, 730))

    # Display opening window
    level_screen = True
    selected_level = None

    # Define buttons for level selection
    level_1_button = Button(200, 400, 100, 50, (0, 255, 0), "1", (255, 255, 255))
    level_2_button = Button(468, 400, 100, 50, (0, 255, 0), "2", (255, 255, 255))
    level_3_button = Button(736, 400, 100, 50, (0, 255, 0), "3", (255, 255, 255))
    back_button = Button(10, 10, 100, 50, (255, 255, 0), "Back", (0, 0, 0))
    quit_button = Button(800, 30, 100, 50, (255, 0, 0), "Quit", (255, 255, 255))

    while level_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = 1
                    level_screen = False
                elif event.key == pygame.K_2:
                    selected_level = 2
                    level_screen = False
                elif event.key == pygame.K_3:
                    selected_level = 3
                    level_screen = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if any button is clicked
                if level_1_button.mouse_clicked(mouse_pos):
                    selected_level = 1
                    level_screen = False
                elif level_2_button.mouse_clicked(mouse_pos):
                    selected_level = 2
                    level_screen = False
                elif level_3_button.mouse_clicked(mouse_pos):
                    selected_level = 3
                    level_screen = False
                elif back_button.mouse_clicked(mouse_pos):
                    return opening_window()
                elif quit_button.mouse_clicked(mouse_pos):
                    pygame.quit()
                    return None

        # Draw opening window
        screen.fill((0, 0, 0))
        # Draw buttons
        level_1_button.draw(screen)
        level_2_button.draw(screen)
        level_3_button.draw(screen)
        back_button.draw(screen)
        quit_button.draw(screen)
        # Draw other text
        text_select_level = font1.render("Select Level:", True, (255, 255, 255))
        text_start = font1.render("Press 1, 2, 3 to Play", True, (255, 255, 255))
        text_quit = font1.render("Press ESC to Quit", True, (255, 255, 255))
        screen.blit(text_select_level, (468 - (text_select_level.get_width() // 2), 250))
        screen.blit(text_start, (468 - (text_start.get_width() // 2), 500))
        screen.blit(text_quit, (468 - (text_quit.get_width() // 2), 550))
        

        pygame.display.flip()

    return selected_level, screen

def ending_screen(score, selected_level, victory=False):
    screen = pygame.display.set_mode((970, 730))
    done = False

    # Define buttons for options
    back_button = Button(385, 328 + 100, 200, 50, (0, 255, 0), "Back", (255, 255, 255))
    quit_button = Button(385, 328 + 200, 200, 50, (0, 255, 0), "Quit", (255, 255, 255))

    if victory:
        text_message = "VICTORY!"
    else:
        text_message = "GAME OVER"

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None

            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_m:
                    return opening_window()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None, None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if any button is clicked
                if back_button.mouse_clicked(mouse_pos):
                    write_high_score(int(max(0, score)), selected_level)
                    return opening_window()
                elif quit_button.mouse_clicked(mouse_pos):
                    pygame.quit()
                    return None, None

        screen.fill((0, 0, 0))
        # Draw buttons
        back_button.draw(screen)
        quit_button.draw(screen)
        # Draw other text
        text_message_rendered = font2.render(text_message, True, (255, 255, 255))
        text_score = font1.render("Score: {0}".format(int(max(0, score))), True, (255, 255, 255))
        screen.blit(text_message_rendered, (468 - (text_message_rendered.get_width() // 2), 328 - (text_message_rendered.get_height() // 2)))
        screen.blit(text_score, (20, 20))  

        pygame.display.flip()

    pygame.quit()

def main():
    selected_level, screen = opening_window()

    if selected_level is None:
        return

    done = False
    x = 50
    y = 170
    clock = pygame.time.Clock()
    timer_duration = 180  # 3 minutes for level 1
    speed = 2
    goal = pygame.Rect(880, 640, 80, 80)
    if selected_level == 2:
        timer_duration = 120  # 2 minutes for level 2
        x = 30
        y = 150
        speed = 2
        goal = pygame.Rect(920, 680, 40, 40)
    elif selected_level == 3:
        timer_duration = 60   # 1 minute for level 3
        x = 20
        y = 140
        speed = 0.5
        goal = pygame.Rect(940, 700, 20, 20)
    timer_start = time.time()
    maze = Labyrinth(selected_level)
    victory = False
    pause = False
    pause_time = 0  # Time spent in pause menu
    pause_time_start = 0  # Initialize pause time start
    game_over_time = 0  # Initialize the time when the game is over
    lives = 5  # Player lives

    # Initial distance between start and end point
    initial_distance = abs(x - goal.left) + abs(y - goal.top)

    # Create an empty path
    path = []

    # Open path.txt file in append mode
    with open('path.txt', 'a') as file:
        file.write("Starting path\n")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_p:
                    pause = not pause
                    if pause:
                        pause_time_start = time.time()  # Update pause time start
                    else:
                        pause_time += time.time() - pause_time_start

        if not victory and not pause:
            move_up = True
            move_down = True
            move_left = True
            move_right = True
            pressed = pygame.key.get_pressed()

            # Movement
            if pressed[pygame.K_u] or pressed[pygame.K_UP]:
                for m in maze.maze_walls:
                    player = pygame.Rect(x, y - speed, 10, 10)
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_up = False
                        break
                if move_up:
                    y -= speed
                    path.append('U')

            if pressed[pygame.K_d] or pressed[pygame.K_DOWN]:
                player = pygame.Rect(x, y + speed, 10, 10)
                for m in maze.maze_walls:
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_down = False
                        break
                if move_down:
                    y += speed
                    path.append('D')

            if pressed[pygame.K_l] or pressed[pygame.K_LEFT]:
                player = pygame.Rect(x - speed, y, 10, 10)
                for m in maze.maze_walls:
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_left = False
                        break
                if move_left:
                    x -= speed
                    path.append('L')

            if pressed[pygame.K_r] or pressed[pygame.K_RIGHT]:
                player = pygame.Rect(x + speed, y, 10, 10)
                for m in maze.maze_walls:
                    if player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])):
                        move_right = False
                        break
                if move_right:
                    x += speed
                    path.append('R')

            # Checks if player has reached the goal
            if goal.colliderect((x, y, 10, 10)):
                victory = True
                game_over_time = time.time()  # Update game over time

            # Checks if player collides with any red cell within a rectangle of 1 units around the player's position
            player_rect = pygame.Rect(x - 1, y - 1, 3, 3)
            for cell in maze.obstacle:
                for wall in cell.walls:
                    if player_rect.colliderect(pygame.Rect(wall[0], wall[1], wall[2], wall[3])):
                        lives -= 1
                        x = 50
                        y = 170
                        if selected_level == 2:
                            x = 30
                            y = 150
                        elif selected_level == 3:
                            x = 20
                            y = 140
                        if lives == 0:
                            # Save the path to file before exiting
                            with open('path.txt', 'a') as file:
                                file.write(''.join(path))
                            return ending_screen(0, False)

            # Draws the screen
            maze.draw(goal, screen, x, y)
            text_time = draw_time(timer_start, timer_duration)
            # Calculate score
            current_distance = abs(x - goal.left) + abs(y - goal.top)
            distance = initial_distance - current_distance
            elapsed_time = time.time() - timer_start - pause_time
            score_value = distance / elapsed_time
            score_text = font1.render("Score: {0}".format(int(max(0, score_value))), True, (255, 255, 255))
            lives_text = font1.render("Lives: {0}".format(lives), True, (255, 255, 255))
            pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x, y, 10, 10))
            screen.blit(text_time, (700, 15))
            screen.blit(score_text, (20, 15))  # Changed position to top left corner
            screen.blit(lives_text, (20, 60))  # Changed position to top left corner
            pygame.display.flip()

            # Check if time's up
            if time.time() - timer_start - pause_time >= timer_duration:
                # Save the path to file before exiting
                with open('path.txt', 'a') as file:
                    file.write(''.join(path))
                return ending_screen(score_value, False)

        elif victory:
            # Save the path to file before exiting
            with open('path.txt', 'a') as file:
                file.write(''.join(path))
            return ending_screen(score_value, selected_level, True)

        else:
            # Save the path to file before exiting
            with open('path.txt', 'a') as file:
                file.write(''.join(path))
            return ending_screen(score_value, False)
        clock.tick(60)



if __name__ == '__main__':
    main()

