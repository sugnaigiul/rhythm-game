import pygame
import random
import math
import csv
from player import Player
from ship import Ship
from sphere import Sphere
from game_utils import get_player_initials, replay

pygame.init()

# On crée la fenêtre
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Mon jeu de rythme")
replayBool = True

# Création des rectangles inclinés pour former une route
# Rectangle gauche
left_rect = pygame.Surface((800, 20), pygame.SRCALPHA)  # Utilise un Surface avec transparence
left_rect.fill((255, 255, 255))
left_rect = pygame.transform.rotate(left_rect, 65)  # Inclinée de 30 degrés
left_rect_rect = left_rect.get_rect(center=(100, 300))  # Place le rectangle en centre gauche

# Rectangle droit
right_rect = pygame.Surface((800, 20), pygame.SRCALPHA)
right_rect.fill((255, 255, 255))
right_rect = pygame.transform.rotate(right_rect, -65)  # Inclinée de -30 degrés
right_rect_rect = right_rect.get_rect(center=(700, 300))  # Place le rectangle en centre droit

while replayBool :

    # Initialisation du joueur
    player_initials = get_player_initials(screen)
    player = Player(player_initials)
    player.load_data()
    player.num_games += 1

    # Initialisation du vaisseau
    ship = Ship()

    # Liste pour stocker les sphères ennemies
    spheres = []
    spawn_delay = 30  # Délai en frames pour créer de nouvelles sphères
    frame_count = 0
    score = 0  # Score du joueur pour la partie en cours
    highscore = player.high_score # Highscore du joueur depuis son CSV

    # Police pour l'affichage du score
    font = pygame.font.Font(None, 36)

    # Début de la boucle de jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship.move("left")
                elif event.key == pygame.K_RIGHT:
                    ship.move("right")
        
        # Remplissage de l'écran en noir
        screen.fill((0, 0, 0))
        # On dessine les rectangles inclinés
        screen.blit(left_rect, left_rect_rect)
        screen.blit(right_rect, right_rect_rect)
        
        # Incrémentation du score par le temps de jeu
        score += 1

        # Création de nouvelles sphères à intervalles réguliers
        frame_count += 1
        if frame_count >= spawn_delay:
            spheres.append(Sphere())
            frame_count = 0

        # Réduction de l'intervalle entre les temps d'apparition des sphères
        spawn_delay = spawn_delay - 0.01
        
        # Mouvement et affichage des sphères
        for sphere in spheres:
            sphere.move()
            sphere.draw(screen)
            
            # Vérification de collision avec la nouvelle taille de la sphère
            if sphere.collides_with(ship):
                print("Collision! Game Over!")
                if score > highscore:
                    player.high_score = score
                player.save_data()
                running = False
            
            # Suppression des sphères en dehors de l'écran
            if sphere.y - sphere.radius > 600:  # Inclut le rayon dans le test de sortie d'écran
                spheres.remove(sphere)
                score += 100  # Ajoute des points pour chaque sphère esquivée
        

        # Affichage du texte "Score" en haut à droite
        label_text = font.render("Score", True, (255, 255, 255))
        screen.blit(label_text, (10, 10))

        # Affichage de la valeur de score en dessous
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 40))

        # Affichage du texte "High score" en haut à droite
        label_text = font.render("High score", True, (255, 255, 255))
        screen.blit(label_text, (10, 70))

        # Affichage de la valeur de score en dessous
        score_text = font.render(str(highscore), True, (255, 255, 255))
        screen.blit(score_text, (10, 100))

        # Affichage du vaisseau
        ship.draw(screen)
        
        # Mise à jour de l'écran
        pygame.display.flip()
        clock.tick(60)

    replayBool = replay(screen, score)

pygame.quit()