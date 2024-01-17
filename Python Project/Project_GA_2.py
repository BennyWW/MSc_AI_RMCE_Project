"""
Ideas:
-   The genetic algorithm needs to edit or modify features in the game. The game needs to have features that suit the
    5 personality types:
        Openness            :   RPG             - allyHomes, Allies, Enemies
        Conscientiousness   :   FPS             - Enemies, walls, central Hex
        Extroversion        :   Violence        - Enemies
        Agreeableness       :   Adventure       - secrets, trees, walls
        Neuroticism         :   Simulators      - walls, trees, centralHex, secrets

            * RPG needs to have some sort of story or plot to give the player some role playing aspect. The level at
            which this is portrayed can be different depending on the personality profile. The player score more through
            following a plot or getting objectives done.
            * FPS needs to have a shooting and damage mechanism where the player score more for fighting the bots. The
            objectives for this could be shooting up the bots and trying not to die in the process.
            * Violence will be similar to FPS but needs to be more intense, flashy and gory. Objectives will be to just
            kill and kill.
            * Adventure needs to have some aspect of unravelling things through exploring. This means there needs to be
            secrets the player can find. So the objectives will be to find secrets.
            * Simulators need to have some aspect of control over the environment and allowing the player to just do
            whatever they want. Should be a chill experience. The objective would be to travel long distances and
            interact with various things.

-   To represent these aspects in a game can be done using a list of 5 elements. Could be 4 elements since violence and
    fps are very similar. Therefore, the list could look as follows:
        [RPG, FPS, Violence, Adventure, Simulation]
            * Each of these is a value that represents how much of the features need to be there. For example, each of
            the values could be the percentage of each feature in the game: what percentage the feature takes up in the
            game.
                > for example, a player can be in cluster 1 characterized by --% openness, --% conscientiousness,
                --% extroversion, --% agreeableness, and --% neuroticism.
                > these percentages are then fed into the genetic algorithm of the game which then designs tries to
                design a game environment or setup that has the percentages of the features:
                    [O%, C%, E%, A%, N%]
            * The genetic algorithm will then need to generate a random layout of the map and objectives to fit the
            distribution of the features.
        * The chromosome will be a representation of the game environment and features. Since the environment consists
            of hexagonal blocks with various features inside, the chromosome will look as follows:
            [block, block, block, block, block,....]
            Each block will have various features and structures that will be evaluated to determine the fitness of a
            generated environment/set up.
        * Since the objectives will need to be edited as well, there needs to be a way to evaluate both the environment
            and objectives. Therefore, the chromosome would need to have both the environment and the objectives:
            [SetUp]
            SetUp                 :       [block, block, block, block,...]
                block                   :       [Features, ObjectiveScores]
                    Features            :       [numberOfWalls, numberOfSecrets, numberOfTrees, centralHex, allyHome]
                        numberOfWalls   :           * integer (0-6). if binary, can be [000000]
                        numberOfSecrets :           * integer (0-4). if binary, can be [0000]
                        numberOfTrees   :           * integer (0-4). if binary, can be [0000]
                        centralHex      :           * integer (0 or 1). if binary, can be [0/1]
                        allyHome        :           * integer (0 or 1). if binary, can be [0/1]
                        spawns_Ally     :           * integer (0-3). binary [000]
                        spawns_Enemy    :           * integer (0-3). binary [000]
                    ObjectiveScores     :       [O_Score,C_Score,E_Score,A_Score,N_Score]
                        O_Score         :           * float. Represents Openness Score
                        C_Score         :           * float. Represents Conscientiousness Score
                        E_Score         :           * float. Represents Extroversion Score
                        A_Score         :           * float. Represents Agreeableness Score
                        N_Score         :           * float. Represents Neuroticism Score

- Fitness Function:
    - The fitness function needs to check the SetUp and determine whether it fits the gamer personality profile of the
        player. To do this, a good understanding of what the personality profiles need to have in a game is crucial.
        or:
            The algorithm could be flexible to accommodate the percentages in personalities. For example:
                > OPN --%   CSN --%     EXT --%     AGR --%     N --%
                    E.g:
                        Cluster 1: 	OPN 76%		CSN 69%		EXT 54%		AGR 73%		N 75%
                        Cluster 2: 	OPN 83%		CSN 77%		EXT 74%		AGR 83%		N 42%
                        Cluster 3: 	OPN 82%		CSN 65%		EXT 74%		AGR 79%		N 68%
                        Cluster 4: 	OPN 72%		CSN 66%		EXT 54%		AGR 60%		N 45%
                Each of the personality traits can have various levels or percentages. The genetic algorithm could be
                fed this information and finds a way to create e a world with those features by modifying the
                environment and objectives accordingly. An allowance of 5-10% can be given to allows it to create
                more diverse set-ups.
            Making it flexible makes it easier to do. Questions is, why is the initial clustering and prediction needed
            if the algorithm can work regardless?
                Answer: To provide consistency. Some people's results might be too extreme and by doing clustering and
                        building a prediction model from the large dataset, it can be easier to maybe make their
                        results make sense.

    - The function will need to check each block and evaluate its features. The score will be calculated through this
        and if the score is close to the predicted personality score, then that set up will be used.


Summary:
-   Perform cluster analysis on the OCEAN dataset using either machine learning algorithms or deep learning algorithms.
-   Identify what each cluster is characterized by, e.g. the percentages or distribution of the personalities
-   Build a prediction model to predict what cluster/personality profile/gamer profile a new record will belong to.
-   Feed the characteristics into the genetic algorithm and modify the game's features/mechanics to follow the
    characteristics.
-   Evaluate the game:
        * This can be done by the player just to show whether the system works as intended.
        * The feedback will not be used to modify the game features or mechanics further but just to be used as a metric
            to measure how well the system works.
"""

# region Libraries
# Libraries
import pandas as pd
import numpy as np
from typing import List, Any

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random

import matplotlib.pyplot as plt
import csv


# endregion

# region Environment Class
class SetUp:
    """
    - The blocks will need to represent each trait:
    > Openness	        :   Role-Playing Games (RPGs)   :	Objects to unlock abilities
    > Conscientiousness	:   Shooter	                    :   Enemies and walls
    > Extroversion	    :   Violence	                :   Dangerous enemies
    > Agreeableness	    :   Adventure	                :   Ally homes, allies and secrets
    > Neuroticism	    :   Simulation	                :   Trees, grass, and random optional interactional objects

    - Openness can be represented by 3 objects that allow teh player to unlock abilities
    - Conscientiousness can be represented by have 2 enemies, 6 walls and 1 central hexagon
    - Extroversion can be represented by 1 dangerous enemy.
    - Agreeableness can be represented by 1 ally home, 2 allies, and 4 secrets/orbs
    - Neuroticism can be represented by 4 trees, 10 grass, and 3 interactable objects.

    Fitness:
    - Determining the fitness of an individual will be by going through all the blocks, determine the trait levels and
        sum all of them. The result will be the total sum of each trait i.e. total sum of Openness, Conscientiousness,
        Extroversion, etc.
    - The sums will then be converted to percentage of the total possible sum of each trait in the whole set up i.e.
        total sum of openness, total sum of conscientiousness, etc.
    - These percentages are then compared to the expected percentages of the cluster. If the percentage is close to that
        of the cluster, that counts as 1. This means, the best fitness from a set-up needs to be 5 and thus the target
        fitness is 5. If 5 is not attained, the algorithm is unsuccessful since not all traits levels have been captured.
    """

    def __init__(self):
        # Environment features (Within each block)
        self.gridSize = 30
        self.unlockObjs = 3  # O
        self.walls = 6  # C
        self.spawns_Enemy = 2  # C
        self.centralHex = 1  # C
        self.spawns_DangerousEnemy = 1  # E
        self.secrets_orbs = 4  # A
        self.allyHome = 1  # A
        self.spawns_Ally = 2  # A
        self.trees = 4  # N
        self.grass = 10  # N
        self.interactableObjs = 3  # N

        # Scoring and progression (Within each block) || Used to determine fitness
        self.traitLevels_dic = {'O': 0,
                                'C': 0,
                                'E': 0,
                                'A': 0,
                                'N': 0
                                }

        # Mutation
        self.m_IndMultiplier = 0

    def __len__(self):
        length = self.gridSize * self.gridSize
        return length

    def GenerateIndividual(self):
        """
            - Generate extreme individuals (High, medium, or low trait Levels)
            - Take the features from each trait and exaggerate them or suppress them
            - This is by chance i.e. 0.3 chance (0.3, 0.6, 0.9)
            - If it falls in the High low or mid, then generate accordingly
        """
        chance = random.uniform(0.0, 1)
        level = ''
        targetTrait = random.randrange(1, 6)
        if 0 < chance < 0.4:
            level = 'low'
        elif 0.4 < chance < 0.6:
            level = 'mid'
        elif 0.6 < chance < 1:
            level = 'high'

        environment = []

        for i in range(0, len(self)):
            # region mid range
            unlockObjs = random.randrange(0, self.unlockObjs + 1)
            walls = random.randrange(0, self.walls + 1)
            centralHex = random.randrange(0, self.centralHex + 1)
            secrets_orbs = random.randrange(0, self.secrets_orbs + 1)
            trees = random.randrange(0, self.trees + 1)
            grass = random.randrange(0, self.grass + 1)
            interactableObjs = random.randrange(0, self.interactableObjs + 1)
            allyHome = random.randrange(0, self.allyHome + 1)
            spawns_Ally = random.randrange(0, self.spawns_Ally + 1)
            spawns_Enemy = random.randrange(0, self.spawns_Enemy + 1)
            spawns_DangerousEnemy = random.randrange(0, self.spawns_DangerousEnemy + 1)
            # endregion

            # region High range
            if level == 'high':
                unlockObjs = self.unlockObjs
                walls = self.walls
                centralHex = self.centralHex
                secrets_orbs = self.secrets_orbs
                trees = self.trees
                grass = self.grass
                interactableObjs = self.interactableObjs
                allyHome = self.allyHome
                spawns_Ally = self.spawns_Ally
                spawns_Enemy = self.spawns_Enemy
                spawns_DangerousEnemy = self.spawns_DangerousEnemy
            # endregion

            # region High range
            if level == 'low':
                unlockObjs = 0
                walls = 0
                centralHex = 0
                secrets_orbs = 0
                trees = 0
                grass = 0
                interactableObjs = 0
                allyHome = 0
                spawns_Ally = 0
                spawns_Enemy = 0
                spawns_DangerousEnemy = 0
            # endregion

            block = {
                # O
                'unlockObjs': unlockObjs,
                # C
                'walls': walls,
                'centralHex': centralHex,
                'spawns_Enemy': spawns_Enemy,
                # E
                'spawns_DangerousEnemy': spawns_DangerousEnemy,
                # A
                'secrets_orbs': secrets_orbs,
                'allyHome': allyHome,
                'spawns_Ally': spawns_Ally,
                # N
                'trees': trees,
                'grass': grass,
                'interactableObjs': interactableObjs,
            }
            environment.append(block)

        return environment

    def Fitness(self, individual, OCEANLevels, printResults, saveFile, ):
        """
        - Go through the list and check the score of each OCEAN trait in the set-up.
            > Openness	        :   Role-Playing Games (RPGs)   :	Objects to unlock abilities
            > Conscientiousness	:   Shooter	                    :   Enemies and walls
            > Extroversion	    :   Violence	                :   Dangerous enemies
            > Agreeableness	    :   Adventure	                :   Ally homes, allies and secrets/orbs
            > Neuroticism	    :   Simulation	                :   Trees, grass, and random optional interactional objects

        - Calculate the percentage of each from the total OCEAN score (sum of all the trait scores in the set-up)
        - Compare the percentages to the trait percentages of a cluster and penalize if the score is far above or below
            the expected score. An allowance of 5-10% can be given.
        """
        # Main Variables
        traitsCaptured = 0
        OCEAN_setUp_Trait_Levels = {"O": [], "C": [], "E": [], "A": [], "N": []}
        OCEAN_setUp_Trait_Max = {"O": [], "C": [], "E": [], "A": [], "N": []}
        OCEAN_setUp_Trait_Perc = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        OCEAN_setUp_Trait_accuracy = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        OCEAN_setUp_Trait_difference = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}

        for block in individual:
            blockOCEAN = [
                # Openness:                 Objects to unlock abilities
                block['unlockObjs'],
                # Conscientiousness:        Enemies and walls
                (block['spawns_Enemy'] + block['walls'] + block['centralHex']),
                # Extroversion:             Dangerous enemies
                block['spawns_DangerousEnemy'],
                # Agreeableness:            Ally homes, allies and secrets/orbs
                (block['secrets_orbs'] + block['spawns_Ally'] + block['allyHome']),
                # Neuroticism:              Trees, grass, and random optional interactional objects
                (block['trees'] + block['grass'] + block['interactableObjs'])
            ]

            OCEAN_setUp_Trait_Levels['O'].append(blockOCEAN[0])
            OCEAN_setUp_Trait_Levels['C'].append(blockOCEAN[1])
            OCEAN_setUp_Trait_Levels['E'].append(blockOCEAN[2])
            OCEAN_setUp_Trait_Levels['A'].append(blockOCEAN[3])
            OCEAN_setUp_Trait_Levels['N'].append(blockOCEAN[4])

        OCEAN_setUp_Trait_Max['O'] = self.unlockObjs * len(self)
        OCEAN_setUp_Trait_Max['C'] = (self.walls + self.centralHex + self.spawns_Enemy) * len(self)
        OCEAN_setUp_Trait_Max['E'] = self.spawns_DangerousEnemy * len(self)
        OCEAN_setUp_Trait_Max['A'] = (self.allyHome + self.spawns_Ally + self.secrets_orbs) * len(self)
        OCEAN_setUp_Trait_Max['N'] = (self.trees + self.grass + self.interactableObjs) * len(self)

        # Calculate percentages
        OCEAN_setUp_Trait_Perc['O'] = (sum(OCEAN_setUp_Trait_Levels['O']) / OCEAN_setUp_Trait_Max['O']) * 100
        OCEAN_setUp_Trait_Perc['C'] = (sum(OCEAN_setUp_Trait_Levels['C']) / OCEAN_setUp_Trait_Max['C']) * 100
        OCEAN_setUp_Trait_Perc['E'] = (sum(OCEAN_setUp_Trait_Levels['E']) / OCEAN_setUp_Trait_Max['E']) * 100
        OCEAN_setUp_Trait_Perc['A'] = (sum(OCEAN_setUp_Trait_Levels['A']) / OCEAN_setUp_Trait_Max['A']) * 100
        OCEAN_setUp_Trait_Perc['N'] = (sum(OCEAN_setUp_Trait_Levels['N']) / OCEAN_setUp_Trait_Max['N']) * 100

        # Calculate the accuracies
        OCEAN_setUp_Trait_accuracy['O'] = (sum(OCEAN_setUp_Trait_Levels['O']) / OCEANLevels['O']) * 100
        OCEAN_setUp_Trait_accuracy['C'] = (sum(OCEAN_setUp_Trait_Levels['C']) / OCEANLevels['C']) * 100
        OCEAN_setUp_Trait_accuracy['E'] = (sum(OCEAN_setUp_Trait_Levels['E']) / OCEANLevels['E']) * 100
        OCEAN_setUp_Trait_accuracy['A'] = (sum(OCEAN_setUp_Trait_Levels['A']) / OCEANLevels['A']) * 100
        OCEAN_setUp_Trait_accuracy['N'] = (sum(OCEAN_setUp_Trait_Levels['N']) / OCEANLevels['N']) * 100

        for trait in OCEAN_setUp_Trait_Perc:
            if abs(OCEAN_setUp_Trait_Perc[trait] - OCEANLevels[trait]) <= 10:
                traitsCaptured += 1

        # Print Results
        if printResults:
            print("Set up OCEAN scores: ")
            for x in OCEAN_setUp_Trait_Levels:
                print(f"\t{x} : {sum(OCEAN_setUp_Trait_Levels[x])} / {OCEAN_setUp_Trait_Max[x]}")

            print("Set up OCEAN Levels: ")
            for x in OCEAN_setUp_Trait_Perc.keys():
                print(f"\t{x} : {OCEAN_setUp_Trait_Perc[x]} %")

            print("Cluster OCEAN Levels: ")
            for x in OCEANLevels.keys():
                print(f"\t{x} : {OCEANLevels[x]} %")

        return traitsCaptured

    def Mutate(self, individual):
        if random.random() <= .5:
            flipTarget = 1
        else:
            flipTarget = 0
        if flipTarget == 1:
            for i in range(0, len(individual)):
                individual[i]['unlockObjs'] = abs(individual[i]['unlockObjs']-self.unlockObjs)
                individual[i]['walls'] = abs(individual[i]['walls']-self.walls)
                individual[i]['centralHex'] = abs(individual[i]['centralHex']-self.centralHex)
                individual[i]['spawns_Enemy'] = abs(individual[i]['spawns_Enemy']-self.spawns_Enemy)
                individual[i]['spawns_DangerousEnemy'] = abs(individual[i]['spawns_DangerousEnemy']-self.spawns_DangerousEnemy)
                individual[i]['secrets_orbs'] = abs(individual[i]['secrets_orbs']-self.secrets_orbs)
                individual[i]['spawns_Ally'] = abs(individual[i]['spawns_Ally']-self.spawns_Ally)
                individual[i]['allyHome'] = abs(individual[i]['allyHome']-self.allyHome)
                individual[i]['trees'] = abs(individual[i]['trees']-self.trees)
                individual[i]['grass'] = abs(individual[i]['grass']-self.grass)
                individual[i]['interactableObjs'] = abs(individual[i]['interactableObjs']-self.interactableObjs)

        newBlock = self.GenerateIndividual()
        for i in range(int(len(newBlock)*self.m_IndMultiplier), len(newBlock)):
            individual[i]['unlockObjs'] = newBlock[i]['unlockObjs']
            individual[i]['walls'] = newBlock[i]['walls']
            individual[i]['centralHex'] = newBlock[i]['centralHex']
            individual[i]['spawns_Enemy'] = newBlock[i]['spawns_Enemy']
            individual[i]['spawns_DangerousEnemy'] = newBlock[i]['spawns_DangerousEnemy']
            individual[i]['secrets_orbs'] = newBlock[i]['secrets_orbs']
            individual[i]['spawns_Ally'] = newBlock[i]['spawns_Ally']
            individual[i]['allyHome'] = newBlock[i]['allyHome']
            individual[i]['trees'] = newBlock[i]['trees']
            individual[i]['grass'] = newBlock[i]['grass']
            individual[i]['interactableObjs'] = newBlock[i]['interactableObjs']
        return individual,


# endregion

# region Set up Genetic Algorithm
def GeneticAlgorithm(OCEAN_Levels, population_size, generations, pCrossover, pMutation, m_IndMultiplier):
    # Main Variables
    setUp = SetUp()
    setUp.m_IndMultiplier = m_IndMultiplier
    randomSeed = 42
    random.seed(randomSeed)

    # region Set-up
    # Set up the toolbox
    toolbox = base.Toolbox()

    # Define fitness, individual and population creators
    # Create function to evaluate the individual
    # Create function to evaluate the individual
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # Create function to create an individual
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # Define/register a function to create and individual
    toolbox.register("IndividualCreator", tools.initIterate,
                     creator.Individual, setUp.GenerateIndividual)
    # Define/Register a function to generate a population
    toolbox.register("PopulationCreator", tools.initRepeat,
                     list, toolbox.IndividualCreator)

    # Define evaluation function
    def Fitness(individual):
        return setUp.Fitness(individual, OCEAN_Levels, False, False),

    # Set up the genetic operators
    toolbox.register("evaluate", Fitness)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", setUp.Mutate)
    # endregion

    # region Run Genetic Algorithm
    population = toolbox.PopulationCreator(n=population_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    hof = tools.HallOfFame(10)

    population, logbook = eaSimpleWithElitism(population,
                                              toolbox,
                                              cxpb=pCrossover,
                                              mutpb=pMutation,
                                              ngen=generations,
                                              stats=stats,
                                              halloffame=hof,
                                              verbose=True)

    best = hof.items[0]

    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    print('Full Best Environment:')
    print(best)
    print(setUp.Fitness(best, OCEAN_Levels, True, True))

    print('Best Environment: ', best[0:22])
    print(setUp.Fitness(best, OCEAN_Levels, True, False))
    print('Worst Environment: ', hof.items[len(hof.items) - 1][0:10])
    print(setUp.Fitness(hof.items[len(hof.items) - 1], OCEAN_Levels, True, False))

    plt.plot(maxFitnessValues, color="red")
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Max/average fitness')
    plt.ylabel('Generations')
    plt.show()
    # endregion


# endregion

# region EASimple ------------------------------------------------------------------------------------------------------
def eaSimpleWithElitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
                        halloffame=None, verbose=__debug__):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
    halloffame is used to implement an elitism mechanism. The individuals contained in the
    halloffame are directly injected into the next generation and are not subject to the
    genetic operators of selection, crossover and mutation.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(halloffame.items)

        # Update the hall of fame with the generated individuals
        halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook


# endregion

def Test():
    environmentSetUp = SetUp()
    testEnv = environmentSetUp.GenerateIndividual()
    # for block in testEnv:
    #     print(block)
    # print(len(testEnv))

    # OCEAN_levels_C1 = {"O": 82, "C": 65, "E": 74, "A": 79, "N": 68}
    # OCEAN_levels_C2 = {"O": 83, "C": 77, "E": 73, "A": 83, "N": 42}
    OCEAN_levels_C3 = {"O": 72, "C": 66, "E": 54, "A": 60, "N": 46}
    # OCEAN_levels_C4 = {"O": 76, "C": 69, "E": 54, "A": 73, "N": 75}
    print(environmentSetUp.Fitness(testEnv, OCEAN_levels_C3, True, False))

    GeneticAlgorithm(OCEAN_levels_C3, 50, 50, .5, .8, .5)
    return


def Main():
    OCEAN_levels_C1 = {"O": 82, "C": 65, "E": 74, "A": 79, "N": 68}
    OCEAN_levels_C2 = {"O": 83, "C": 77, "E": 73, "A": 83, "N": 42}
    OCEAN_levels_C3 = {"O": 72, "C": 66, "E": 54, "A": 60, "N": 46}
    OCEAN_levels_C4 = {"O": 76, "C": 69, "E": 54, "A": 73, "N": 75}
    GeneticAlgorithm(OCEAN_levels_C2, 50, 100, 1, .8, 0)
    return


if __name__ == "__main__":
    Test()
    # Main()
