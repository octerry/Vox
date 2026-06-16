import pygame, math
from pygame.fastevent import post

from pyvidplayer import Video
from enum import Enum


class voxState(Enum):
    BLAZED = 0
    FULLSCREENHYPNOSE = 1
    MIKUVIDEO = 2
    DEMON = 3
    HATE = 4

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

        self.hateLightningImage = None
        self.hateGradientSurface = None
        self.hateGradientBounds = None

        self.backgroundSetup()

        self.joysticks = []
        self.eyeShiftRatioX = 0
        self.eyeShiftRatioY = 0

        self.mouthShiftRatio = 0

        self.currentState = voxState.BLAZED

        self.hypnoseShiftRatio = 0

        self.importSprites()
        self.importHatsuneMikuVideo()

    def backgroundSetup(self):
        # DEFAULT BG
        ## L'éclair classique
        rectWidth = self.ur(180, x=True)
        rectHeight = self.ur(800, y=True)
        self.lightningImage = pygame.Surface((rectWidth * 2, rectHeight * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.lightningImage, (33, 141, 191), (0, 0, rectWidth, rectHeight))
        pygame.draw.rect(self.lightningImage, (33, 141, 191),(rectWidth, rectHeight - rectWidth, rectWidth, rectHeight))

        ## Le dégradé circulaire classique
        self.gradientBounds = int(2 * self.screen.get_height())
        self.gradientSurface = pygame.Surface((self.gradientBounds, self.gradientBounds), pygame.SRCALPHA)
        center = [self.gradientBounds / 2, self.gradientBounds / 2]
        for radius in range(self.gradientBounds // 2, 0, -1):
            opacity = 255 * (1 - radius / (self.gradientBounds // 2))
            color = (74, 158, 189, int(opacity))
            pygame.draw.circle(self.gradientSurface, color, center, radius)

        ## L'éclair haine
        rectWidth = self.ur(180, x=True)
        rectHeight = self.ur(800, y=True)
        self.hateLightningImage = pygame.Surface((rectWidth * 2, rectHeight * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.hateLightningImage, (16, 16, 16), (0, 0, rectWidth, rectHeight))
        pygame.draw.rect(self.hateLightningImage, (16, 16, 16),(rectWidth, rectHeight - rectWidth, rectWidth, rectHeight))

        ## Le dégradé circulaire haine
        self.hateGradientBounds = int(4 * self.screen.get_height())
        self.hateGradientSurface = pygame.Surface((self.hateGradientBounds, self.hateGradientBounds), pygame.SRCALPHA)
        center = [self.hateGradientBounds / 2, self.hateGradientBounds / 2]
        for radius in range(self.hateGradientBounds // 2, 0, -1):
            if radius / (self.hateGradientBounds/2) <= .8 : opacity = 250
            else :
                opacityPercentage = math.exp( ( radius / (self.hateGradientBounds/2) - .8 ) * 5 ) - 1
                opacity = ( 1 - opacityPercentage ) * 255
                if opacity > 250 : opacity = 250
                if opacity < 0 : opacity = 0
            color = (0, 0, 0, int(opacity))
            pygame.draw.circle(self.hateGradientSurface, color, center, radius)

    def importSprites(self):
        ## Eclair d'hypnose
        self.hypnosisPupil = pygame.image.load("source/vox_hypnosis_lightning.svg").convert_alpha()
        self.hypnosisPupil = pygame.transform.scale(self.hypnosisPupil, self.ur([215, 390], x=True, y=True))

        self.importBlazedSprites()
        self.importDemonSprites()
        self.importHateSprites()

    def importBlazedSprites(self):
        # SPRITES DES YEUX
        ## Oeuil Gauche Fond
        self.blazedLeftEyeImage = pygame.image.load("source/vox_blazed_lefteye_bg.svg").convert_alpha()
        self.blazedLeftEyeImage = pygame.transform.scale(self.blazedLeftEyeImage, self.ur([711, 223], x=True, y=True))
        self.blazedLeftEyeMask = pygame.image.load("source/vox_blazed_lefteye_mask.svg").convert_alpha()
        self.blazedLeftEyeMask = pygame.transform.scale(self.blazedLeftEyeMask, self.ur([711, 223], x=True, y=True))

        ## Oeuil Gauche Contour
        self.blazedLeftEyeBorder = pygame.image.load("source/vox_blazed_lefteye_border.svg").convert_alpha()
        self.blazedLeftEyeBorder = pygame.transform.scale(self.blazedLeftEyeBorder, self.ur([711, 223], x=True, y=True))

        ## Sourcil Droit
        self.blazedLeftEyebrow = pygame.image.load("source/vox_blazed_lefteyebrow.svg").convert_alpha()
        self.blazedLeftEyebrow = pygame.transform.scale(self.blazedLeftEyebrow, self.ur([719, 219], x=True, y=True))

        ## Oeuil Droit Fond
        self.blazedRightEyeImage = pygame.image.load("source/vox_blazed_righteye_bg.svg").convert_alpha()
        self.blazedRightEyeImage = pygame.transform.scale(self.blazedRightEyeImage, self.ur([734, 253], x=True, y=True))
        self.blazedRightEyeMask = pygame.image.load("source/vox_blazed_righteye_mask.svg").convert_alpha()
        self.blazedRightEyeMask = pygame.transform.scale(self.blazedRightEyeMask, self.ur([734, 253], x=True, y=True))

        ## Oeuil Droit Contour
        self.blazedRightEyeBorder = pygame.image.load("source/vox_blazed_righteye_border.svg").convert_alpha()
        self.blazedRightEyeBorder = pygame.transform.scale(self.blazedRightEyeBorder, self.ur([734, 253], x=True, y=True))

        ## Sourcil Droit
        self.blazedRightEyebrow = pygame.image.load("source/vox_blazed_righteyebrow.svg").convert_alpha()
        self.blazedRightEyebrow = pygame.transform.scale(self.blazedRightEyebrow, self.ur([735, 266], x=True, y=True))

        ## Pupille
        self.defaultPupilImage = pygame.image.load("source/vox_pupil.svg").convert_alpha()
        self.defaultPupilImage = pygame.transform.scale(self.defaultPupilImage, self.ur([61, 91], x=True, y=True))

        ## Bouche
        self.blaedMouthImage = pygame.image.load("source/vox_blazed_mouth.svg").convert_alpha()
        self.blaedMouthImage = pygame.transform.scale(self.blaedMouthImage, self.ur([478, 224], x=True, y=True))

    def importDemonSprites(self):
        # SPRITES DES YEUX
        ## Oeil du bas
        self.demonDownEyeImage = pygame.image.load("source/vox_demon_downeye_bg.svg").convert_alpha()
        self.demonDownEyeImage = pygame.transform.scale(self.demonDownEyeImage, self.ur([737, 343], x=True, y=True))
        self.demonDownEyeMask = pygame.image.load("source/vox_demon_downeye_mask.svg").convert_alpha()
        self.demonDownEyeMask = pygame.transform.scale(self.demonDownEyeMask, self.ur([737, 343], x=True, y=True))

        ## Contour de l'oeil du bas
        self.demonDownEyeBorder = pygame.image.load("source/vox_demon_downeye_border.svg").convert_alpha()
        self.demonDownEyeBorder = pygame.transform.scale(self.demonDownEyeBorder, self.ur([737, 343], x=True, y=True))
        self.demonDownEyebrow = pygame.image.load("source/vox_demon_downeyebrow.svg").convert_alpha()
        self.demonDownEyebrow = pygame.transform.scale(self.demonDownEyebrow, self.ur([727, 179], x=True, y=True))

        ## Oeil du haut
        self.demonUpEyeImage = pygame.image.load("source/vox_demon_upeye_bg.svg").convert_alpha()
        self.demonUpEyeImage = pygame.transform.scale(self.demonUpEyeImage, self.ur([504, 127], x=True, y=True))
        self.demonUpEyeMask = pygame.image.load("source/vox_demon_upeye_mask.svg").convert_alpha()
        self.demonUpEyeMask = pygame.transform.scale(self.demonUpEyeMask, self.ur([504, 127], x=True, y=True))

        ## Contour de l'oeil du haut
        self.demonUpEyeBorder = pygame.image.load("source/vox_demon_upeye_border.svg").convert_alpha()
        self.demonUpEyeBorder = pygame.transform.scale(self.demonUpEyeBorder, self.ur([504, 127], x=True, y=True))
        self.demonUpEyebrow = pygame.image.load("source/vox_demon_upeyebrow.svg").convert_alpha()
        self.demonUpEyebrow = pygame.transform.scale(self.demonUpEyebrow, self.ur([576, 239], x=True, y=True))

        ## Pupille
        self.demonPupil = pygame.image.load("source/vox_demon_pupil.svg").convert_alpha()
        self.demonPupil = pygame.transform.scale(self.demonPupil, self.ur([93, 132], x=True, y=True))

        ## Bouche
        self.demonMouthImage = pygame.image.load("source/vox_demon_mouth_bg.svg").convert_alpha()
        self.demonMouthImage = pygame.transform.scale(self.demonMouthImage, self.ur([1959, 783], x=True, y=True))
        self.demonMouthMask = pygame.image.load("source/vox_demon_mouth_mask.svg").convert_alpha()
        self.demonMouthMask = pygame.transform.scale(self.demonMouthMask, self.ur([1959, 783], x=True, y=True))
        self.demonMouthTop = pygame.image.load("source/vox_demon_mouth_top.svg").convert_alpha()
        self.demonMouthTop = pygame.transform.scale(self.demonMouthTop, self.ur([1963, 430], x=True, y=True))

    def importHateSprites(self):
        ## Oeil
        self.hateEyeMask = pygame.image.load("source/vox_hate_eye_bg.svg").convert_alpha()
        self.hateEyeMask = pygame.transform.scale(self.hateEyeMask, self.ur([870, 535], x=True, y=True))
        self.hateEyeBorder = pygame.image.load("source/vox_hate_eye_border.svg").convert_alpha()
        self.hateEyeBorder = pygame.transform.scale(self.hateEyeBorder, self.ur([870, 535], x=True, y=True))

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
                self.hatsuneVideo.pause()
                if event.key == pygame.K_1 and self.currentState != voxState.BLAZED: ## 1
                    self.currentState = voxState.BLAZED
                if event.key == pygame.K_2 and self.currentState != voxState.FULLSCREENHYPNOSE:
                    self.currentState = voxState.FULLSCREENHYPNOSE
                if event.key == pygame.K_3 and self.currentState != voxState.MIKUVIDEO:
                    self.currentState = voxState.MIKUVIDEO
                    self.hatsuneVideo.resume()
                if event.key == pygame.K_4 and self.currentState != voxState.DEMON:
                    self.currentState = voxState.DEMON
                if event.key == pygame.K_5 and self.currentState != voxState.HATE:
                    self.currentState = voxState.HATE

    def update(self):
        self.eyeShiftRatioX = self.joysticks[0].get_axis(0)
        self.eyeShiftRatioY = self.joysticks[0].get_axis(1)
        self.mouthShiftRatio = 0.5 - self.joysticks[0].get_axis(3)/2

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
        elif self.currentState == voxState.DEMON:
            self.showDemonFace()
        elif self.currentState == voxState.HATE:
            self.showHateFace()

        # CONTOUR ROUGE
        pygame.draw.rect(self.screen, (214, 28, 41), (0, 0, self.screen.get_width(), self.screen.get_height()), int(self.ur(10, y=True)))

        # Afficher les changements
        pygame.display.update()

    def showBackground(self):
        # --- FOND BLEU UNI ---
        self.screen.fill((16, 97, 148))

        # --- ECLAIR SUR SON FRONT ---
        toShow = pygame.transform.rotate(self.lightningImage, -40)
        self.screen.blit(toShow, (self.ur(-410, y=True), self.ur(-350, y=True)))

        # --- DEGRADE CIRCULAIRE ---
        self.screen.blit(self.gradientSurface, (self.screen.get_width()/2 - self.gradientBounds/2, self.screen.get_height()/2 - self.gradientBounds/2))

    def showBlazedFace(self):
        # LEFT EYE
        pupilPosition = [self.blazedLeftEyeImage.get_width() / 2, self.blazedLeftEyeImage.get_height() / 2 - self.defaultPupilImage.get_height() / 2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.blazedLeftEyeImage.get_width() / 2)
        pupilPosition[1] += self.eyeShiftRatioY * (self.blazedLeftEyeImage.get_height() / 2)

        faceDisplacement = self.eyeShiftRatioY * self.ur(80, y=True)

        finalPupilImage = pygame.transform.rotate(self.defaultPupilImage, self.eyeShiftRatioX * 20)

        self.blazedLeftEyeImage.fill((255, 0, 66))
        self.blazedLeftEyeImage.blit(finalPupilImage, pupilPosition)
        self.blazedLeftEyeImage.blit(self.blazedLeftEyeBorder, (0, 0))


        result = self.blazedLeftEyeMask.copy()
        result.blit(self.blazedLeftEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([111, 409], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        # RIGHT EYEBROW
        position = self.ur([120, 140], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.blazedLeftEyebrow, position)


        # RIGHT EYE
        pupilPosition = [self.blazedRightEyeImage.get_width() / 2 - self.defaultPupilImage.get_width(), self.blazedRightEyeImage.get_height() / 2 - self.defaultPupilImage.get_height() / 2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.blazedRightEyeImage.get_width() / 2)
        pupilPosition[1] += self.eyeShiftRatioY * (self.blazedRightEyeImage.get_height() / 2)

        self.blazedRightEyeImage.fill((255, 0, 66))
        self.blazedRightEyeImage.blit(finalPupilImage, pupilPosition)
        self.blazedRightEyeImage.blit(self.blazedRightEyeBorder, (0, 0))

        result = self.blazedRightEyeMask.copy()
        result.blit(self.blazedRightEyeImage, (0, 0), None, pygame.BLEND_MULT)

        position = [self.screen.get_width() - self.ur(151, x=True) - self.blazedRightEyeImage.get_width(), self.ur(375, y=True)]
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        # RIGHT EYEBROW
        position = [self.screen.get_width() - self.blazedRightEyebrow.get_width() - self.ur(184, x=True), self.ur(99, y=True)]
        position[1] += faceDisplacement
        self.screen.blit(self.blazedRightEyebrow, position)


        # MOUTH
        position = [0,0]
        position[0] = self.ur(658, x=True)
        position[1] = self.screen.get_height() - self.ur(101, x=True) - self.blaedMouthImage.get_height() + faceDisplacement
        self.screen.blit(self.blaedMouthImage, position)

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

    def showDemonFace(self):
        # DOWN EYE
        pupilPosition = [self.demonDownEyeImage.get_width()/2, self.demonDownEyeImage.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.demonDownEyeImage.get_width() / 2)
        pupilPosition[1] += self.eyeShiftRatioY * (self.demonDownEyeImage.get_height() / 2)

        faceDisplacement = self.eyeShiftRatioY * self.ur(100, y=True)

        finalPupilImage = pygame.transform.rotate(self.demonPupil, self.eyeShiftRatioX * 40)

        self.demonDownEyeImage.fill((255, 0, 66))
        self.demonDownEyeImage.blit(finalPupilImage, pupilPosition)
        self.demonDownEyeImage.blit(self.demonDownEyeBorder, (0,0))

        result = self.demonDownEyeMask.copy()
        result.blit(self.demonDownEyeImage, (0,0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([126,243], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([149,197], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.demonDownEyebrow, position)


        # UP EYE
        pupilPosition = [self.demonUpEyeImage.get_width()/2, self.demonUpEyeImage.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.demonUpEyeImage.get_width() / 2)
        pupilPosition[1] += self.eyeShiftRatioY * (self.demonUpEyeImage.get_height())

        self.demonUpEyeImage.fill((255, 0, 66))
        self.demonUpEyeImage.blit(finalPupilImage, pupilPosition)
        self.demonUpEyeImage.blit(self.demonUpEyeBorder, (0,0))

        result = self.demonUpEyeMask.copy()
        result.blit(self.demonUpEyeImage, (0,0), None, pygame.BLEND_RGBA_MULT)
        result = pygame.transform.rotate(result, -25.5)

        position = self.ur([344, 0], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = [self.ur(288, x=True), 0]
        position[1] += faceDisplacement
        self.screen.blit(self.demonUpEyebrow, position)


        # RIGHT EYE
        rightEye = pygame.Surface(self.ur([900, 500], x=True, y=True))
        rightEye.fill((255, 0, 66))
        self.hypnoseShiftRatio += .005
        if self.hypnoseShiftRatio > 1: self.hypnoseShiftRatio = 0

        center = [rightEye.get_width()/2, rightEye.get_height()/2]
        center[0] += self.eyeShiftRatioX * (rightEye.get_width() / 2)
        center[1] += self.eyeShiftRatioY * (rightEye.get_height() / 2)

        for i in range (5):
            shift = self.hypnoseShiftRatio + ( i*.2 )
            if shift > 1: shift -= 1
            shift = math.exp(shift) - 1

            radiusShift = shift * rightEye.get_width()/2
            widthShift = math.ceil(shift * self.ur(20, y=True))

            pygame.draw.circle(rightEye, [0,0,0], (center[0], center[1]), radiusShift, widthShift)

        pygame.draw.rect(rightEye, (66, 219, 230), [0,0,rightEye.get_width(),rightEye.get_height()], int(self.ur(8, y=True)))
        rightEye.blit(self.hypnosisPupil, (center[0] - self.hypnosisPupil.get_width()/2, center[1] - self.hypnosisPupil.get_height()/2))

        position = [self.screen.get_width() - rightEye.get_width(), 0]
        position[1] += faceDisplacement
        self.screen.blit(rightEye, position)


        # MOUTH
        self.demonMouthImage.blit(self.demonMouthTop, (0, 0))
        demonMouseRatio = self.mouthShiftRatio * 0.5 + 0.5

        result = self.demonMouthMask.copy()
        result.blit(self.demonMouthImage, (0,0), None, pygame.BLEND_RGBA_MULT)
        result = pygame.transform.scale(result, (result.get_width(), result.get_height() * demonMouseRatio))

        position = self.ur([47,466], x=True, y=True)
        position[1] += faceDisplacement
        position[1] += self.demonMouthImage.get_height()/2
        position[1] -= (demonMouseRatio * self.demonMouthImage.get_height()/2)
        self.screen.blit(result, position)

    def showHateFace(self):
        # --- FOND GRIS ---
        self.screen.fill((66, 65, 66))

        # --- DEGRADE CIRCULAIRE ---
        self.screen.blit(self.hateGradientSurface, (self.screen.get_width()/2 - self.hateGradientBounds/2, self.screen.get_height()/2 - self.hateGradientBounds/5))

        # --- ECLAIR SUR SON FRONT ---
        toShow = pygame.transform.rotate(self.hateLightningImage, -40)
        self.screen.blit(toShow, (self.ur(-410, y=True), self.ur(-350, y=True)))

        # OEIL
        hateEye = pygame.Surface((self.hateEyeMask.get_width(), self.hateEyeMask.get_height()))
        hateEye.fill((255, 0, 66))

        self.hypnoseShiftRatio += .005
        if self.hypnoseShiftRatio > 1: self.hypnoseShiftRatio = 0

        center = [hateEye.get_width()/2, hateEye.get_height()/2]
        center[0] += self.eyeShiftRatioX * (hateEye.get_width() / 2)
        center[1] += self.eyeShiftRatioY * (hateEye.get_height() / 2)

        for i in range (5):
            shift = self.hypnoseShiftRatio + ( i*.2 )
            if shift > 1: shift -= 1
            shift = math.exp(shift) - 1

            radiusShift = shift * hateEye.get_width()/2
            widthShift = math.ceil(shift * self.ur(20, y=True))

            pygame.draw.circle(hateEye, [0,0,0], (center[0], center[1]), radiusShift, widthShift)

        angle = 20 + self.eyeShiftRatioX * 10
        newHypnosisPupil = pygame.transform.rotate(self.hypnosisPupil, angle)
        hateEye.blit(newHypnosisPupil, (center[0] - self.hypnosisPupil.get_width()/2, center[1] - self.hypnosisPupil.get_height()/2))

        hateEye.blit(self.hateEyeBorder)

        result = self.hateEyeMask.copy()
        result.blit(hateEye, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = [self.screen.get_width() - result.get_width() - self.ur(50, x=True), self.ur(76, y=True)]
        position[1] += self.eyeShiftRatioY * self.ur(80, y=True)
        self.screen.blit(result, position)

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
# screen = pygame.display.set_mode((800, 450))
# screen = pygame.display.set_mode((1920, 1080))
screen = pygame.display.set_mode((0, 0))
instance = Main(screen)
instance.run()

pygame.quit()