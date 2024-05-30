import time

from modbus import Modbus
from Tremie import Tremie
from Switch import Switch
from utils import *
import pygame


def main():
    modbus = Modbus()
    x_debut_bordure_chargement = TAILLE_FENETRE[0] * 0.05
    y_debut_bordure_chargement = 55
    largeur_barre_chargement = 420
    hauteur_bordure_chargement = 45
    epaiss_bordure = 3

    pygame.init()

    ecran = pygame.display.set_mode(TAILLE_FENETRE)


    tremie1 = Tremie(0, ecran, x_debut_bordure_chargement, y_debut_bordure_chargement + 10, RED,
                     x_debut_bordure_chargement, 20, modbus)
    tremie2 = Tremie(1, ecran, x_debut_bordure_chargement,
                     y_debut_bordure_chargement + hauteur_bordure_chargement + 130+20,
                     BLUE, x_debut_bordure_chargement, 100 + hauteur_bordure_chargement + 45+20, modbus)
    tremie3 = Tremie(2, ecran, x_debut_bordure_chargement,
                     y_debut_bordure_chargement + 2 * hauteur_bordure_chargement + 240 + 40, pygame.Color(RED).lerp(BLUE, modbus.lireRegistre(12) / (modbus.lireRegistre(11) + modbus.lireRegistre(12))),
                     x_debut_bordure_chargement,
                     30 * 2 + 2 * hauteur_bordure_chargement + 200+40, modbus)

    switch = Switch(ecran, modbus)

    pygame.display.set_caption("Supervision")

    continuer = True

    # modbus.ecrireBit(306, True)
    while continuer:
        ecran.fill(WHITE)
        # Lire les valeurs des variables accessibles en lecture
        sup_cycr = modbus.lireBit(300)  # État cycle remplissage
        sup_cycv = modbus.lireBit(301)  # État cycle vidange
        sup_cycm = modbus.lireBit(302)  # État Marche/Arrêt
        sup_conv1 = modbus.lireBit(303)  # État convoyeur 1
        sup_conv2 = modbus.lireBit(304)  # État convoyeur 2
        sup_conv3 = modbus.lireBit(305)  # État convoyeur 3

        debit_1 = modbus.lireRegistre(11)
        debit_2 = modbus.lireRegistre(12)
        debit_3 = modbus.lireRegistre(13)

        sup_dist = modbus.lireBit(306)  # Autorisation pilotage distance
        sup_niv_c = modbus.lireRegistre(30)  # Niveau trémie 3

        tremie1.draw()

        tremie2.draw()

        tremie3.draw()

        switch.draw()

        # afficher un texte indiquant le cycle en cours
        font = pygame.font.Font(None, 36)
        y = 600
        text = font.render(f"Cycle : {'Remplissage' if sup_cycr else 'Vidange'}", True, BLACK)
        ecran.blit(text, (x_debut_bordure_chargement, y))



        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                switch.handleClick(event.pos)
                tremie3.handleClick(event.pos)
                if tremie1.handleClick(event.pos) or tremie2.handleClick(event.pos) :
                    tremie3.couleur = pygame.Color(YELLOW).lerp(GREEN, modbus.lireRegistre(12) / (modbus.lireRegistre(11) + modbus.lireRegistre(12)))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    continuer = False
                if event.key == pygame.K_m:
                    modbus.ecrireBit(201, True)
                    modbus.ecrireBit(202, False)
                    print("Marche: ", sup_cycm)
                if event.key == pygame.K_s:
                    modbus.ecrireBit(201, False)
                    modbus.ecrireBit(202, True)
                    print("Arrêt: ", sup_cycm)

        time.sleep(0.1)
        # pygame.display.flip()
    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
