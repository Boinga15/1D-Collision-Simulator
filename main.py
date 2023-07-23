import pygame
import time
import copy

from actors import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([1200, 600])

pygame.display.set_caption("1D Collision Simulator")

# Simulation Class
class Simulation():
    def __init__(self):  # Initilisation
        self.objectFont = pygame.font.SysFont('Arial Black', 12)
        self.statFont = pygame.font.SysFont('Arial Black', 20)
        self.consoleFont = pygame.font.SysFont('Arial Black', 40)

        self.settingStatistics = False

        self.simulationPaused = True

        self.startingObjects = [Object(200, 50, 1, 1), Object(1000, 50, 1, -1)]
        self.objects = [Object(200, 50, 1, 1), Object(1000, 50, 1, -1)]

        self.walls = True
        self.textStatistics = True
        self.coefficientOfRestitution = 1
        
        self.collisionCount = 0
        self.timeElapsed = 0

        # Input
        self.pressedSpace = False
        self.leftClicked = False

    def clearConsole(self):
        for i in range(0, 10):
            print("\n" * 6)

    def input(self):  # Input
        keys = pygame.key.get_pressed()

        # Mouse Input
        mouseInp = pygame.mouse.get_pressed()
        if mouseInp[0] and not self.leftClicked:
            mouseX, mouseY = pygame.mouse.get_pos()

            for object in self.objects:
                collisionBox = pygame.Rect(object.x, 550 - object.size, object.size, object.size)
                
                if collisionBox.collidepoint(mouseX, mouseY):
                    optionsDone = False
                    self.simulationPaused = True
                    self.settingStatistics = True

                    screen.blit(self.consoleFont.render("Check the console.", False, (0, 200, 0)), (380, 220))
                    pygame.display.flip()

                    # Options Menu #2 - Box Settings
                    self.clearConsole()
                    while not optionsDone:
                        print("Select an option:")
                        print("1: Change object size (size = " + str(object.size) + "m wide and high).")
                        print("2: Change object x location (x location = " + str(object.x) + ").")
                        print("3: Change object mass (mass = " + str(object.mass) + "kg).")
                        print("4: Change object velocity (velocity = " + str(object.velocity) + "ms^-1) [Positive values indicate movement right].")
                        print("5: Remove object.")
                        print("6: Finish.")
                        op = input("> ")
                        self.clearConsole()

                        try:
                            op = int(op)
                            if not 0 < op < 7:
                                print("Error: Invalid value. Try again.\n")
                                continue

                            match op:
                                case 1:
                                    print("Enter a new value for the size of the object (must be a value above 0).")
                                    try:
                                        choice = float(input("> "))
                                        self.clearConsole()
                                        if choice > 0.0:
                                            object.size = choice
                                        else:
                                            print("Error: Invalid value.\n")
                                        
                                    except ValueError:
                                        self.clearConsole()
                                        print("Error: Invalid value.\n")
                                    
                                case 2:
                                    print("Enter a new value for the x location of the object.")
                                    try:
                                        choice = float(input("> "))
                                        self.clearConsole()
                                        object.x = choice
                                        
                                    except ValueError:
                                        self.clearConsole()
                                        print("Error: Invalid value.\n")
                                    
                                case 3:
                                    print("Enter a new value for the mass of the object (must be a value above 0).")
                                    try:
                                        choice = float(input("> "))
                                        self.clearConsole()
                                        if choice > 0.0:
                                            object.mass = choice
                                        else:
                                            print("Error: Invalid value.\n")
                                        
                                    except ValueError:
                                        self.clearConsole()
                                        print("Error: Invalid value.\n")
                                case 4:
                                    print("Enter a new value for the velocity of the object (positive values will make the object move right).")
                                    try:
                                        choice = float(input("> "))
                                        self.clearConsole()
                                        object.velocity = choice
                                        
                                    except ValueError:
                                        self.clearConsole()
                                        print("Error: Invalid value.\n")
                                case 5:
                                    self.objects.remove(object)
                                    optionsDone = True
                                case 6:
                                    optionsDone = True
                        
                        except ValueError:
                            print("Error: Invalid value. Try again.\n")
                    
                    if self.timeElapsed <= 0:
                        self.startingObjects = copy.deepcopy(self.objects)
                    break

        elif self.leftClicked and not mouseInp[0]:
            self.leftClicked = False
        
        # Pausing the simulation
        if keys[pygame.K_SPACE] and not self.pressedSpace:
            self.pressedSpace = True
            self.simulationPaused = not self.simulationPaused

        elif self.pressedSpace and not keys[pygame.K_SPACE]:
            self.pressedSpace = False
        
        # Resetting the simulation
        if keys[pygame.K_r]:
            self.objects = copy.deepcopy(self.startingObjects)
            self.collisionCount = 0
            self.timeElapsed = 0
        
        if keys[pygame.K_p]:
            screen.blit(self.consoleFont.render("Check the console.", False, (0, 200, 0)), (380, 220))
            pygame.display.flip()

            self.simulationPaused = True
            self.settingStatistics = True

            # Options Menu #1 - General Settings

            optionsDone = False
            
            self.clearConsole()
            while not optionsDone:
                print("Select an option:")
                print("1: Set coefficient of restitution (epsillon = " + str(self.coefficientOfRestitution) + ").")
                print("2: Set the wall's presence (walls: " + ("active" if self.walls else "not active") + ").")
                print("3: Add a new object.")
                print("4: Set the statistic text's state (statistic text: " + ("enabled" if self.textStatistics else "disabled") + ").")
                print("5: Finish.")
                op = input("> ")
                self.clearConsole()

                try:
                    op = int(op)
                    if not 0 < op < 6:
                        print("Error: Invalid value. Try again.\n")
                        continue

                    match op:
                        case 1:
                            print("Enter a new value for the coefficient of restitution (from 0 to 1).")
                            try:
                                choice = float(input("> "))
                                self.clearConsole()
                                if 0.0 <= choice <= 1.0:
                                    self.coefficientOfRestitution = choice
                                else:
                                    print("Error: Invalid value.\n")
                                
                            except ValueError:
                                self.clearConsole()
                                print("Error: Invalid value.\n")
                            
                        case 2:
                            print("Enter whether or not you want walls to be active (yes to activate them).")
                            choice = input("> ")
                            self.clearConsole()
                            if choice.lower() == "yes":
                                self.walls = True
                            else:
                                self.walls = False
                            
                        case 3:
                            print("Enter the x position of the new object.")
                            try:
                                choice = float(input("> "))
                                self.clearConsole()
                                
                                if self.timeElapsed <= 0:
                                    self.startingObjects.append(Object(choice, 50, 1, 0))
                                
                                self.objects.append(Object(choice, 50, 1, 0))
                                
                            except ValueError:
                                self.clearConsole()
                                print("Error: Invalid value.\n")
                        case 4:
                            print("Enter whether or not you want to text statistics to be active (yes to activate them).")
                            choice = input("> ")
                            self.clearConsole()
                            if choice.lower() == "yes":
                                self.textStatistics = True
                            else:
                                self.textStatistics = False
                            
                        case 5:
                            optionsDone = True
                
                except ValueError:
                    print("Error: Invalid value. Try again.\n")

    def logic(self):  # Handling Logic

        # Handle Object Movement
        if not self.simulationPaused:
            self.timeElapsed += 1

            for object in self.objects:
                object.x += object.velocity

                # Collisions
                for object2 in self.objects:
                    if object2 == object or object2 == object.collidedWith:
                        pass
                    else:
                        collisionBox1 = pygame.Rect(object.x, 550 - object.size, object.size, object.size)
                        collisionBox2 = pygame.Rect(object2.x, 550 - object2.size, object2.size, object2.size)

                        if collisionBox1.colliderect(collisionBox2):
                            object.collidedWith = object2
                            object2.collidedWith = object

                            object.forgetTimer = 3
                            object2.forgetTimer = 3

                            object.collisions += 1
                            object2.collisions += 1

                            self.collisionCount += 1

                            # Collision Mathematics
                            v1 = copy.deepcopy(object.velocity)
                            v2 = copy.deepcopy(object2.velocity)

                            m1 = copy.deepcopy(object.mass)
                            m2 = copy.deepcopy(object2.mass)

                            # Calculation #1: First Fraction
                            fp1 = v1 * ((m1 - self.coefficientOfRestitution * m2)/(m1 + m2))
                            fp2 = v2 * ((m2 - self.coefficientOfRestitution * m1)/(m1 + m2))

                            # Calculation #2: Second Fraction
                            fs1 = v2 * (((1 + self.coefficientOfRestitution) * m2)/(m1 + m2))
                            fs2 = v1 * (((1 + self.coefficientOfRestitution) * m1)/(m1 + m2))
                            
                            # Final Step
                            object.velocity = fp1 + fs1
                            object2.velocity = fp2 + fs2

                # Wall Collision
                if self.walls:
                    if (object.x) <= 10 or (object.x + object.size) >= 1190:
                        self.collisionCount += 1
                        object.velocity *= (-1 * self.coefficientOfRestitution)
                        object.collidedWith = object
                        object.collisions += 1
            
            object.forgetTimer -= 1
            if object.forgetTimer <= 0:
                object.collidedWith = object


    def draw(self):  # Draw Function
        global screen

        screen.fill((255, 255, 255)) # Clear Screen

        # Floor
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 550, 1200, 30))

        # Walls
        if self.walls:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, -20, 10, 700))
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(1190, -20, 10, 700))

        # Objects
        for object in self.objects:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(object.x, 550 - object.size, object.size, object.size))
            if self.textStatistics:
                line = self.objectFont.render("Collisions: " + str(object.collisions), False, (0, 0, 0))
                line_rect = line.get_rect(center = (object.x + (object.size / 2), 535 - object.size))
                screen.blit(line, line_rect)

                line = self.objectFont.render("Velocity: " + str(round(object.velocity, 3)), False, (0, 0, 0))
                line_rect = line.get_rect(center = (object.x + (object.size / 2), 520 - object.size))
                screen.blit(line, line_rect)

                line = self.objectFont.render("Position: " + str(round(object.x, 3)), False, (0, 0, 0))
                line_rect = line.get_rect(center = (object.x + (object.size / 2), 505 - object.size))
                screen.blit(line, line_rect)

        # Text
        screen.blit(self.statFont.render("Simulation Paused" if self.simulationPaused else "Simulation Running", False, (255, 0, 0) if self.simulationPaused else (0, 200, 0)), (30, 10))
        screen.blit(self.statFont.render("Collisions: " + str(self.collisionCount), False, (0, 0, 0)), (30, 30))

        pygame.display.flip()

simulation = Simulation()

gameRunning = True
while gameRunning:
    ev = pygame.event.get()

    simulation.input()

    for event in ev:
        if event.type == pygame.QUIT:
            gameRunning = False
    
    simulation.logic()

    simulation.draw()

    time.sleep(0.01)

pygame.quit()
