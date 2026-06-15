import pygame, math
from pyvidplayer import Video
from enum import Enum


class voxState(Enum):
    BLAZED = 0
    FULLSCREENHYPNOSE = 1
    MIKUVIDEO = 2

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

        self.joysticks = []
        self.eyeShiftRatioX = 0
        self.eyeShiftRatioY = 0

        self.currentState = voxState.BLAZED

        self.hypnoseShiftRatio = 0

        self.importSprites()
        self.importHatsuneMikuVideo()

    def importSprites(self):
        # SPRITES DES YEUX
        ## Oeuil Gauche Fond
        self.leftEyeImage = pygame.image.load("source/vox_blazed_lefteye_bg.svg").convert_alpha()
        self.leftEyeImage = pygame.transform.scale(self.leftEyeImage, self.ur([711, 223], x=True, y=True))
        self.leftEyeMask = pygame.image.load("source/vox_blazed_lefteye_mask.svg").convert_alpha()
        self.leftEyeMask = pygame.transform.scale(self.leftEyeMask, self.ur([711, 223], x=True, y=True))

        ## Oeuil Gauche Contour
        self.leftEyeBorder = pygame.image.load("source/vox_blazed_lefteye_border.svg").convert_alpha()
        self.leftEyeBorder = pygame.transform.scale(self.leftEyeBorder, self.ur([711, 223], x=True, y=True))

        ## Sourcil Droit
        self.leftEyebrow = pygame.image.load("source/vox_blazed_lefteyebrow.svg").convert_alpha()
        self.leftEyebrow = pygame.transform.scale(self.leftEyebrow, self.ur([719, 219], x=True, y=True))

        ## Oeuil Droit Fond
        self.rightEyeImage = pygame.image.load("source/vox_blazed_righteye_bg.svg").convert_alpha()
        self.rightEyeImage = pygame.transform.scale(self.rightEyeImage, self.ur([734, 253], x=True, y=True))
        self.rightEyeMask = pygame.image.load("source/vox_blazed_righteye_mask.svg").convert_alpha()
        self.rightEyeMask = pygame.transform.scale(self.rightEyeMask, self.ur([734, 253], x=True, y=True))

        ## Oeuil Droit Contour
        self.rightEyeBorder = pygame.image.load("source/vox_blazed_righteye_border.svg").convert_alpha()
        self.rightEyeBorder = pygame.transform.scale(self.rightEyeBorder, self.ur([734, 253], x=True, y=True))

        ## Sourcil Droit
        self.rightEyebrow = pygame.image.load("source/vox_blazed_righteyebrow.svg").convert_alpha()
        self.rightEyebrow = pygame.transform.scale(self.rightEyebrow, self.ur([735, 266], x=True, y=True))

        ## Pupille
        self.pupilImage = pygame.image.load("source/vox_pupil.svg").convert_alpha()
        self.pupilImage = pygame.transform.scale(self.pupilImage, self.ur([61, 91], x=True, y=True))

        ## Bouche
        self.mouthImage = pygame.image.load("source/vox_blazed_mouth.svg").convert_alpha()
        self.mouthImage = pygame.transform.scale(self.mouthImage, self.ur([478, 224], x=True, y=True))

        ## Eclair d'hypnose
        self.hypnosisPupil = pygame.image.load("source/vox_hypnosis_lightning.svg").convert_alpha()
        self.hypnosisPupil = pygame.transform.scale(self.hypnosisPupil, self.ur([215, 390], x=True, y=True))

    def importHatsuneMikuVideo(self):
        self.hatsuneVideo = Video("source/hatsuneMiku.mp4")
        self.hatsuneVideo.set_size((self.screen.get_width(), self.screen.get_height()))
        self.hatsuneVideo.pause()

    def handling_events(self):
        for event in pygame.event.get():
            ##Si le joueur appuie sur la croix de la fenetre
            if event.type == pygame.QUIT:
                self.isRunning = False ##Le jeu s'arrete

            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks.append(joy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and self.currentState != voxState.BLAZED: ## 1
                    self.currentState = voxState.BLAZED
                    self.hatsuneVideo.pause()
                if event.key == pygame.K_2 and self.currentState != voxState.FULLSCREENHYPNOSE: ## 1
                    self.currentState = voxState.FULLSCREENHYPNOSE
                    self.hatsuneVideo.pause()
                if event.key == pygame.K_3 and self.currentState != voxState.MIKUVIDEO: ## 1
                    self.currentState = voxState.MIKUVIDEO
                    self.hatsuneVideo.resume()

    def update(self):
        for joystick in self.joysticks:
            self.eyeShiftRatioX = joystick.get_axis(0)
            self.eyeShiftRatioY = joystick.get_axis(1)

    def display(self):
        # LE FOND
        self.showBackground()


        ## LES VISAGES
        if self.currentState == voxState.BLAZED:
            self.showBlazedFace()
        elif self.currentState == voxState.FULLSCREENHYPNOSE:
            self.showHypnoticFace()
        elif self.currentState == voxState.MIKUVIDEO:
            self.showHatsuneMiku()

        # CONTOUR ROUGE
        pygame.draw.rect(self.screen, (214, 28, 41), (0, 0, self.screen.get_width(), self.screen.get_height()), int(self.ur(10, y=True)))


        # # Afficher les FPS
        # self.font = pygame.font.Font("source/inter.ttf", 32)
        # self.fpsText = self.font.render(str(int(self.clock.get_fps())) + " FPS", True, (255, 255, 255))
        #
        # self.screen.blit(self.fpsText, self.fpsText.get_rect())

        # Afficher les changements
        pygame.display.update()

    def showBackground(self):
        # --- FOND BLEU UNI ---
        self.screen.fill((16, 97, 148))

        # --- ECLAIR SUR SON FRONT ---
        if (self.firstRun):
            rectWidth = self.ur(180, x=True)
            rectHeight = self.ur(800, y=True)
            self.image = pygame.Surface((rectWidth*2,rectHeight*2), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (33, 141, 191), (0, 0, rectWidth, rectHeight))
            pygame.draw.rect(self.image, (33, 141, 191), (rectWidth, rectHeight-rectWidth, rectWidth, rectHeight))
        toShow = pygame.transform.rotate(self.image, -40)
        self.screen.blit(toShow, (self.ur(-410, y=True), self.ur(-350, y=True)))

        # --- DEGRADE CIRCULAIRE ---
        if (self.firstRun):
            self.gradientBounds = int(2 * self.screen.get_height())
            self.gradientSurface = pygame.Surface((self.gradientBounds, self.gradientBounds), pygame.SRCALPHA)
            center = [self.gradientBounds/2, self.gradientBounds/2]
            for radius in range(self.gradientBounds // 2, 0, -1):
                opacity = 255 * (1 - radius / (self.gradientBounds // 2))
                color = (74, 158, 189, int(opacity))
                pygame.draw.circle(self.gradientSurface, color, center, radius)
        self.screen.blit(self.gradientSurface, (self.screen.get_width()/2 - self.gradientBounds/2, self.screen.get_height()/2 - self.gradientBounds/2))

    def showBlazedFace(self):
        # LEFT EYE
        pupilPosition = [self.leftEyeImage.get_width() / 2, self.leftEyeImage.get_height()/2 - self.pupilImage.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.leftEyeImage.get_width() / 2)
        pupilPosition[1] += self.eyeShiftRatioY * (self.leftEyeImage.get_height() / 2)

        faceDisplacement = self.eyeShiftRatioY * self.ur(80, y=True)

        finalPupilImage = pygame.transform.rotate(self.pupilImage, self.eyeShiftRatioX * 20)

        self.leftEyeImage.fill((255, 0, 66))
        self.leftEyeImage.blit(finalPupilImage, pupilPosition)
        self.leftEyeImage.blit(self.leftEyeBorder, (0,0))


        result = self.leftEyeMask.copy()
        result.blit(self.leftEyeImage, (0,0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([111, 409], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        # RIGHT EYEBROW
        position = self.ur([120, 140], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.leftEyebrow, position)


        # RIGHT EYE
        pupilPosition = [self.rightEyeImage.get_width() / 2 - self.pupilImage.get_width(), self.rightEyeImage.get_height()/2 - self.pupilImage.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.rightEyeImage.get_width() / 2)
        pupilPosition[1] += self.eyeShiftRatioY * (self.rightEyeImage.get_height() / 2)

        self.rightEyeImage.fill((255, 0, 66))
        self.rightEyeImage.blit(finalPupilImage, pupilPosition)
        self.rightEyeImage.blit(self.rightEyeBorder, (0, 0))

        result = self.rightEyeMask.copy()
        result.blit(self.rightEyeImage, (0,0), None, pygame.BLEND_MULT)

        position = [self.screen.get_width() - self.ur(151, x=True) - self.rightEyeImage.get_width(), self.ur(375, y=True)]
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        # RIGHT EYEBROW
        position = [self.screen.get_width() - self.rightEyebrow.get_width() - self.ur(184, x=True), self.ur(99, y=True)]
        position[1] += faceDisplacement
        self.screen.blit(self.rightEyebrow, position)


        # MOUTH
        position = [0,0]
        position[0] = self.ur(658, x=True)
        position[1] = self.screen.get_height() - self.ur(101, x=True) - self.mouthImage.get_height() + faceDisplacement
        self.screen.blit(self.mouthImage, position)

    def showHypnoticFace(self):
        self.screen.fill((255, 0, 66))
        self.hypnoseShiftRatio += .005
        if self.hypnoseShiftRatio > 1: self.hypnoseShiftRatio = 0

        for i in range (5):
            shift = self.hypnoseShiftRatio + ( i*.2 )
            if shift > 1: shift -= 1
            shift = math.exp(shift) - 1

            radiusShift = shift * self.screen.get_width()/2
            widthShift = math.ceil(shift * self.ur(20, y=True))

            pygame.draw.circle(self.screen, [0,0,0], (self.screen.get_width()/2, self.screen.get_height()/2), radiusShift, widthShift)

        self.screen.blit(self.hypnosisPupil, (self.screen.get_width()/2 - self.hypnosisPupil.get_width()/2, self.screen.get_height()/2 - self.hypnosisPupil.get_height()/2))

    def showHatsuneMiku(self):
        self.hatsuneVideo.draw(self.screen, (0,0))
        pygame.display.flip()

    def run(self):
        while self.isRunning :
            self.handling_events()
            self.update()
            self.display()

            self.clock.tick(60)
            # print(self.clock.get_fps())
            self.firstRun = False

    def ur(self, value, x=False, y=False):
        if self.screen.get_width() != 1920:
            ''' Universal Ratio from 1920 x 1080 to screen size '''
            if x:
                currentValue = value if not y else value[0] ## Au cas où si c'est une liste
                finalValue = (currentValue/1920) * self.screen.get_width()
                if not y : return finalValue
                else : second = finalValue;
            if y:
                currentValue = value if not x else value[1] ## Au cas où si c'est une liste
                finalValue = (currentValue/1080) * self.screen.get_height()
                return finalValue if not x else [second, finalValue]
        else : return value

pygame.init()

# à la fin faudra mettre (0,0) pour le fullscreen
# c'est en 16:9
screen = pygame.display.set_mode((800, 450))
# screen = pygame.display.set_mode((1920, 1080))
# screen = pygame.display.set_mode((0, 0))
instance = Main(screen)
instance.run()

pygame.quit()