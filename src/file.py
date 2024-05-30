import time

from modbus import Modbus
import pygame

def main():
    modbus = Modbus()

    # Définir les couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pygame.init()

    ecran = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("supervision")
    continuer = True
    pos = []
    # modbus.ecrireBit(306, True)
    while continuer:
        ecran.fill(WHITE)

        font = pygame.font.Font(None, 36)
    #     récupérer les mouvements de la souris et les afficher en console

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

    #     écrire du texte dans la fenêtre

        # texte = font.render("Position de la souris : " + str(pos), 1, (0,0,0))
        # # afficher le texte au centre de la fenêtre
        # ecran.blit(texte, (640//2 - texte.get_width()//2, 480//2 - texte.get_height()//2 ))

        y = 50
        text = font.render(f"Cycle remplissage : {'En cours' if sup_cycr else 'Arrêté'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Cycle vidange : {'En cours' if sup_cycv else 'Arrêté'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Marche/Arrêt : {'En marche' if sup_cycm else 'Arrêté'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Convoyeur 1 : {'En marche' if sup_conv1 else 'Arrêté'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Debit convoyeur 1 : {debit_1}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        # placons des boutons pour augmenter ou diminuer le débit
        # bouton plus
        plus=pygame.draw.rect(ecran, GREEN, (400, y - text.get_height()//2 + 10, 40, 40))
        text = font.render("+", True, BLACK)
        ecran.blit(text, (400 + 10, y - text.get_height()//2 + 10))
        # bouton moins

        text = font.render(f"Convoyeur 2 : {'En marche' if sup_conv2 else 'Arrêté'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Debit convoyeur 2 : {debit_2}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Convoyeur 3 : {'En marche' if sup_conv3 else 'Arrêté'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Debit convoyeur 3 : {debit_3}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Pilotage distance : {'Autorisé' if sup_dist else 'Interdit'}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        text = font.render(f"Niveau trémie 3 : {sup_niv_c}", True, BLACK)
        ecran.blit(text, (20, y))
        y+= 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("clic")
            if event.type == pygame.KEYDOWN:
                print("touche appuyée")
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


# 3 rectangles blanc avec bordures noires pour représenter les 3 trémies
        # la 1ère tout à gauche
        # pygame.draw.rect(ecran, BLACK, (50, 50, HAUTEUR_TREMIE, HAUTEUR_TREMIE), LARGEUR_BORDURE)
        # pygame.draw.rect(ecran, YELLOW, (50+LARGEUR_BORDURE, 50+LARGEUR_BORDURE, HAUTEUR_TREMIE-2*LARGEUR_BORDURE, HAUTEUR_TREMIE-2*LARGEUR_BORDURE))
        #
        # # la 2e tout à droite
        # pygame.draw.rect(ecran, BLACK, (TAILLE_FENETRE[0]-50-HAUTEUR_TREMIE, 50, HAUTEUR_TREMIE, HAUTEUR_TREMIE), LARGEUR_BORDURE)
        # pygame.draw.rect(ecran, YELLOW, (TAILLE_FENETRE[0]-50-HAUTEUR_TREMIE+LARGEUR_BORDURE, 50+LARGEUR_BORDURE, HAUTEUR_TREMIE-2*LARGEUR_BORDURE, HAUTEUR_TREMIE-2*LARGEUR_BORDURE))
        #
        # # la 3e au milieu en bas
        # pygame.draw.rect(ecran, BLACK, (TAILLE_FENETRE[0]//2-HAUTEUR_TREMIE//2, TAILLE_FENETRE[1]-50-HAUTEUR_TREMIE, HAUTEUR_TREMIE, HAUTEUR_TREMIE), LARGEUR_BORDURE)
        # pygame.draw.rect(ecran, YELLOW, (TAILLE_FENETRE[0]//2-HAUTEUR_TREMIE//2+LARGEUR_BORDURE, TAILLE_FENETRE[1]-50-HAUTEUR_TREMIE+LARGEUR_BORDURE, HAUTEUR_TREMIE-2*LARGEUR_BORDURE, HAUTEUR_TREMIE-2*LARGEUR_BORDURE))
        #
        # # traçons une ligne pour la base de la cuve
        # pygame.draw.line(ecran, BLACK, (50, TAILLE_FENETRE[1]-50), (200, TAILLE_FENETRE[1]-50), 3)
        # # les arcs pour les surfaces latérales
        # pygame.draw.arc(ecran, BLACK, (50, TAILLE_FENETRE[1]-50))