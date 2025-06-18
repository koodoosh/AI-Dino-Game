'''
An AI that plays Google Chrome Dino Game

looks a bit ugly, but will do

Last Modified: July 1, 2020
Time Spent: 10 hrs (lots of debugging)

'''

import pygame
from DinoGame import Dino
from DinoGame import BG
from DinoGame import Cactus
from DinoGame import Pterodactyl
import neat
import random
import pickle
import os

pygame.init()

WIDTH = 800
HEIGHT = 200
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
gen = 0
CLOCK = pygame.time.Clock()
pygame.display.set_caption("AI Plays Chrome Dino Game")


def draw(dinos, bg, cactuses, enemies):
    WINDOW.fill((255, 255, 255))

    bg.draw(WINDOW)

    for dino in dinos:
        dino.draw(WINDOW)

    for cactus in cactuses:
        cactus.draw(WINDOW)

    for enemy in enemies:
        enemy.draw(WINDOW)

    pygame.display.update()

def update(dinos, bg, cactuses, enemies, networks, genomes):
    # counter = 0

    for index, dino in enumerate(dinos):
        #distance to the closest obstacle, width of the obstacle, height of the closest obstacle

        cactuse = cactuses[0]
        if cactuse.x < dino.x:
            cactuse = cactuses[1]
            genomes[index].fitness += 5

        if len(enemies) > 0:
            enemy = enemies[0]

            if enemy.x < dino.x:
                genomes[index].fitness += 5

            if enemy.x < cactuse.x:
                distance = enemy.x - dino.x
                width = enemy.img1.get_width()
                height = HEIGHT - enemy.y
            else:
                distance = cactuse.x - dino.x
                width = cactuse.img.get_width()
                height = HEIGHT - cactuse.y
        else:
            distance = cactuse.x - dino.x
            width = cactuse.img.get_width()
            height = HEIGHT - cactuse.y

        # if counter == 0:
        #     counter += 1
        #     print("distance: " + str(distance))
        #     print("width: " + str(width))
        #     print("height: " + str(height))

        output = networks[index].activate((distance, width, height))

        # #experiment 1: closest to 0
        # a = 0
        # for i in range(1, 3):
        #     if abs(output[a]) > abs(output[i]):
        #         a = i
        #
        # if i == 0:
        #     dino.jump()
        # elif i == 1:
        #     dino.duck()
        # else:
        #     dino.stop_ducking()

        #experiment 2:
        if -0.2 < output[1] < 0.2:
            dino.duck()
        else:
            dino.stop_ducking()

        if -0.2 < output[0] < 0.2:
            dino.jump()

        dino.move()
        genomes[index].fitness += 0.1

    bg.move()

    for cactus in cactuses:
        if cactus.disappear():
            cactuses.remove(cactus)
        else:
            cactus.move()

    for enemy in enemies:
        if enemy.disappear():
            enemies.remove(enemy)
        else:
            enemy.move()

    if len(enemies) > 0:
        if enemies[0].x <= WIDTH * 3 / 4:
            return True
        return False
    return True



def main(genomes, config):
    global gen
    gen += 1

    run = True
    # dino = Dino(50, HEIGHT - 60)

    dinos = []
    neural_networks = []
    dinos_genomes = []

    for id, genome in genomes:
        genome.fitness = 0
        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_networks.append(neural_network)
        dinos.append(Dino(50, 140))
        dinos_genomes.append(genome)

    bg = BG(WIDTH, HEIGHT)
    cactuses = []
    enemy = []

    MIN_GAP = 20
    new_gap = 20

    counter = 0
    enemy_counter = 0
    enemy_gap = 300
    random_gap = random.randint(MIN_GAP, MIN_GAP * 2)
    cactuses.append(Cactus(WIDTH, HEIGHT))

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_DOWN:
            #         for dino in dinos:
            #             dino.duck()
            #     else:
            #         for dino in dinos:
            #             dino.stop_ducking()
            #
            #     if event.key == pygame.K_SPACE:
            #         for dino in dinos:
            #             dino.jump()



        state = update(dinos, bg, cactuses, enemy, neural_networks, dinos_genomes)
        draw(dinos, bg, cactuses, enemy)

        if counter >= random_gap and state == True:
            counter = 0
            random_gap = random.randint(MIN_GAP, MIN_GAP * 2)
            cactuses.append(Cactus(WIDTH, HEIGHT))

        if enemy_counter >= enemy_gap and counter >= 25:
            MIN_GAP = new_gap
            enemy.append(Pterodactyl(WIDTH))
            enemy_gap = random.randint(150, 250)
            enemy_counter = 0

        for dino in dinos:
            if dinos_genomes[dinos.index(dino)].fitness > 10000:
                outFile = open("best_dino.pickle", 'wb')
                pickle.dump(neural_networks[dinos.index(dino)], outFile)
                outFile.close()

                run = False
                break

            if dino.collision_detection(cactuses, enemy):
                del neural_networks[dinos.index(dino)]
                del dinos_genomes[dinos.index(dino)]
                dinos.remove(dino)

        if len(dinos) == 0:
            run = False
            break

        counter += 1
        enemy_counter += 1






def run_best(net, config):

    run = True

    dino = Dino(50, HEIGHT - 60)
    neural_network = net

    bg = BG(WIDTH, HEIGHT)
    cactuses = []
    enemies = []

    MIN_GAP = 20
    new_gap = 20

    counter = 0
    enemy_counter = 0
    enemy_gap = 300
    random_gap = random.randint(MIN_GAP, MIN_GAP * 2)
    cactuses.append(Cactus(WIDTH, HEIGHT))

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        #update
        state = True

        # distance to the closest obstacle, width of the obstacle, height of the closest obstacle

        cactuse = cactuses[0]
        if cactuse.x < dino.x:
            cactuse = cactuses[1]

        if len(enemies) > 0:
            enemy = enemies[0]


            if enemy.x < cactuse.x:
                distance = enemy.x - dino.x
                width = enemy.img1.get_width()
                height = HEIGHT - enemy.y
            else:
                distance = cactuse.x - dino.x
                width = cactuse.img.get_width()
                height = HEIGHT - cactuse.y
        else:
            distance = cactuse.x - dino.x
            width = cactuse.img.get_width()
            height = HEIGHT - cactuse.y

        output = neural_network.activate((distance, width, height))

        if -0.2 < output[1] < 0.2:
            dino.duck()
        else:
            dino.stop_ducking()

        if -0.2 < output[0] < 0.2:
            dino.jump()

        dino.move()

        bg.move()

        for cactus in cactuses:
            if cactus.disappear():
                cactuses.remove(cactus)
            else:
                cactus.move()

        for enemy in enemies:
            if enemy.disappear():
                enemies.remove(enemy)
            else:
                enemy.move()

        if len(enemies) > 0:
            if enemies[0].x >= WIDTH * 3 / 4:
                state = False

        # draw
        WINDOW.fill((255, 255, 255))

        bg.draw(WINDOW)

        dino.draw(WINDOW)

        for cactus in cactuses:
            cactus.draw(WINDOW)

        for enemy in enemies:
            enemy.draw(WINDOW)

        pygame.display.update()

        #manage
        if counter >= random_gap and state == True:
            counter = 0
            random_gap = random.randint(MIN_GAP, MIN_GAP * 2)
            cactuses.append(Cactus(WIDTH, HEIGHT))

        if enemy_counter >= enemy_gap and counter >= 25:
            MIN_GAP = new_gap
            enemies.append(Pterodactyl(WIDTH))
            enemy_gap = random.randint(150, 250)
            enemy_counter = 0

        if dino.collision_detection(cactuses, enemies):
            run = False
            break

        counter += 1
        enemy_counter += 1

    pygame.quit()
    quit()

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # best = pickle.load(open("best_dino.pickle", 'rb'))
    #
    # run_best(best, config)
    #
    # pygame.quit()
    # quit()

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(main, 1000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

    pygame.quit()
    quit()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)