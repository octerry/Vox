import pygame
import math

class Main:
    def __init__(self, screen):
        # Ca tourne
        self.isRunning = True

        # Taille de la fenetre
        self.screen = screen

        # Titre de la fenetre
        pygame.display.set_caption("Vox Test")

        self.clock = pygame.time.Clock()

        self.firstRun = True

        self.lightningImage = None
        self.gradientSurface = None
        self.gradientBounds = None

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##Si le joueur appuie sur la croix de la fenetre
                self.isRunning = False ##Le jeu s'arrete

    # def update(self):
    #     # actualiser ce qui doit être actualisé

    def display(self):
        # Fond bleu uni
        self.screen.fill((16, 97, 148))


        # ECLAIR SUR SON FRONT
        if (self.firstRun):
            rectWidth = self.ur(180, x=True)
            rectHeight = self.ur(800, y=True)
            self.image = pygame.Surface((rectWidth*2,rectHeight*2), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (33, 141, 191), (0, 0, rectWidth, rectHeight))
            pygame.draw.rect(self.image, (33, 141, 191), (rectWidth, rectHeight-rectWidth, rectWidth, rectHeight))
        toShow = pygame.transform.rotate(self.image, -40)
        self.screen.blit(toShow, (self.ur(-410, y=True), self.ur(-350, y=True)))


        # DEGRADE CIRCULAIRE
        if (self.firstRun):
            self.gradientBounds = int(2 * self.screen.get_height())
            self.gradientSurface = pygame.Surface((self.gradientBounds, self.gradientBounds), pygame.SRCALPHA)
            center = [self.gradientBounds/2, self.gradientBounds/2]
            for x in range(self.gradientBounds):
                for y in range(self.gradientBounds):
                    ## √( (Px-Cx)² + (Py-Cy)² )
                    m = math.sqrt( ( x - center[0] )**2 + ( y - center[1])**2 ) ## Distance du centre

                    opacityPercentage = ( 1 - ( m / (self.gradientBounds/2) ) ) * 1.5
                    if opacityPercentage < 0: opacityPercentage = 0
                    if opacityPercentage > 1: opacityPercentage = 1
                    opacity =  opacityPercentage * 255

                    self.gradientSurface.set_at((x, y), (74, 158, 189, opacity))
        self.screen.blit(self.gradientSurface, (self.screen.get_width()/2 - self.gradientBounds/2, self.screen.get_height()/2 - self.gradientBounds/2))

        # CONTOUR ROUGE
        pygame.draw.rect(self.screen, (214, 28, 41), (0, 0, self.screen.get_width(), self.screen.get_height()), int(self.ur(10, y=True)))

        # Afficher les changements
        pygame.display.flip()

    def run(self):
        while self.isRunning :
            self.handling_events()
            # self.update()
            self.display()

            self.clock.tick(30)
            self.firstRun = False

    def ur(self, value, x=False, y=False):
        ''' Universal Ratio from 1920 x 1080 to screen size '''
        if x:
            currentValue = value if not y else value[0] ## Au cas où si c'est une liste
            finalValue = (currentValue/1920) * self.screen.get_width()
            if not y : return finalValue
            else : second = finalValue;
        if y:
            currentValue = value if not x else value[1] ## Au cas où si c'est une liste
            finalValue = (currentValue/1080) * self.screen.get_height()
            return finalValue if not x else (finalValue, second)

pygame.init()

# à la fin faudra mettre (0,0) pour le fullscreen
# c'est en 16:9
screen = pygame.display.set_mode((800, 450))
instance = Main(screen)
instance.run()

pygame.quit()