import pygame
import random

pygame.init()

v_width = 256
v_height = 144

w_width = 1100
w_height = 650

virtual_screen =  pygame.Surface((v_width, v_height))
window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('Tamapeachy')
clock = pygame.time.Clock()

scale_x = w_width / v_width
scale_y = w_height / v_height

play_btn = pygame.Rect(78, 60, 100, 20)
quit_btn = pygame.Rect(78, 85, 100, 20)
feed_btn = pygame.Rect(10, 120, 60, 18)
play_game_btn = pygame.Rect(98, 120, 60, 18)
sleep_btn = pygame.Rect(186, 120, 60, 18)

pygame.font.init()
font = pygame.font.Font(None, 20)
text_play = font.render('Играть', False, (225, 255, 255))
text_quit = font.render('Выйти', False, (255, 255, 255))
text_feed = font.render('кормить', False, (255, 255, 255))
text_play_game = font.render('играть', False, (255, 255, 255))
text_sleep = font.render('спать', False, (255, 255, 255))
text_hibernation = font.render('поднесите персика к еде', False, (240, 30, 30))

menu_bg = pygame.image.load('menu_tamapeachy.png')

game_bg = pygame.image.load('background_tamapeachy.png')
bed_img = pygame.image.load('bed.png')

peach_idle = pygame.image.load('peach_idle.png')
peach_little_move = pygame.image.load('peach_little_move.png')
peach_eyes_closed = pygame.image.load('peach_blink.png')
peach_sad = pygame.image.load('peach_sad.png')
peach_happy = pygame.image.load('peach_happy.png')
peach_eating = pygame.image.load('peach_chew.png')
peach_hibernation = pygame.image.load('peach_sad_sleeping.png')

food = pygame.image.load('food_tamapeachy.png')

peach_x = 108
peach_y = 65

peach_speed = 0.4

target_x = peach_x
target_y = peach_y

move_timer = 0
blink_timer = 0
idle_timer = 0 
current_peach_sprite = peach_idle
happiness = 50
hunger = 50
energy = 50
stat_timer = 0

is_little_move = False
is_blinking = False
dragging = False
falling = False

food_active = False
food_x = 0
food_y = 0
eating_timer = 0 
is_eating = False

ball_active = False
ball_x = 0
ball_y = 0
ball_vy = 0
ball_timer = 0
gravity = 0.3

going_to_sleep = False
sleeping = False
bed_x = 190
bed_y = 65
sleep_timer = 0 

unwell = False
hibernation = False

state = 'menu'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0] / scale_x
            mouse_y = event.pos[1] / scale_y

            peach_rect = pygame.Rect(peach_x, peach_y, 41, 41)
            if peach_rect.collidepoint(mouse_x, mouse_y) and state == 'game':
                dragging = True
            
            if play_btn.collidepoint(mouse_x, mouse_y) and state == 'menu':
                    state = 'game'
            if quit_btn.collidepoint(mouse_x, mouse_y) and state == 'menu':
                    running = False
            if not going_to_sleep and not sleeping:
                
                if feed_btn.collidepoint(mouse_x, mouse_y) and state == 'game':
                    
                    if not food_active:
                        food_x = random.randint(20, 150)
                        food_y = random.randint(60, 70)
                        food_active = True
    
                if play_game_btn.collidepoint(mouse_x, mouse_y) and state == 'game':
                    
                    if not ball_active:
                        ball_x = random.randint(30, 150)
                        ball_y = random.randint(60, 80)
                        ball_vy = 0
                        ball_timer = 0 
                        ball_active = True

            if sleep_btn.collidepoint(mouse_x, mouse_y) and state == 'game':
                going_to_sleep = True
                sleep_timer = 0
                ball_active = False
                
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            falling = True
            target_x = peach_x
            target_y = random.randint(60, 80)
    
        if event.type == pygame.MOUSEWHEEL:
            pass 

    if state == 'game':
        virtual_screen.blit(game_bg,(0, 0))
        
        if not sleeping and not going_to_sleep:
            if ball_active:
                ball_vy += gravity
                ball_y += ball_vy
                
                if ball_y >= 100:
                    ball_y = 100
                    ball_vy = -ball_vy * 1.0
    
                ball_timer += 1
                if ball_timer >= 300:
                    ball_active = False
                    happiness = min(100, happiness + 20)
    
            if ball_active:
                target_x = ball_x
    
            elif food_active:
                target_x = food_x
                target_y = food_y
                move_timer = 0
    
                if abs(peach_x - food_x) < 10 and abs(peach_y - food_y) < 10:
                    is_eating = True
                    eating_timer = 0
                    food_active = False
                    hunger = min(100, hunger + 30)

        if going_to_sleep:
            target_x = bed_x
            target_y = bed_y

            if abs(peach_x - bed_x) < 5 and abs(peach_y - bed_y) < 5:
                sleeping = True
                going_to_sleep = False

        if sleeping == True:
            target_x = bed_x
            target_y = bed_y
            
            if energy < 100:
                energy += 0.1
            elif energy >= 100:
                sleeping = False


        if not sleeping and not going_to_sleep:
            stat_timer += 1

            if stat_timer >= 300:
                stat_timer = 0
                hunger = max(0, hunger - 2)
                happiness = max(0, happiness - 1)
                energy = max(0, energy - 1)
            
        if hunger <= 10 and hunger > 0 or happiness <= 10 and happiness > 0 or energy <= 10 and energy > 0:
            unwell = True
        else:
            unwell = False

        if hunger == 0 or happiness == 0 or energy == 0:
            hibernation = True
            target_x = bed_x
            target_y = bed_y
            
        else:
            hibernation = False        

        blink_timer += 1
        idle_timer += 1

        if unwell and not sleeping:
            current_peach_sprite = peach_sad

        elif hibernation and not sleeping:
            current_peach_sprite = peach_hibernation

        elif is_eating:
            eating_timer += 1
            current_peach_sprite = peach_eating
            if eating_timer >= 60:
                is_eating = False
                eating_timer = 0

        elif ball_active and not sleeping and not going_to_sleep:
            current_peach_sprite = peach_happy

        elif sleeping:
            current_peach_sprite = peach_eyes_closed
            
        else:
        
            if idle_timer >= 40:
                idle_timer = 0
                is_little_move = not is_little_move
    
            if blink_timer >= 90:
                blink_timer = 0
                is_blinking = True
    
            if is_blinking:
                current_peach_sprite = peach_eyes_closed
                if blink_timer >= 5:
                    is_blinking = False
                    blink_timer = 0
            else:
                if is_little_move:
                    current_peach_sprite = peach_little_move
                else:
                    current_peach_sprite = peach_idle

        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            peach_x = mouse_x / scale_x - 20
            peach_y = mouse_y / scale_y - 20
            target_x = peach_x
            target_y = peach_y

        falling = peach_y < 60
        if falling:
            target_x = peach_x
            target_y = random.randint(60, 80)
            peach_y += 2
            if peach_y >= target_y:
                falling = False
        else:
            move_timer += 1
            if move_timer >= 180:
                move_timer = 0
                target_x = random.randint(30, 200)
                target_y = random.randint(60, 90)
    
            if abs(peach_x - target_x) < peach_speed:
                peach_x = target_x
            if abs(peach_y - target_y) < peach_speed:
                peach_y = target_y
                
            if peach_x < target_x:
                peach_x += peach_speed
            elif peach_x > target_x:
                peach_x -= peach_speed
    
            if peach_y < target_y:
                peach_y += peach_speed
            elif peach_y > target_y:
                peach_y -= peach_speed

        virtual_screen.blit(bed_img, (0, 10))

        virtual_screen.blit(current_peach_sprite, (peach_x, peach_y))

        if food_active:
            virtual_screen.blit(food, (food_x, food_y))

        elif ball_active:
            pygame.draw.circle(virtual_screen, (255, 100, 100), (int(ball_x), int(ball_y)), 6)

        pygame.draw.rect(virtual_screen, (100, 100, 100), (10, 5, 70, 8))
        pygame.draw.rect(virtual_screen, (100, 200, 100), (10, 5, hunger * 0.7, 8))

        pygame.draw.rect(virtual_screen, (100, 100, 100), (93, 5, 70, 8))
        pygame.draw.rect(virtual_screen, (255, 220, 100), (93, 5, happiness * 0.7, 8))

        pygame.draw.rect(virtual_screen, (100, 100, 100), (176, 5, 70, 8))
        pygame.draw.rect(virtual_screen, (100, 150, 255), (176, 5, energy * 0.7, 8))

        pygame.draw.rect(virtual_screen, (100, 180, 100), feed_btn)
        pygame.draw.rect(virtual_screen, (255, 200, 100), play_game_btn)
        pygame.draw.rect(virtual_screen, (100, 150, 200), sleep_btn)

        virtual_screen.blit(text_feed, (feed_btn.x + 3, feed_btn.y + 2))
        virtual_screen.blit(text_play_game, (play_game_btn.x + 8, play_game_btn.y + 2))
        virtual_screen.blit(text_sleep, (sleep_btn.x + 10, sleep_btn.y + 2))

        if hunger == 0:
            virtual_screen.blit(text_hibernation, (10, 20))
            
    if state == 'menu':
        virtual_screen.blit(menu_bg, (0, 0))
        
        pygame.draw.rect(virtual_screen, (160, 220, 100), play_btn)
        pygame.draw.rect(virtual_screen, (200, 100, 100), quit_btn)
    
        virtual_screen.blit(text_play, (play_btn.x + 27, play_btn.y + 3))
        virtual_screen.blit(text_quit, (quit_btn.x + 27, quit_btn.y + 3))


    scaled = pygame.transform.scale(virtual_screen, ((w_width, w_height)))
    window.blit(scaled, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
