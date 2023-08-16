
# ///////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////
# /////////////////////// B T M 2 6 0 - F I N A L ///////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////
# //////////////// K A L E B - S V I T L A N A - L O U R D E S //////////////////////
# ///////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////




import pygame, sys, threading

from button import Button
from pygame import mixer
from fighter import Fighter

# Initialize pygame
pygame.init()

# Set screen size and menu display
SCREEN = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/images/background/menu_bg.jpeg")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/buttons/font.ttf", size)

#######################################
########## Function for PLAY ##########
#######################################
def play():
    while True:       

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        # Menu screen disappears and moves onto game
        SCREEN.fill("black")
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

        mixer.init()
        pygame.init()

        # Create the game/screen window ---- should be identical with menu display on line 23
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 600
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brawler")

        # Set the framerate
        clock = pygame.time.Clock()
        FPS = 60

        # Define colors used for Health Bar and Fonts
        RED = (255, 0, 0)
        ORANGE = (255, 165, 0)
        WHITE = (255, 255, 255)

        # Define game variables
        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]#player scores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000

        # Define fighter variables
        WARRIOR_SIZE = 162
        WARRIOR_SCALE = 5
        WARRIOR_OFFSET = [72, 56]
        WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
        WIZARD_SIZE = 250
        WIZARD_SCALE = 3
        WIZARD_OFFSET = [112, 107]
        WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

        # Load music and sounds
        pygame.mixer.music.load("assets/audio/alexander-nakarada-chase.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        # Load background image
        bg_image = pygame.image.load("assets/images/background/level-1.gif").convert_alpha()

        # Load spritesheets
        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        # Load victory image
        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        # Define number of steps in each animation
        WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        # Define fonts
        count_font = pygame.font.Font("assets/fonts/Hare-.otf", 80)
        score_font = pygame.font.Font("assets/fonts/Hare-.otf", 30)

        # Function for drawing text
        def draw_text(text, font, text_col, x, y):
          img = font.render(text, True, text_col)
          screen.blit(img, (x, y))

        # Function for drawing background
        def draw_bg():
          scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
          screen.blit(scaled_bg, (0, 0))

        # Function for drawing fighter health bars
        def draw_health_bar(health, x, y):
          ratio = health / 100
          pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
          pygame.draw.rect(screen, RED, (x, y, 400, 30))
          pygame.draw.rect(screen, ORANGE, (x, y, 400 * ratio, 30))

        # Create two instances of fighters
        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        # Game Loop
        run = True
        while run:
          clock.tick(FPS)

          # Draw background
          draw_bg()

          # Show player stats
          draw_health_bar(fighter_1.health, 20, 20)
          draw_health_bar(fighter_2.health, 580, 20)
          draw_text("WARRIOR: " + str(score[0]), score_font, RED, 20, 60)
          draw_text("WIZARD: " + str(score[1]), score_font, RED, 580, 60)

          # Update countdown
          if intro_count <= 0:
            # Move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
          else:
            # Display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            # Update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
              intro_count -= 1
              last_count_update = pygame.time.get_ticks()

          # Update fighters
          fighter_1.update()
          fighter_2.update()

          # Draw fighters
          fighter_1.draw(screen)
          fighter_2.draw(screen)

          # Check for player defeat
          if round_over == False:
            if fighter_1.alive == False:
              score[1] += 1
              round_over = True
              round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
              score[0] += 1
              round_over = True
              round_over_time = pygame.time.get_ticks()
          else:
            # Display VICTORY image
            screen.blit(victory_img, (300, 250))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
              round_over = False
              intro_count = 3
              fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
              fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

          # Event handler
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False


          # Update display
          pygame.display.update()

        # Exit pygame
        pygame.quit()


#######################################
######## Function for CONTROL #########
#######################################

def control():
    while True:
        CONTROL_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        CONTROL_SCREEN = pygame.image.load("assets/images/icons/controls.png")
        CONTROL_RECT = CONTROL_SCREEN.get_rect(center=(500, 260))
        SCREEN.blit(CONTROL_SCREEN, CONTROL_RECT)

        CONTROL_BACK = Button(image=None, pos=(500, 460), 
        text_input="BACK", font=get_font(40), base_color="white", hovering_color="red")

        CONTROL_BACK.changeColor(CONTROL_MOUSE_POS)
        CONTROL_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTROL_BACK.checkForInput(CONTROL_MOUSE_POS):
                    main_menu()

        pygame.display.update()


#######################################
######### M A I N - M E N U  ##########
#######################################

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TITLE = pygame.image.load("assets/images/icons/title.png").convert_alpha()
        MENU_RECT = MENU_TITLE.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/buttons/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        CONTROL_BUTTON = Button(image=pygame.image.load("assets/buttons/Options Rect.png"), pos=(500, 400), 
                            text_input="CONTROL", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/buttons/Quit Rect.png"), pos=(500, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TITLE, MENU_RECT)

        for button in [PLAY_BUTTON, CONTROL_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if CONTROL_BUTTON.checkForInput(MENU_MOUSE_POS):
                    control()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()



