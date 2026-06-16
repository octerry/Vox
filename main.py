import pygame, math
from pyvidplayer2 import Video
from enum import Enum

class voxState(Enum):
    DEFAULT = 0
    BLAZED = 1
    FULLSCREENHYPNOSE = 2
    MIKUVIDEO = 3
    DEMON = 4
    HATE = 5
    DEI = 6

class Main:
    def __init__(self, screen):
        # Ca tourne
        self.isRunning = True

        # Taille de la fenetre
        self.screen = screen

        # Titre de la fenetre
        pygame.display.set_caption("Vox")

        self.clock = pygame.time.Clock()

        self.firstRun = True

        self.setLoadingScreenAt(.01)

        self.lightningImage = None
        self.gradientSurface = None
        self.gradientBounds = None

        self.hateLightningImage = None
        self.hateGradientSurface = None
        self.hateGradientBounds = None

        self.pixelFilter = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)

        self.setLoadingScreenAt(.02)
        self.backgroundSetup()

        self.joysticks = []
        self.eyeShiftRatioX = 0
        self.eyeShiftRatioY = 0

        self.mouthShiftRatio = 0

        self.currentState = voxState.DEFAULT

        self.hypnoseShiftRatio = 0

        self.importSprites()
        self.importVideos()

    def setLoadingScreenAt(self, p):
        width = p * self.screen.get_width()
        pygame.draw.rect(self.screen, (33, 141, 191), (0,0,width,10))
        pygame.display.update()

    def backgroundSetup(self):
        # DEFAULT BG
        ## L'éclair classique
        rectWidth = self.ur(180, x=True)
        rectHeight = self.ur(800, y=True)
        self.lightningImage = pygame.Surface((rectWidth * 2, rectHeight * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.lightningImage, (33, 141, 191), (0, 0, rectWidth, rectHeight))
        pygame.draw.rect(self.lightningImage, (33, 141, 191),(rectWidth, rectHeight - rectWidth, rectWidth, rectHeight))
        self.setLoadingScreenAt(.05)

        ## Le dégradé circulaire classique
        self.gradientBounds = int(2 * self.screen.get_height())
        self.gradientSurface = pygame.Surface((self.gradientBounds, self.gradientBounds), pygame.SRCALPHA)
        center = [self.gradientBounds / 2, self.gradientBounds / 2]
        for radius in range(self.gradientBounds // 2, 0, -1):
            opacity = 255 * (1 - radius / (self.gradientBounds // 2))
            color = (74, 158, 189, int(opacity))
            pygame.draw.circle(self.gradientSurface, color, center, radius)
        self.setLoadingScreenAt(.1)

        ## L'éclair haine
        rectWidth = self.ur(180, x=True)
        rectHeight = self.ur(800, y=True)
        self.hateLightningImage = pygame.Surface((rectWidth * 2, rectHeight * 2), pygame.SRCALPHA)
        pygame.draw.rect(self.hateLightningImage, (16, 16, 16), (0, 0, rectWidth, rectHeight))
        pygame.draw.rect(self.hateLightningImage, (16, 16, 16),(rectWidth, rectHeight - rectWidth, rectWidth, rectHeight))
        self.setLoadingScreenAt(.15)

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
        self.setLoadingScreenAt(.2)

        # LE FILTRE PIXEL POUR DEI
        self.pixelFilter.fill((126,187,117,60))
        for x in range(self.screen.get_width()):
            for y in range(self.screen.get_height()):
                if x % int(self.ur(5, x=True)) == 0 and y % int(self.ur(5, y=True)) == 0:
                    self.pixelFilter.set_at((x, y), (255,255,255))
        self.setLoadingScreenAt(.21)

    def importSprites(self):
        ## Eclair d'hypnose
        self.hypnosisPupil = pygame.image.load("source/vox_hypnosis_lightning.svg").convert_alpha()
        self.hypnosisPupil = pygame.transform.scale(self.hypnosisPupil, self.ur([215, 390], x=True, y=True))

        self.importDefaultSprites()
        self.importBlazedSprites()
        self.importDemonSprites()
        self.importHateSprites()
        self.importDeiSprites()

    def importDefaultSprites(self):
        # YEUX
        ## Oeil gauche
        self.defaultLeftEyeImage = pygame.image.load("source/vox_default_lefteye_bg.svg").convert_alpha()
        self.defaultLeftEyeImage = pygame.transform.scale(self.defaultLeftEyeImage, self.ur([866, 352], x=True, y=True))
        self.defaultLeftEyeMask = pygame.image.load("source/vox_default_lefteye_mask.svg").convert_alpha()
        self.defaultLeftEyeMask = pygame.transform.scale(self.defaultLeftEyeMask, self.ur([866, 352], x=True, y=True))

        ## Contour oeil gauche
        self.defaultLeftEyeBorder = pygame.image.load("source/vox_default_lefteye_border.svg").convert_alpha()
        self.defaultLeftEyeBorder = pygame.transform.scale(self.defaultLeftEyeBorder, self.ur([866, 352], x=True, y=True))

        ## Sourcil gauche
        self.defaultLeftEyebrow = pygame.image.load("source/vox_default_lefteyebrow.svg").convert_alpha()
        self.defaultLeftEyebrow = pygame.transform.scale(self.defaultLeftEyebrow, self.ur([718, 244], x=True, y=True))

        ## Oeil droit
        self.defaultRightEyeImage = pygame.image.load("source/vox_default_righteye_bg.svg").convert_alpha()
        self.defaultRightEyeImage = pygame.transform.scale(self.defaultRightEyeImage, self.ur([854, 376], x=True, y=True))
        self.defaultRightEyeMask = pygame.image.load("source/vox_default_righteye_mask.svg").convert_alpha()
        self.defaultRightEyeMask = pygame.transform.scale(self.defaultRightEyeMask, self.ur([854, 376], x=True, y=True))

        ## Contour oeil droit
        self.defaultRightEyeBorder = pygame.image.load("source/vox_default_righteye_border.svg").convert_alpha()
        self.defaultRightEyeBorder = pygame.transform.scale(self.defaultRightEyeBorder, self.ur([854, 376], x=True, y=True))

        ## Sourcil droite
        self.defaultRightEyebrow = pygame.image.load("source/vox_default_righteyebrow.svg").convert_alpha()
        self.defaultRightEyebrow = pygame.transform.scale(self.defaultRightEyebrow, self.ur([734, 276], x=True, y=True))

        ## Pupille
        self.defaultPupilImage = pygame.image.load("source/vox_pupil.svg").convert_alpha()
        self.defaultPupilImage = pygame.transform.scale(self.defaultPupilImage, self.ur([61, 91], x=True, y=True))

        ## Bouche
        self.defaultMouthMask = pygame.image.load("source/vox_default_mouth_mask.svg").convert_alpha()
        self.defaultMouthMask = pygame.transform.scale(self.defaultMouthMask, self.ur([1756, 855], x=True, y=True))
        self.defaultMouthBorder = pygame.image.load("source/vox_default_mouth_border.svg").convert_alpha()
        self.defaultMouthBorder = pygame.transform.scale(self.defaultMouthBorder, self.ur([1756, 855], x=True, y=True))

        self.defaultMouthTop = pygame.image.load("source/vox_default_mouth_top.svg").convert_alpha()
        self.defaultMouthTop = pygame.transform.scale(self.defaultMouthTop, self.ur([1756, 824], x=True, y=True))
        self.defaultMouthBottom = pygame.image.load("source/vox_default_mouth_bottom.svg").convert_alpha()
        self.defaultMouthBottom = pygame.transform.scale(self.defaultMouthBottom, self.ur([1756, 824], x=True, y=True))

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

        ## Bouche
        self.blazedMouthImage = pygame.image.load("source/vox_blazed_mouth.svg").convert_alpha()
        self.blazedMouthImage = pygame.transform.scale(self.blazedMouthImage, self.ur([478, 224], x=True, y=True))

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
        self.demonMouthImage = pygame.image.load("source/vox_demon_mouth.svg").convert_alpha()
        self.demonMouthImage = pygame.transform.scale(self.demonMouthImage, self.ur([1959, 783], x=True, y=True))

    def importHateSprites(self):
        ## Oeil
        self.hateEyeMask = pygame.image.load("source/vox_hate_eye_bg.svg").convert_alpha()
        self.hateEyeMask = pygame.transform.scale(self.hateEyeMask, self.ur([870, 535], x=True, y=True))
        self.hateEyeBorder = pygame.image.load("source/vox_hate_eye_border.svg").convert_alpha()
        self.hateEyeBorder = pygame.transform.scale(self.hateEyeBorder, self.ur([870, 535], x=True, y=True))

    def importDeiSprites(self):
        # EYES
        ## Left eye
        self.deiLeftEyeImage = pygame.image.load("source/vox_dei_lefteye_bg.svg").convert_alpha()
        self.deiLeftEyeImage = pygame.transform.scale(self.deiLeftEyeImage, self.ur([903, 614], x=True, y=True))
        self.deiLeftEyeMask = pygame.image.load("source/vox_dei_lefteye_mask.svg").convert_alpha()
        self.deiLeftEyeMask = pygame.transform.scale(self.deiLeftEyeMask, self.ur([903, 614], x=True, y=True))

        ## Left eye border
        self.deiLeftEyeBorder = pygame.image.load("source/vox_dei_lefteye_border.svg").convert_alpha()
        self.deiLeftEyeBorder = pygame.transform.scale(self.deiLeftEyeBorder, self.ur([903, 614], x=True, y=True))

        ## Left eyebrow
        self.deiLeftEyebrow = pygame.image.load("source/vox_dei_lefteyebrow.svg").convert_alpha()
        self.deiLeftEyebrow = pygame.transform.scale(self.deiLeftEyebrow, self.ur([905, 618], x=True, y=True))

        ## Right eye
        self.deiRightEyeImage = pygame.image.load("source/vox_dei_righteye_bg.svg").convert_alpha()
        self.deiRightEyeImage = pygame.transform.scale(self.deiRightEyeImage, self.ur([841, 656], x=True, y=True))
        self.deiRightEyeMask = pygame.image.load("source/vox_dei_righteye_mask.svg").convert_alpha()
        self.deiRightEyeMask = pygame.transform.scale(self.deiRightEyeMask, self.ur([841, 656], x=True, y=True))

        ## Right eye border
        self.deiRightEyeBorder = pygame.image.load("source/vox_dei_righteye_border.svg").convert_alpha()
        self.deiRightEyeBorder = pygame.transform.scale(self.deiRightEyeBorder, self.ur([841, 656], x=True, y=True))

        ## Right eyebrow
        self.deiRightEyebrow = pygame.image.load("source/vox_dei_righteyebrow.svg").convert_alpha()
        self.deiRightEyebrow = pygame.transform.scale(self.deiRightEyebrow, self.ur([772, 515], x=True, y=True))

        ## Pupil
        self.deiPupil = pygame.image.load("source/vox_dei_pupil.svg").convert_alpha()
        self.deiPupil = pygame.transform.scale(self.deiPupil, self.ur([69, 118], x=True, y=True))

        # MOUTH
        self.deiMouthMask = pygame.image.load("source/vox_dei_mouth_mask.svg").convert_alpha()
        self.deiMouthMask = pygame.transform.scale(self.deiMouthMask, self.ur([2109, 930], x=True, y=True))
        self.deiMouthBorder = pygame.image.load("source/vox_dei_mouth_border.svg").convert_alpha()
        self.deiMouthBorder = pygame.transform.scale(self.deiMouthBorder, self.ur([2109, 930], x=True, y=True))

    def importVideos(self):
        ## Noise video
        self.noiseVideo = Video("source/vox_dei_noise.mp4")
        self.noiseVideo.resize(self.deiMouthMask.get_size())

        ## Hatsune Miku
        self.hatsuneVideo = Video("source/hatsuneMiku.mp4")
        self.hatsuneVideo.resize(self.screen.get_size())
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
                if event.key == pygame.K_1 and self.currentState != voxState.DEFAULT:
                    self.currentState = voxState.DEFAULT
                if event.key == pygame.K_2 and self.currentState != voxState.BLAZED:
                    self.currentState = voxState.BLAZED
                if event.key == pygame.K_3 and self.currentState != voxState.FULLSCREENHYPNOSE:
                    self.currentState = voxState.FULLSCREENHYPNOSE
                if event.key == pygame.K_4 and self.currentState != voxState.MIKUVIDEO:
                    self.currentState = voxState.MIKUVIDEO
                    self.hatsuneVideo.resume()
                if event.key == pygame.K_5 and self.currentState != voxState.DEMON:
                    self.currentState = voxState.DEMON
                if event.key == pygame.K_6 and self.currentState != voxState.HATE:
                    self.currentState = voxState.HATE
                if event.key == pygame.K_7 and self.currentState != voxState.DEI:
                    self.currentState = voxState.DEI

    def update(self):
        self.eyeShiftRatioX = self.joysticks[0].get_axis(0)
        self.eyeShiftRatioY = self.joysticks[0].get_axis(1)
        self.mouthShiftRatio = -self.joysticks[0].get_axis(3) if self.joysticks[0].get_axis(3) < 0 else 0

    def display(self):
        # LE FOND
        self.showBackground()

        ## LES VISAGES
        if self.currentState == voxState.DEFAULT:
            self.showDefaultFace()
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
        elif self.currentState == voxState.DEI:
            self.showDeiFace()

        # CONTOUR ROUGE
        pygame.draw.rect(self.screen, (214, 28, 41), (0, 0, self.screen.get_width(), self.screen.get_height()), int(self.ur(10, y=True)))

        if self.currentState == voxState.DEI:
            self.screen.blit(self.pixelFilter, (0,0), None, pygame.BLEND_RGBA_MULT)

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

    def showDefaultFace(self):
        # LEFT EYE
        pupilPosition = [self.defaultLeftEyeImage.get_width() / 2, self.defaultLeftEyeImage.get_height() / 2 - self.defaultPupilImage.get_height() / 2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.defaultLeftEyeImage.get_width() / 2) - self.defaultPupilImage.get_width()/2
        pupilPosition[1] += self.eyeShiftRatioY * (self.defaultLeftEyeImage.get_height() / 2) - self.defaultPupilImage.get_height()/2

        spinValue = 180 if self.eyeShiftRatioY <= .1 else 0
        finalPupilImage = pygame.transform.rotate(self.defaultPupilImage, self.eyeShiftRatioX * 20 + spinValue)

        faceDisplacement = self.eyeShiftRatioY * self.ur(80, y=True)

        self.defaultLeftEyeImage.fill((255, 0, 66))
        self.defaultLeftEyeImage.blit(finalPupilImage, pupilPosition)
        self.defaultLeftEyeImage.blit(self.defaultLeftEyeBorder, (0,0))


        result = self.defaultLeftEyeMask.copy()
        result.blit(self.defaultLeftEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([60, 193], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([153, -31], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.defaultLeftEyebrow, position)


        # RIGHT EYE
        pupilPosition = [self.defaultRightEyeImage.get_width() / 2, self.defaultRightEyeImage.get_height() / 2 - self.defaultPupilImage.get_height() / 2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.defaultRightEyeImage.get_width() / 2) - self.defaultPupilImage.get_width()/2
        pupilPosition[1] += self.eyeShiftRatioY * (self.defaultRightEyeImage.get_height() / 2) - self.defaultPupilImage.get_height()/2

        self.defaultRightEyeImage.fill((255, 0, 66))
        self.defaultRightEyeImage.blit(finalPupilImage, pupilPosition)
        self.defaultRightEyeImage.blit(self.defaultRightEyeBorder, (0,0))


        result = self.defaultRightEyeMask.copy()
        result.blit(self.defaultRightEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = [ self.screen.get_width() - result.get_width() - self.ur(42,x=True), self.ur(146,y=True) ]
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = [ self.screen.get_width() - self.defaultRightEyebrow.get_width() - self.ur(128, x=True), self.ur(-31, y=True) ]
        position[1] += faceDisplacement
        self.screen.blit(self.defaultRightEyebrow, position)


        # MOUTH
        mouthImage = pygame.Surface((self.defaultMouthMask.get_width(), self.defaultMouthMask.get_height()))
        mouthImage.fill((25, 49, 58))

        mouthDeformation = self.mouthShiftRatio * self.defaultMouthTop.get_height()/2

        size = [ self.defaultMouthTop.get_width(),  self.defaultMouthTop.get_height() ]
        size[1] -= mouthDeformation
        newMouthTop = pygame.transform.scale(self.defaultMouthTop, size)
        mouthImage.blit(newMouthTop, (0, 0))

        size = [ self.defaultMouthBottom.get_width(),  self.defaultMouthBottom.get_height() ]
        size[1] -= mouthDeformation
        newMouthBottom = pygame.transform.scale(self.defaultMouthBottom, size)
        mouthImage.blit(newMouthBottom, (0, self.defaultMouthMask.get_height() - newMouthBottom.get_height()))

        mouthImage.blit(self.defaultMouthBorder, (0, 0))

        result = self.defaultMouthMask.copy()
        result.blit(mouthImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([122, 400], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

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
        position[1] = self.screen.get_height() - self.ur(101, x=True) - self.blazedMouthImage.get_height() + faceDisplacement
        self.screen.blit(self.blazedMouthImage, position)

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
        demonMouthRatio = self.mouthShiftRatio * 0.5 + 0.5

        size = [ self.demonMouthImage.get_width(), demonMouthRatio * self.demonMouthImage.get_height() ]
        result = pygame.transform.scale(self.demonMouthImage, size)

        position = self.ur([47,466], x=True, y=True)
        position[1] += faceDisplacement
        position[1] += self.demonMouthImage.get_height()/2
        position[1] -= (demonMouthRatio * self.demonMouthImage.get_height()/2)
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

    def showDeiFace(self):
        # LEFT EYE
        pupilPosition = [self.deiLeftEyeImage.get_width()/2, self.deiLeftEyeImage.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.deiLeftEyeImage.get_width() / 4) + self.deiLeftEyeImage.get_width() / 6
        pupilPosition[1] += self.eyeShiftRatioY * (self.deiLeftEyeImage.get_height() / 3)

        faceDisplacement = self.eyeShiftRatioY * self.ur(80, y=True)

        self.deiLeftEyeImage.fill((255, 0, 66))
        self.deiLeftEyeImage.blit(self.deiPupil, pupilPosition)
        self.deiLeftEyeImage.blit(self.deiLeftEyeBorder, (0,0))

        result = self.deiLeftEyeMask.copy()
        result.blit(self.deiLeftEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([-10, -83], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([50, -257], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.deiLeftEyebrow, position)


        # RIGHT EYE
        rightEye = pygame.Surface(self.deiRightEyeImage.get_size())
        rightEye.fill((255, 0, 66))
        self.hypnoseShiftRatio += .005
        if self.hypnoseShiftRatio > 1: self.hypnoseShiftRatio = 0

        center = [rightEye.get_width()/2, rightEye.get_height()/2]
        center[0] += self.eyeShiftRatioX * (rightEye.get_width() / 4) - rightEye.get_width() / 6
        center[1] += self.eyeShiftRatioY * (rightEye.get_height() / 3)

        for i in range (5):
            shift = self.hypnoseShiftRatio + ( i*.2 )
            if shift > 1: shift -= 1
            shift = math.exp(shift) - 1

            radiusShift = shift * rightEye.get_width()/2
            widthShift = math.ceil(shift * self.ur(20, y=True))

            pygame.draw.circle(rightEye, [0,0,0], (center[0], center[1]), radiusShift, widthShift)

        rightEye.blit(self.hypnosisPupil, (center[0] - self.hypnosisPupil.get_width()/2, center[1] - self.hypnosisPupil.get_height()/2))

        self.deiRightEyeImage.blit(rightEye, (0,0))
        self.deiRightEyeImage.blit(self.deiRightEyeBorder, (0,0))

        result = self.deiRightEyeMask.copy()
        result.blit(self.deiRightEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = [ self.screen.get_width() - result.get_width() + self.ur(11, x=True), self.ur(-71, y=True) ]
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([992, -150], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.deiRightEyebrow, position)


        # MOUTH
        deiMouth = pygame.Surface((self.deiMouthMask.get_width(), self.deiMouthMask.get_height()))

        self.noiseVideo.draw(deiMouth, (0,0))

        if self.noiseVideo.get_pos() >= 20:
            self.noiseVideo.restart()

        deiMouth.blit(self.deiMouthBorder, (0,0))

        result = self.deiMouthMask.copy()
        result.blit(deiMouth, (0, 0), None, pygame.BLEND_RGBA_MULT)

        size = [deiMouth.get_width(), deiMouth.get_height()/2]
        size[1] += self.mouthShiftRatio * deiMouth.get_height()/2
        result = pygame.transform.scale(result, size)

        position = self.ur([-89, 289], x=True, y=True)
        position[1] += deiMouth.get_height()/4
        position[1] -= self.mouthShiftRatio * deiMouth.get_height()/4
        position[1] += faceDisplacement
        self.screen.blit(result , position)


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