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
    LAUGH = 7
    MUTED = 8
    SMOL = 9
    CALIBRATION = 64

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

        self.setLoadingScreenAt(0.1)

        self.importDefaultSprites()
        self.setLoadingScreenAt(0.2)

        self.importBlazedSprites()
        self.setLoadingScreenAt(0.3)

        self.importDemonSprites()
        self.setLoadingScreenAt(0.4)

        self.importHateSprites()
        self.setLoadingScreenAt(0.5)

        self.importDeiSprites()
        self.setLoadingScreenAt(0.6)

        self.importLaughSprites()
        self.setLoadingScreenAt(0.7)

        self.importMutedSprites()
        self.setLoadingScreenAt(0.75)

        self.importSmolSprites()
        self.setLoadingScreenAt(0.9)

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

    def importLaughSprites(self):
        # EYES
        ## Left eye
        self.laughLeftEyeMask = pygame.image.load("source/vox_laugh_lefteye_mask.svg").convert_alpha()
        self.laughLeftEyeMask = pygame.transform.scale(self.laughLeftEyeMask, self.ur([790, 250], x=True, y=True))
        self.laughLeftEyeImage = pygame.Surface(self.laughLeftEyeMask.get_size())

        ## Left eye border
        self.laughLeftEyeBorder = pygame.image.load("source/vox_laugh_lefteye_border.svg").convert_alpha()
        self.laughLeftEyeBorder = pygame.transform.scale(self.laughLeftEyeBorder, self.ur([790, 250], x=True, y=True))

        ## Left eyebrow
        self.laughLeftEyebrow = pygame.image.load("source/vox_laugh_lefteyebrow.svg").convert_alpha()
        self.laughLeftEyebrow = pygame.transform.scale(self.laughLeftEyebrow, self.ur([744, 114], x=True, y=True))

        ## Right eye
        self.laughRightEyeMask = pygame.image.load("source/vox_laugh_righteye_mask.svg").convert_alpha()
        self.laughRightEyeMask = pygame.transform.scale(self.laughRightEyeMask, self.ur([829, 477], x=True, y=True))
        self.laughRightEyeImage = pygame.Surface(self.laughRightEyeMask.get_size())

        ## Right eye border
        self.laughRightEyeBorder = pygame.image.load("source/vox_laugh_righteye_border.svg").convert_alpha()
        self.laughRightEyeBorder = pygame.transform.scale(self.laughRightEyeBorder, self.ur([829, 477], x=True, y=True))

        ## Right eyebrow
        self.laughRightEyebrow = pygame.image.load("source/vox_laugh_righteyebrow.svg").convert_alpha()
        self.laughRightEyebrow = pygame.transform.scale(self.laughRightEyebrow, self.ur([751, 293], x=True, y=True))

        # MOUTH
        self.laughMouthMask = pygame.image.load("source/vox_laugh_mouth_mask.svg").convert_alpha()
        self.laughMouthMask = pygame.transform.scale(self.laughMouthMask, self.ur([1755, 850], x=True, y=True))
        self.laughMouthImage = pygame.Surface(self.laughMouthMask.get_size())

        ## Mouth border
        self.laughMouthBorder = pygame.image.load("source/vox_laugh_mouth_border.svg").convert_alpha()
        self.laughMouthBorder = pygame.transform.scale(self.laughMouthBorder, self.ur([1755, 850], x=True, y=True))

        ## Mouth inner
        self.laughMouthTop = pygame.image.load("source/vox_laugh_mouth_top.svg").convert_alpha()
        self.laughMouthTop = pygame.transform.scale(self.laughMouthTop, self.ur([1755, 760], x=True, y=True))
        self.laughMouthBottom = pygame.image.load("source/vox_laugh_mouth_bottom.svg").convert_alpha()
        self.laughMouthBottom = pygame.transform.scale(self.laughMouthBottom, self.ur([1755, 850], x=True, y=True))

        ## Tongue
        self.laughTongue = pygame.image.load("source/vox_laugh_tongue.svg").convert_alpha()
        self.laughTongue = pygame.transform.scale(self.laughTongue, self.ur([921, 397], x=True, y=True))

        ## Blood drop
        self.laughBlood = pygame.image.load("source/vox_laugh_blood.svg").convert_alpha()
        self.laughBlood = pygame.transform.scale(self.laughBlood, self.ur([76, 407], x=True, y=True))

    def importMutedSprites(self):
        # MUTE SYMBOL
        self.mutedImage = pygame.image.load("source/vox_muted.svg").convert_alpha()
        self.mutedImage = pygame.transform.scale(self.mutedImage, self.ur([980, 980], x=True, y=True))

    def importSmolSprites(self):
        # EYES
        ## Left eye
        self.smolLeftEyeMask = pygame.image.load("source/vox_small_lefteye_mask.svg").convert_alpha()
        self.smolLeftEyeMask = pygame.transform.scale(self.smolLeftEyeMask, self.ur([175, 144], x=True, y=True))
        self.smolLeftEyeImage = pygame.Surface(self.smolLeftEyeMask.get_size())

        ## Left eye border
        self.smolLeftEyeBorder = pygame.image.load("source/vox_small_lefteye_border.svg").convert_alpha()
        self.smolLeftEyeBorder = pygame.transform.scale(self.smolLeftEyeBorder, self.ur([175, 144], x=True, y=True))

        ## Left eyebrow
        self.smolLeftEyebrow = pygame.image.load("source/vox_small_lefteyebrow.svg").convert_alpha()
        self.smolLeftEyebrow = pygame.transform.scale(self.smolLeftEyebrow, self.ur([204, 150], x=True, y=True))

        ## Left eye dark circle
        self.smolLeftDarkCircle = pygame.image.load("source/vox_small_leftdarkcircle.svg").convert_alpha()
        self.smolLeftDarkCircle = pygame.transform.scale(self.smolLeftDarkCircle, self.ur([84, 37], x=True, y=True))

        ## Right eye
        self.smolRightEyeMask = pygame.image.load("source/vox_small_righteye_mask.svg").convert_alpha()
        self.smolRightEyeMask = pygame.transform.scale(self.smolRightEyeMask, self.ur([174, 135], x=True, y=True))
        self.smolRightEyeImage = pygame.Surface(self.smolRightEyeMask.get_size())

        ## Right eye border
        self.smolRightEyeBorder = pygame.image.load("source/vox_small_righteye_border.svg").convert_alpha()
        self.smolRightEyeBorder = pygame.transform.scale(self.smolRightEyeBorder, self.ur([174, 135], x=True, y=True))

        ## Right eyebrow
        self.smolRightEyebrow = pygame.image.load("source/vox_small_righteyebrow.svg").convert_alpha()
        self.smolRightEyebrow = pygame.transform.scale(self.smolRightEyebrow, self.ur([174, 135], x=True, y=True))

        ## Right eye dark circle
        self.smolRightDarkCircle = pygame.image.load("source/vox_small_rightdarkcircle.svg").convert_alpha()
        self.smolRightDarkCircle = pygame.transform.scale(self.smolRightDarkCircle, self.ur([76, 31], x=True, y=True))

        ## Pupil
        self.smolPupil = pygame.image.load("source/vox_pupil.svg").convert_alpha()
        self.smolPupil = pygame.transform.scale(self.smolPupil, self.ur([19, 29], x=True, y=True))

        ## Sweat
        self.smolSweatLeft = pygame.image.load("source/vox_small_sweat_left.svg").convert_alpha()
        self.smolSweatLeft = pygame.transform.scale(self.smolSweatLeft, self.ur([26, 45], x=True, y=True))
        self.smolSweatBottomLeft = pygame.image.load("source/vox_small_sweat_bottomleft.svg").convert_alpha()
        self.smolSweatBottomLeft = pygame.transform.scale(self.smolSweatBottomLeft, self.ur([20, 29], x=True, y=True))
        self.smolSweatBottomRight = pygame.image.load("source/vox_small_sweat_bottomright.svg").convert_alpha()
        self.smolSweatBottomRight = pygame.transform.scale(self.smolSweatBottomRight, self.ur([17, 22], x=True, y=True))
        self.smolSweatTopRight = pygame.image.load("source/vox_small_sweat_topright.svg").convert_alpha()
        self.smolSweatTopRight = pygame.transform.scale(self.smolSweatTopRight, self.ur([21, 41], x=True, y=True))

        # Mouth
        self.smolMouthImage = pygame.image.load("source/vox_small_mouth_bg.svg").convert_alpha()
        self.smolMouthImage = pygame.transform.scale(self.smolMouthImage, self.ur([88, 86], x=True, y=True))
        self.smolMouthMask = pygame.image.load("source/vox_small_mouth_mask.svg").convert_alpha()
        self.smolMouthMask = pygame.transform.scale(self.smolMouthMask, self.ur([88, 86], x=True, y=True))
        self.smolMouthTop = pygame.image.load("source/vox_small_mouth_top.svg").convert_alpha()
        self.smolMouthTop = pygame.transform.scale(self.smolMouthTop, self.ur([88, 22], x=True, y=True))
        self.smolMouthBottom = pygame.image.load("source/vox_small_mouth_bottom.svg").convert_alpha()
        self.smolMouthBottom = pygame.transform.scale(self.smolMouthBottom, self.ur([72, 86], x=True, y=True))

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
                match event.key:
                    case pygame.K_1 :
                        self.currentState = voxState.DEFAULT
                    case pygame.K_2 :
                        self.currentState = voxState.BLAZED
                    case pygame.K_3 :
                        self.currentState = voxState.FULLSCREENHYPNOSE
                    case pygame.K_4 :
                        self.currentState = voxState.MIKUVIDEO
                        self.hatsuneVideo.resume()
                    case pygame.K_5 :
                        self.currentState = voxState.DEMON
                    case pygame.K_6 :
                        self.currentState = voxState.HATE
                    case pygame.K_7 :
                        self.currentState = voxState.DEI
                    case pygame.K_8 :
                        self.currentState = voxState.LAUGH
                    case pygame.K_9 :
                        self.currentState = voxState.MUTED
                    case pygame.K_0 :
                        self.currentState = voxState.SMOL
                    case pygame.K_c :
                        self.currentState = voxState.CALIBRATION

    def update(self):
        self.eyeShiftRatioX = self.joysticks[0].get_axis(0)
        self.eyeShiftRatioY = self.joysticks[0].get_axis(1)
        self.mouthShiftRatio = -self.joysticks[0].get_axis(3) if self.joysticks[0].get_axis(3) < 0 else 0

    def display(self):
        # LE FOND
        self.showBackground()

        # LES VISAGES
        match self.currentState:
            case voxState.DEFAULT:
                self.showDefaultFace()
            case voxState.BLAZED:
                self.showBlazedFace()
            case voxState.FULLSCREENHYPNOSE:
                self.showHypnoticFace()
            case voxState.MIKUVIDEO:
                self.showHatsuneMiku()
            case voxState.DEMON:
                self.showDemonFace()
            case voxState.HATE:
                self.showHateFace()
            case voxState.DEI:
                self.showDeiFace()
            case voxState.LAUGH:
                self.showLaughFace()
            case voxState.MUTED:
                self.showMutedFace()
            case voxState.SMOL:
                self.showSmolFace()
            case voxState.CALIBRATION:
                self.showCalibrationFace()


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
        pupilPosition[0] += self.eyeShiftRatioX * (self.deiLeftEyeImage.get_width() / 4) + self.deiLeftEyeImage.get_width() / 8
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
        center[1] += self.eyeShiftRatioY * (rightEye.get_height() / 3) + self.deiPupil.get_height()/2

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

    def showLaughFace(self):
        # LEFT EYE
        pupilPosition = [self.laughLeftEyeMask.get_width()/2, self.laughLeftEyeMask.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.laughLeftEyeMask.get_width() / 4) + self.defaultPupilImage.get_width()/2
        pupilPosition[1] += self.eyeShiftRatioY * (self.laughLeftEyeMask.get_height() / 5) - self.defaultPupilImage.get_height()

        spinValue = 180 if self.eyeShiftRatioY <= -.3 else 0
        finalPupilImage = pygame.transform.rotate(self.defaultPupilImage, self.eyeShiftRatioX * 10 + spinValue)

        faceDisplacement = self.eyeShiftRatioY * self.ur(80, y=True)

        self.laughLeftEyeImage.fill((255, 0, 66))
        self.laughLeftEyeImage.blit(finalPupilImage, pupilPosition)
        self.laughLeftEyeImage.blit(self.laughLeftEyeBorder, (0,0))

        result = self.laughLeftEyeMask.copy()
        result.blit(self.laughLeftEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([113, 239], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([153, 157], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.laughLeftEyebrow, position)


        # RIGHT EYE
        rightEye = pygame.Surface(self.laughRightEyeMask.get_size())
        rightEye.fill((255, 0, 66))
        self.hypnoseShiftRatio += .005
        if self.hypnoseShiftRatio > 1: self.hypnoseShiftRatio = 0

        center = [rightEye.get_width()/2, rightEye.get_height()/2]
        center[0] += self.eyeShiftRatioX * (rightEye.get_width() / 4)
        center[1] += self.eyeShiftRatioY * (rightEye.get_height() / 3)

        for i in range (5):
            shift = self.hypnoseShiftRatio + ( i*.2 )
            if shift > 1: shift -= 1
            shift = math.exp(shift) - 1

            radiusShift = shift * rightEye.get_width()/2
            widthShift = math.ceil(shift * self.ur(20, y=True))

            pygame.draw.circle(rightEye, [0,0,0], (center[0], center[1]), radiusShift, widthShift)

        rightEye.blit(self.hypnosisPupil, (center[0] - self.hypnosisPupil.get_width()/2, center[1] - self.hypnosisPupil.get_height()/2))

        self.laughRightEyeImage.blit(rightEye, (0,0))
        self.laughRightEyeImage.blit(self.laughRightEyeBorder, (0,0))

        result = self.laughRightEyeMask.copy()
        result.blit(self.laughRightEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = [ self.screen.get_width() - result.get_width() - self.ur(60, x=True), self.ur(100, y=True) ]
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = [ self.screen.get_width() - self.laughRightEyebrow.get_width() - self.ur(142, x=True), self.ur(-28, y=True) ]
        position[1] += faceDisplacement
        self.screen.blit(self.laughRightEyebrow, position)

        # MOUTH
        self.laughMouthImage.fill((25, 49, 58))

        position = [ self.laughMouthImage.get_width() - self.laughTongue.get_width(), self.laughMouthImage.get_height() - self.laughTongue.get_height() ]
        self.laughMouthImage.blit(self.laughTongue, position)

        scale = [ self.laughMouthTop.get_width(), self.laughMouthTop.get_height() ]
        scale[1] *= .5 - ( self.mouthShiftRatio * .5 ) + .5
        finalMouthTop = pygame.transform.scale(self.laughMouthTop, scale)
        position = [0, 0]
        position[1] += self.mouthShiftRatio * self.laughMouthBottom.get_height()/10
        self.laughMouthImage.blit(finalMouthTop, position)

        scale = [ self.laughMouthBottom.get_width(), self.laughMouthBottom.get_height() ]
        scale[1] *= .5 - ( self.mouthShiftRatio * .5 ) + .5
        finalMouthBottom = pygame.transform.scale(self.laughMouthBottom, scale)
        position = [ 0, self.laughMouthMask.get_height() - finalMouthBottom.get_height() ]
        position[1] += self.mouthShiftRatio * self.laughMouthBottom.get_height()/5
        self.laughMouthImage.blit(finalMouthBottom, position)

        self.laughMouthImage.blit(self.laughMouthBorder, (0, 0))

        result = self.laughMouthMask.copy()
        result.blit(self.laughMouthImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([1548, 430], x=True, y=True)
        result.blit(self.laughBlood, position)

        scale = [ result.get_width(), result.get_height() ]
        scale[1] *= ( self.mouthShiftRatio * .5 ) + .5

        result = pygame.transform.scale(result, scale)

        position = self.ur([113, 309], x=True, y=True)
        position[1] += faceDisplacement
        position[1] += self.laughMouthMask.get_height()/5
        position[1] -= self.laughMouthMask.get_height()/5 * (self.mouthShiftRatio)
        self.screen.blit(result, position)

    def showMutedFace(self):
        # MUTE SYMBOL
        position = [ self.screen.get_width()/2 - self.mutedImage.get_width()/2, self.screen.get_height()/2 - self.mutedImage.get_height()/2 ]
        self.screen.blit(self.mutedImage, position)

    def showSmolFace(self):
        # LEFT EYE
        pupilPosition = [self.smolLeftEyeMask.get_width()/2, self.smolLeftEyeMask.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.smolLeftEyeMask.get_width() / 4) + self.smolPupil.get_width()
        pupilPosition[1] += self.eyeShiftRatioY * (self.smolLeftEyeMask.get_height() / 5) - self.smolPupil.get_height()

        spinValue = 180 if self.eyeShiftRatioY <= -.3 else 0
        finalPupilImage = pygame.transform.rotate(self.smolPupil, self.eyeShiftRatioX * 10 + spinValue)

        faceDisplacement = self.eyeShiftRatioY * self.ur(80, y=True)

        self.smolLeftEyeImage.fill((255, 0, 66))
        self.smolLeftEyeImage.blit(finalPupilImage, pupilPosition)
        self.smolLeftEyeImage.blit(self.smolLeftEyeBorder, (0,0))

        result = self.smolLeftEyeMask.copy()
        result.blit(self.smolLeftEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([764, 363], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([711, 293], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.smolLeftEyebrow, position)

        position = self.ur([753,486], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.smolLeftDarkCircle, position)


        # RIGHT EYE
        pupilPosition = [self.smolRightEyeMask.get_width()/2, self.smolRightEyeMask.get_height()/2]
        pupilPosition[0] += self.eyeShiftRatioX * (self.smolRightEyeMask.get_width() / 4) - self.smolPupil.get_width()
        pupilPosition[1] += self.eyeShiftRatioY * (self.smolRightEyeMask.get_height() / 5) - self.smolPupil.get_height()

        spinValue = 180 if self.eyeShiftRatioY <= -.3 else 0
        finalPupilImage = pygame.transform.rotate(self.smolPupil, self.eyeShiftRatioX * 10 + spinValue)

        self.smolRightEyeImage.fill((255, 0, 66))
        self.smolRightEyeImage.blit(finalPupilImage, pupilPosition)
        self.smolRightEyeImage.blit(self.smolRightEyeBorder, (0,0))

        result = self.smolRightEyeMask.copy()
        result.blit(self.smolRightEyeImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        position = self.ur([989,363], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(result, position)

        position = self.ur([1010,279], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.smolRightEyebrow, position)

        position = self.ur([1087,490], x=True, y=True)
        position[1] += faceDisplacement
        self.screen.blit(self.smolRightDarkCircle, position)


        # MOUTH
        mouthImage = self.smolMouthImage.copy()
        mouthImage.blit(self.smolMouthBottom, self.ur([8,2], x=True, y=True))

        result = self.smolMouthMask.copy()
        result.blit(mouthImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

        scale = [ result.get_width(), result.get_height() ]
        scale[0] *= 2 - self.mouthShiftRatio
        scale[1] *= self.mouthShiftRatio
        result = pygame.transform.scale(result, scale)

        position = self.ur([882, 518], x=True, y=True)
        position[0] += self.mouthShiftRatio * result.get_width()/3
        position[1] += faceDisplacement
        position[1] += self.smolMouthImage.get_width()/6
        position[1] -= self.smolMouthImage.get_width()/6 * self.mouthShiftRatio
        self.screen.blit(result, position)

        position[1] -= self.smolMouthImage.get_width()/6
        position[1] += self.smolMouthImage.get_width()/6 * self.mouthShiftRatio
        scale = [ result.get_width(), self.smolMouthTop.get_height() ]
        mouthTop = pygame.transform.scale(self.smolMouthTop, scale)
        self.screen.blit(mouthTop, position)


        # SWEAT
        self.screen.blit(self.smolSweatLeft, self.ur([589, 481], x=True, y=True))
        self.screen.blit(self.smolSweatBottomLeft, self.ur([633, 577], x=True, y=True))
        self.screen.blit(self.smolSweatBottomRight, self.ur([1275, 559], x=True, y=True))
        self.screen.blit(self.smolSweatTopRight, self.ur([1221, 228], x=True, y=True))

    def showCalibrationFace(self):
        x1 = self.screen.get_width()/7
        x2 = x1 * 2
        x3 = x1 * 3
        x4 = x1 * 4
        x5 = x1 * 5
        x6 = x1 * 6
        pygame.draw.rect(self.screen, [255, 255, 255], [0,0,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [255, 255, 0], [x1,0,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 255, 255], [x2,0,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 255, 0], [x3,0,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [255, 0, 255], [x4,0,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [255, 0, 0], [x5,0,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 0, 255], [x6,0,x1,self.screen.get_height()])

        yPos = self.screen.get_height() - self.ur(150, y=True)
        pygame.draw.rect(self.screen, [0, 0, 255], [0,yPos,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 0, 0], [x1,yPos,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [255, 0, 255], [x2,yPos,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 0, 0], [x3,yPos,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 255, 255], [x4,yPos,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [0, 0, 0], [x5,yPos,x1,self.screen.get_height()])
        pygame.draw.rect(self.screen, [255, 255, 255], [x6,yPos,x1,self.screen.get_height()])


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