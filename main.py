import pygame
from tkinter import Tk
from tkinter import messagebox
import ast
import os

from car import Car


def getSelectedCar(event):
    for car in Car.cars:
        rect = car.rect
        if rect.collidepoint(event.pos):
            mouse_x, mouse_y = event.pos
            offset_x = rect.x - mouse_x
            offset_y = rect.y - mouse_y
            return (car, offset_x, offset_y)
 

Tk().wm_withdraw()
pygame.init()


window_size = (600, 800)


screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Unblock Red Car')

background = pygame.image.load(os.path.join('images', 'pitch.png'))
background = pygame.transform.scale(background, window_size)

BUTTONS1 = pygame.image.load("images/restart.png") 
BUTTONS2 = pygame.image.load("images/exit.png")


draging_car = None

class Button:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=pygame.transform.scale(img,(70,70))
        self.draw()
        self.rect=self.img.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
    def draw(self):
        screen.blit(self.img,(self.x,self.y))

    def check_click(self):
        mouse_pos=pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if left_click and self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

def load_stage(stage):
    cars = []
    for x, y, width, height in stages[stage]:
        car = Car(x*2, y*2, width*2, height*2)
        cars.append(car)
    

stages = ast.literal_eval(open('stages.json').read())
last_stage = open('Level').read()

load_stage(last_stage)

run=True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.check_click():
                # Restart button is clicked, reload level
                Car.cars.clear()
                load_stage(last_stage)

            if end_button.check_click():
                pygame.quit()

            if event.button == 1:
                SelectedCar = getSelectedCar(event)
                if SelectedCar: 
                    draging_car, offset_x, offset_y = SelectedCar




        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                
                if not draging_car:
                    continue

                rounded_x, rounded_y = draging_car.round()

                # x
                rect_x = draging_car.rect.x
                rect_w = draging_car.rect.width
                if rect_x <= 0: rect_x = 0
                else:
                    if rect_w == 150*2:
                        if rounded_x >= 150*2: rect_x = 150*2
                        else: rect_x = rounded_x
                    elif rect_w == 50*2:
                        if rounded_x >= 250*2: rect_x = 250*2
                        else: rect_x = rounded_x
                    elif rect_w == 100*2:
                        if rounded_x >= 200*2:
                            if draging_car.is_main:
                                if last_stage == str(len(stages) - 1):
                                    messagebox.showinfo('won', 'you won the game.\nGame Over ! Thank you for playing.')
                                    with open('Level', 'w') as Level_file:
                                        Level_file.write('1')
                                        Level_file.close()
                                    pygame.quit()
                                else:
                                    last_stage = str(int(last_stage) + 1)
                                    with open('Level', 'w') as Level_file:
                                        Level_file.write(last_stage)
                                        Level_file.close()
                                    Car.cars.clear()
                                    r = messagebox.askquestion("won","you won the game ! next stage ?")
                                    if r == 'no':
                                        pygame.quit()
                                    elif r == 'yes' and last_stage=='11':
                                        messagebox.showinfo('Won!', 'you won the game. Thank you for playing.')
                                        pygame.quit()
                                    for x, y, width, height in stages[last_stage]:
                                        Car(x*2, y*2, width*2, height*2)
                            else:
                                rect_x = 200*2
                        else: rect_x = rounded_x
                draging_car.rect.x = rect_x


                # y
                rect_y = draging_car.rect.y
                rect_h = draging_car.rect.height
                if rect_y <= 0: rect_y = 0
                else:
                    if rect_h == 150*2:
                        if rounded_y >= 150*2: rect_y = 150*2
                        else: rect_y = rounded_y
                    elif rect_h == 50*2:
                        if rounded_y >= 250*2: rect_y = 250*2
                        else: rect_y = rounded_y
                    elif rect_h == 100*2:
                        if rounded_y >= 200*2: rect_y = 200*2
                        else: rect_y = rounded_y
                draging_car.rect.y = rect_y
 

                draging_car = None





        elif event.type == pygame.MOUSEMOTION:

            if draging_car:
                mouse_x, mouse_y = event.pos
                new_y = mouse_y + offset_y
                new_x = mouse_x + offset_x
                if new_x < 0:
                    new_x = 0
                elif new_x + draging_car.rect.width > 300*2:
                    new_x = window_size[0] - draging_car.rect.width

                if new_y < 0:
                    new_y = 0
                elif new_y + draging_car.rect.height > 300*2:
                    new_y = window_size[1] - draging_car.rect.height

                draging_car.move(new_x, new_y)


        pygame.display.update()

    # set background image (parking asphalt)
    screen.blit(background, background.get_rect())
    
    # put cars in parking
    for car in Car.cars: car.show(screen)
    restart_button = Button(18*2,342*2,BUTTONS1)
    end_button = Button(257*2,342*2,BUTTONS2)
    pygame.display.flip()