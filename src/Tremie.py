# Classe pour gérer la création de composants graphiques

import pygame
from modbus import Modbus
from utils import *


# crée une classe nommée composants


class Tremie:
    largeur_barre_chargement = 420
    hauteur_bordure_chargement = 45
    epaiss_bordure = 3
    capacites = [5100, 5100, 10200]
    adresses_debits = [11, 12, 13]
    adresses_conv = [303, 304, 305]

    leds_convoyeur = [pygame.transform.scale(pygame.image.load("assets/blink.svg"), (25, 25)),
                      pygame.transform.scale(pygame.image.load("assets/stop.svg"), (30, 30))]

    icones_debits = [pygame.transform.scale(pygame.image.load("assets/plus.svg"), (25, 25)),
                      pygame.transform.scale(pygame.image.load("assets/minus.svg"), (25, 25))]


    def __init__(self, num, ecran, x_debut_bordure_chargement, y_debut_bordure_chargement, couleur, x_titre_tremie,
                 y_titre_tremie, modbus: Modbus):
        self.num = num
        self.ecran = ecran
        self.couleur = couleur
        self.x = x_debut_bordure_chargement
        self.y = y_debut_bordure_chargement
        self.x_titre_tremie = x_titre_tremie
        self.y_titre_tremie = y_titre_tremie
        self.modbus = modbus
        self.blink = False
        self.buttons = []

    def calcul_niveau(self):
        if self.num != 2:
            return (self.capacites[self.num] - ((self.modbus.lireRegistre(self.adresses_debits[self.num]) / sum(
                [self.modbus.lireRegistre(ad) for ad in self.adresses_debits])) * self.modbus.lireRegistre(30))) / self.capacites[self.num]
        else:
            return self.modbus.lireRegistre(30) / self.capacites[2]

    def draw(self):
        font = pygame.font.Font(None, 33)

        texte = font.render("Trémie " + str(self.num + 1), 1, BLACK)

        niveau_tremie = self.calcul_niveau()
        # if (niveau_tremie > 1):
        #     print(niveau_tremie)
        #     niveau_tremie = 1

        texte2 = font.render(str(round(niveau_tremie * 100, 1)) + " %", 1, BLACK)

        self.ecran.blit(texte, (self.x_titre_tremie, self.y_titre_tremie))
        # pygame.draw.line(self.ecran, BLACK, (10, self.y_titre_tremie + 30),
        #                  (TAILLE_FENETRE[0] - 10, self.y_titre_tremie + 30), self.epaiss_bordure)  # barre horizontale
        # un rectangle plutôt
        pygame.draw.rect(self.ecran, BLACK, (self.x, self.y, self.largeur_barre_chargement + self.epaiss_bordure,
                                             self.hauteur_bordure_chargement), self.epaiss_bordure)

        pygame.draw.line(self.ecran, BLACK, (self.x, self.y), (self.x, self.y + self.hauteur_bordure_chargement),
                         self.epaiss_bordure)
        pygame.draw.line(self.ecran, BLACK, (self.x + self.largeur_barre_chargement + self.epaiss_bordure, self.y), (
        self.x + self.largeur_barre_chargement + self.epaiss_bordure, self.y + self.hauteur_bordure_chargement),
                         self.epaiss_bordure)
        pygame.draw.rect(self.ecran, self.couleur, (
        self.x + self.epaiss_bordure, self.y + self.epaiss_bordure, niveau_tremie * self.largeur_barre_chargement,
        self.hauteur_bordure_chargement - self.epaiss_bordure * 2))
        self.ecran.blit(texte2, (self.x + self.largeur_barre_chargement // 2 - texte.get_width() // 2,
                                 self.y + self.hauteur_bordure_chargement // 2 - texte.get_height() // 2))

        texte3 = font.render("Débit : "+str(self.modbus.lireRegistre(self.adresses_debits[self.num])) + " /s", 1, BLACK)
        self.ecran.blit(texte3, (self.x + self.largeur_barre_chargement//2 - texte3.get_width()//2,
                                 self.y + self.hauteur_bordure_chargement + 18))

        # affichage des boutons pour augmenter ou diminuer le débit
        # bouton plus

        self.buttons.append(self.ecran.blit(self.icones_debits[0], (self.x + self.largeur_barre_chargement//2 + 10 + texte3.get_width() //2,
                                                self.y + self.hauteur_bordure_chargement + 18 - (25//2 -texte3.get_height()//2))))

        # bouton moins
        self.buttons.append(self.ecran.blit(self.icones_debits[1], (self.x + self.largeur_barre_chargement//2 - 10 - 25 - texte3.get_width() //2,
                                                self.y + self.hauteur_bordure_chargement + 18 - (25//2 -texte3.get_height()//2))))

        if self.modbus.lireBit(self.adresses_conv[self.num]):
            if self.blink:
                self.ecran.blit(self.leds_convoyeur[0], (self.x + texte.get_width() + 10, self.y_titre_tremie - (
                            self.leds_convoyeur[0].get_height() / 2 - texte.get_height() / 2)))
            self.blink = not self.blink

        else:
            self.ecran.blit(self.leds_convoyeur[1], (self.x + texte.get_width() + 10,
                                                     self.y_titre_tremie - (
                                                             self.leds_convoyeur[
                                                                 1].get_height() / 2 - texte.get_height() / 2)))

    def handleClick(self, pos: []):
        if (self.buttons[0].collidepoint(pos)):
            self.modbus.ecrireRegistre(self.adresses_debits[self.num], self.modbus.lireRegistre(self.adresses_debits[self.num]) + 1)
            return True

        elif (self.buttons[1].collidepoint(pos)):
            self.modbus.ecrireRegistre(self.adresses_debits[self.num], self.modbus.lireRegistre(self.adresses_debits[self.num]) - 1)
            return True

        return False
