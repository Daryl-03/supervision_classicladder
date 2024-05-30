from modbus import Modbus
import pygame
from utils import *


class Switch:
    switches = [pygame.transform.scale(pygame.image.load("assets/on.svg"), (60, 60)),
                pygame.transform.scale(pygame.image.load("assets/off.svg"), (60, 60))]
    x_self = TAILLE_FENETRE[0] * 0.9
    y_self = 15

    def __init__(self, ecran, modbus: Modbus):
        self.ecran = ecran
        self.modbus = modbus
        self.state = modbus.lireBit(302)

    def draw(self):
        self.ecran.blit(self.switches[1 if self.state else 0], (self.x_self, self.y_self))

    # cette fonction est appelée lorsqu'on clique sur le bouton
    def handleClick(self, pos: []):
        switchActuel = self.switches[1 if self.state else 0]
        if (switchActuel.get_width() + self.x_self > pos[0] > self.x_self and pos[
            1] < switchActuel.get_height() + self.y_self and pos[1] > self.y_self):

            if self.state:
                self.modbus.ecrireBit(201, False)
                self.modbus.ecrireBit(202, True)
            else:
                self.modbus.ecrireBit(201, True)
                self.modbus.ecrireBit(202, False)
            self.state = not self.state
            print("state changed "+str(self.state))
