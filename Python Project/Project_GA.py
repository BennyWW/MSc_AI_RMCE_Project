"""
Ideas:
-   The genetic algorithm needs to edit or modify features in the game. The game needs to have features that suit the
    5 personality types:
        > Openness	        :   Role-Playing Games (RPGs)   :	Objects to unlock abilities
        > Extroversion	    :   Shooter	                    :   Enemies and walls
        > Neuroticism	    :   Action  	                :   Dangerous enemies
        > Agreeableness	    :   Adventure	                :   Ally homes, allies and secrets/orbs
        > Conscientiousness :   Simulation	                :   Trees, grass, and random optional interactional objects

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
            SetUp                           :       [block, block, block, block,...]
                block                       :       [Features]
                    Features                :       [numberOfWalls, numberOfSecrets, numberOfTrees, centralHex, allyHome]
                        Walls               :       * integer (0-6). if binary, can be [00...]
                        Secrets             :       * integer (0-4). if binary, can be [00...]
                        Trees               :       * integer (0-4). if binary, can be [00...]
                        CentralHex          :       * bool. if binary, can be [0/1]
                        AllyHome            :       * bool. if binary, can be [0/1]
                        AllySpawns          :       * binary [00...]
                        EnemySpawns         :       * binary [00...]
                        dangerousEnemySpawns:       * binary [00...]
                        grass               :       * binary [00...]
                        unlockObjs          :       * binary [00...]
                        interactableObjs    :       * binary [00...]

- Fitness Function:
    - The fitness function needs to check the map and determine whether it fits the player personality profile.
    - To do this, a good understanding of what the personality profiles need to have in the game is crucial.
            The algorithm could be flexible to accommodate the percentages in personalities. For example:
                > OPN --%   CSN --%     EXT --%     AGR --%     N --%
                    E.g:
                        Cluster 1: 	OPN 76%		CSN 69%		EXT 54%		AGR 73%		N 75%
                        Cluster 2: 	OPN 83%		CSN 77%		EXT 74%		AGR 83%		N 42%
                        Cluster 3: 	OPN 82%		CSN 65%		EXT 74%		AGR 79%		N 68%
                        Cluster 4: 	OPN 72%		CSN 66%		EXT 54%		AGR 60%		N 45%

                        Cluster 1: 	OPN 70%		CSN 65%		EXT 54%		AGR 61%		N 46%
                        Cluster 2: 	OPN 82%		CSN 64%		EXT 74%		AGR 79%		N 68%
                        Cluster 3: 	OPN 76%		CSN 68%		EXT 54%		AGR 72%		N 75%
                        Cluster 4: 	OPN 83%		CSN 77%		EXT 73%		AGR 83%		N 42%
                Each of the personality traits can have various levels or percentages. The genetic algorithm could be
                fed this information and finds a way to create a world with those features by modifying the
                environment and objectives accordingly. An allowance of 5-10% can be given to allows it to create
                more diverse set-ups.
            Making it flexible makes it easier to do. Question is, why is the initial clustering and prediction needed
            if the algorithm can work regardless?
                Answer: To provide consistency. Some people's results might be too extreme and by doing clustering and
                        building a prediction model from the large dataset, it can be easier to make their
                        results make sense or provide a balanced experience.

    - The function will need to check each block and evaluate its features. The score will be calculated through this
        and if the score is close to the predicted personality score, then that set up will be used.

Summary:
-   Perform cluster analysis on the OCEAN dataset using either machine learning algorithms or deep learning algorithms.
-   Identify what each cluster is characterized by, e.g. the percentages or distribution of the personalities
-   Build a prediction model to predict what cluster/personality profile/gamer profile a new record will belong to.
-   Feed the characteristics into the genetic algorithm and modify the game's features/mechanics to follow the
    characteristics.

"""
# region Libraries
# Libraries
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
    def __init__(self):
        # Environment features (Within each block)
        self.gridSize = 30
        self.unlockObjs = [0, 0, 0]
        self.walls = [0, 0, 0, 0, 0, 0]
        self.secrets_orbs = [0, 0, 0, 0]
        self.trees = [0, 0, 0, 0]
        self.interactableObjs = [0, 0, 0]
        self.grass = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.centralHex = [0]
        self.allyHome = [0]
        self.spawns_Ally = [0]
        self.spawns_Enemy = [0]
        self.spawns_DangerousEnemy = [0]
        self.features = [self.unlockObjs,
                         self.walls,
                         self.secrets_orbs,
                         self.trees,
                         self.interactableObjs,
                         self.grass,
                         self.centralHex,
                         self.allyHome,
                         self.spawns_Ally,
                         self.spawns_Enemy,
                         self.spawns_DangerousEnemy
                         ]
        # Main features [binary]
        self.block = [item for sublist in self.features for item in
                      (sublist if isinstance(sublist, list) else [sublist])]

        # Scoring and progression (Within each block) || Used to determine fitness
        self.O_Score = 0
        self.C_Score = 0
        self.E_Score = 0
        self.A_Score = 0
        self.N_Score = 0
        self.objectiveScores = [self.O_Score,
                                self.C_Score,
                                self.E_Score,
                                self.A_Score,
                                self.N_Score]
        self.enemyBots = 0
        self.allyBots = 0

        # Mutation
        self.m_IndMultiplier = .5

    def __len__(self):
        """
        - block = [000000 0000 0000 0 0] (22 indices)
        - The map is a 30 X 30 grid of blocks. That means there are a total of 900 blocks and since each block has 22
            indices, the length of the binary list will be 900 * 22 =  indices
        """
        length = len(self.block) * self.gridSize * self.gridSize
        return length

    def GetBlocks(self, binaryList):
        blocks = [binaryList[i:i + len(self.block)] for i in range(0, len(binaryList), len(self.block))]
        return blocks

    def GetBlockFeatures(self, block, printFeatures):
        # Sum of set up features
        walls = []
        secrets = []
        trees = []
        centralHexes = []
        allyHomes = []
        allySpawns = []
        enemySpawns = []
        dangerousEnemySpawns = []
        grass = []
        unlockObjs = []
        interactableObjs = []

        # region Get all features from each block in set up
        # Check walls
        for i in range(0,
                       len(self.walls)):
            walls.append(block[i])
        # Check secrets
        for i in range(len(self.walls),
                       len(self.walls) + len(self.secrets_orbs)):
            secrets.append(block[i])
        # Check trees
        for i in range(len(self.walls) + len(self.secrets_orbs),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees)):
            trees.append(block[i])
        # Check centralHex
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex)):
            centralHexes.append(block[i])
        # Check allyHomes
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome)):
            allyHomes.append(block[i])
        # Check Ally spawns
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally)):
            allySpawns.append(block[i])
        # Check Enemy Spawns
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy)):
            enemySpawns.append(block[i])
        # Check Dangerous Enemy Spawns
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy)):
            dangerousEnemySpawns.append(block[i])
        # Check Grass
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy) + len(self.grass)):
            grass.append(block[i])
        # Check UnlockObjs
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy) + len(self.grass),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy) + len(self.grass) + len(self.unlockObjs)):
            unlockObjs.append(block[i])
        # Check InteractableObjs
        for i in range(len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy) + len(self.grass) + len(self.unlockObjs),
                       len(self.walls) + len(self.secrets_orbs) + len(self.trees) + len(self.centralHex) +
                       len(self.allyHome) + len(self.spawns_Ally) + len(self.spawns_Enemy) +
                       len(self.spawns_DangerousEnemy) + len(self.grass) + len(self.unlockObjs) +
                       len(self.interactableObjs)):
            interactableObjs.append(block[i])

        if printFeatures:
            # (walls + secrets_orbs + trees + centralHex + allyHome + spawns_Ally + spawns_Enemy +
            #                            spawns_DangerousEnemy + grass + unlockObjs + interactableObjs)
            print(
                f'Walls: \t\t{walls}\n'
                f'Secrets: \t\t{secrets}\n'
                f'Trees: \t\t{trees}\n'
                f'CentralHex: \t\t{centralHexes}\n'
                f'AllyHome: \t\t{allyHomes}\n'
                f'AllySpawns: \t\t{allySpawns}\n'
                f'EnemySpawns: \t\t{enemySpawns}\n'
                f'DangerousEnemySpawns: \t\t{dangerousEnemySpawns}\n'
                f'Grass: \t\t{grass}\n'
                f'UnlockObjs: \t\t{unlockObjs}\n'
                f'InteractableObjs: \t\t{interactableObjs}\n'
            )
        return walls, secrets, trees, centralHexes, allyHomes, allySpawns, enemySpawns, dangerousEnemySpawns, \
            grass, unlockObjs, interactableObjs

    def GenerateIndividual(self):
        individual = []
        '''
        > Openness	        :   Role-Playing Games (RPGs)   :	Objects to unlock abilities
        > Neuroticism	    :   Shooter	                    :   Enemies and walls
        > Extroversion	    :   Action  	                :   Dangerous enemies
        > Agreeableness	    :   Adventure	                :   Ally homes, allies and secrets/orbs
        > Conscientiousness :   Simulation	                :   Trees, grass, and random optional interactional objects

            - Generate extreme individuals (High, medium, or low trait Levels)
            - Take the features from each trait and exaggerate them or suppress them
            - This is by chance i.e. 0.3 chance (0.3, 0.6, 0.9)
            - If it falls in the High low or mid, then generate accordingly
        '''
        chance = random.uniform(0.0, 1)
        level = ''
        targetTrait = random.randrange(1, 6)
        if 0 < chance < 0.4:
            level = 'low'
        elif 0.4 < chance < 0.6:
            level = 'mid'
        elif 0.6 < chance < 1:
            level = 'high'

        O_chance = random.randint(0, 1)
        C_chance = random.randint(0, 1)
        E_chance = random.randint(0, 1)
        A_chance = random.randint(0, 1)
        N_chance = random.randint(0, 1)

        for i in range(0, self.gridSize * self.gridSize):
            if O_chance > 0:
                unlockObjs = [1] * len(self.unlockObjs)
            else:
                unlockObjs = [0] * len(self.unlockObjs)

            if N_chance > 0:
                walls = [1] * len(self.walls)
                centralHex = [1] * len(self.centralHex)
                spawns_Enemy = [1] * len(self.spawns_Enemy)
            else:
                walls = [0] * len(self.walls)
                centralHex = [0] * len(self.centralHex)
                spawns_Enemy = [0] * len(self.spawns_Enemy)

            if E_chance > 0:
                spawns_DangerousEnemy = [1] * len(self.spawns_DangerousEnemy)
            else:
                spawns_DangerousEnemy = [0] * len(self.spawns_DangerousEnemy)

            if A_chance > 0:
                allyHome = [1] * len(self.allyHome)
                spawns_Ally = [1] * len(self.spawns_Ally)
                secrets_orbs = [1] * len(self.secrets_orbs)
            else:
                allyHome = [0] * len(self.allyHome)
                spawns_Ally = [0] * len(self.spawns_Ally)
                secrets_orbs = [0] * len(self.secrets_orbs)

            if C_chance > 0:
                trees = [1] * len(self.trees)
                grass = [1] * len(self.grass)
                interactableObjs = [1] * len(self.interactableObjs)
            else:
                trees = [0] * len(self.trees)
                grass = [0] * len(self.grass)
                interactableObjs = [0] * len(self.interactableObjs)

            binary_list = (walls + secrets_orbs + trees + centralHex + allyHome + spawns_Ally + spawns_Enemy +
                           spawns_DangerousEnemy + grass + unlockObjs + interactableObjs)
            individual += binary_list

        blocks = self.GetBlocks(individual)
        newIndividual = []
        for block in blocks:
            randomIndex = random.randint(0, len(blocks) - 1)
            for i in range(0, random.randint(0, len(block) - 1)):
                block[i] = blocks[randomIndex][i]

        newIndividual = [item for sublist in blocks for item in sublist]

        return newIndividual

    def Mutate(self, individual):
        # Flip most of 1 or 0
        flipTarget = 0
        if random.random() <= .5:
            flipTarget = 1
        else:
            flipTarget = 0
        for i in range(len(individual)):
            if individual[i] != flipTarget:
                if random.randrange(0, 10) <= 8:
                    individual[i] = flipTarget

        newIndividual = self.GenerateIndividual()
        for i in range(int(len(individual) * self.m_IndMultiplier), len(newIndividual)):
            individual[i] = newIndividual[i]

        blocks = self.GetBlocks(individual)
        random.shuffle(blocks)
        combinedList = []
        for block in blocks:
            combinedList += block
        for i in range(0, len(combinedList)):
            individual[i] = combinedList[i]

        return individual,

    def Fitness(self, setUpList, OCEAN_Levels, printResults, saveFile):
        """
        - Go through the list and check the score of each OCEAN trait in the set-up.
        > Openness	        :   Role-Playing Games (RPGs)       :	Objects to unlock abilities
        > Neuroticism	    :   Action  	                    :   Dangerous enemies
        > Extroversion	    :   Shooter	                        :   Enemies and walls
        > Agreeableness	    :   Adventure	                    :   Ally homes, allies and secrets/orbs
        > Conscientiousness :   Simulation	                    :   Trees, grass, and random optional interactional objects

        - Calculate the percentage of each from the total OCEAN score (sum of all the trait scores in the set-up)
        - Compare the percentages to the trait percentages of a cluster and penalize if the score is far above or below
            the expected score. An allowance of 5-10% can be given.
        """
        # Main Variables
        fitness = 0
        blocks = self.GetBlocks(setUpList)
        OCEAN_setUp = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        OCEAN_setUp_Max = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        OCEAN_setUp_Trait_levels = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}

        # Sum of set up features
        walls = []
        secrets = []
        trees = []
        centralHexes = []
        allyHomes = []
        allySpawns = []
        enemySpawns = []
        dangerousEnemySpawns = []
        grass = []
        unlockObjs = []
        interactableObjs = []

        # region Get all features from each block in set up
        for block in blocks:
            walls_block, secrets_block, trees_block, centralHexes_block, allyHomes_block, allySpawns_block, enemySpawns_block, dangerousEnemySpawns_block, \
                grass_block, unlockObjs_block, interactableObjs_block = self.GetBlockFeatures(block, False)

            walls += walls_block
            secrets += secrets_block
            trees += trees_block
            centralHexes += centralHexes_block
            allyHomes += allyHomes_block
            allySpawns += allySpawns_block
            enemySpawns += enemySpawns_block
            dangerousEnemySpawns += dangerousEnemySpawns_block
            grass += grass_block
            unlockObjs += unlockObjs_block
            interactableObjs += interactableObjs_block

        environ_info = (f'walls:      {sum(walls)} / {len(walls)}\n'
                        f'secrets:    {sum(secrets)} / {len(secrets)}\n'
                        f'trees:      {sum(trees)}  / {len(trees)}\n'
                        f'centralHex: {sum(centralHexes)} / {len(centralHexes)}\n'
                        f'allyHome:   {sum(allyHomes)} / {len(allyHomes)}\n'
                        f'spawns_Ally:   {sum(allySpawns)} / {len(allySpawns)}\n'
                        f'spawns_Enemy:   {sum(enemySpawns)} / {len(enemySpawns)}\n'
                        f'spawns_DangerousEnemy:   {sum(dangerousEnemySpawns)} / {len(dangerousEnemySpawns)}\n'
                        f'grass:   {sum(grass)} / {len(grass)}\n'
                        f'unlockObjs:   {sum(unlockObjs)} / {len(unlockObjs)}\n'
                        f'interactableObjs:   {sum(interactableObjs)} / {len(interactableObjs)}\n'
                        )

        if printResults:
            print(environ_info)

            print(f'% walls: {sum(walls) / len(setUpList) * 100}\n'
                  f'% secrets: {sum(secrets) / len(setUpList) * 100}\n'
                  f'% trees: {sum(trees) / len(setUpList) * 100}\n'
                  f'% centralHex: {sum(centralHexes) / len(setUpList) * 100}\n'
                  f'% allyHome: {sum(allyHomes) / len(setUpList) * 100}\n'
                  f'% spawns_Ally: {sum(allySpawns) / len(setUpList) * 100}\n'
                  f'% spawns_Enemy: {sum(enemySpawns) / len(setUpList) * 100}\n'
                  f'% spawns_DangerousEnemy:   {sum(dangerousEnemySpawns)} / {len(setUpList) * 100}\n'
                  f'% grass:   {sum(grass)} / {len(setUpList) * 100}\n'
                  f'% unlockObjs:   {sum(unlockObjs)} / {len(setUpList) * 100}\n'
                  f'% interactableObjs:   {sum(interactableObjs)} / {len(setUpList) * 100}\n'
                  f'Total: {sum(walls + secrets + trees + centralHexes + allyHomes + allySpawns + enemySpawns + dangerousEnemySpawns + grass + unlockObjs + interactableObjs) / len(setUpList) * 100}\n')

        # endregion

        # region Calculate OCEAN score of set up
        #  Role Playing:   Sum of [unlock Objects]
        OCEAN_setUp['O'] = sum(unlockObjs)
        OCEAN_setUp_Max['O'] = len(unlockObjs)
        #  Action:        Sum of [Enemies, Walls, CentralHex]
        OCEAN_setUp['N'] = sum(walls + centralHexes + enemySpawns)
        OCEAN_setUp_Max['N'] = len(walls + centralHexes + enemySpawns)
        #  Shooter:       Sum of [dangerous enemies]
        OCEAN_setUp['E'] = sum(dangerousEnemySpawns)
        OCEAN_setUp_Max['E'] = len(dangerousEnemySpawns)
        #  Adventure:      Sum of [Secrets, allies, allyHomes]
        OCEAN_setUp['A'] = sum(secrets + allySpawns + allyHomes)
        OCEAN_setUp_Max['A'] = len(secrets + allySpawns + allyHomes)
        #  Simulators:     Sum of [trees, grass, interactable objects]
        OCEAN_setUp['C'] = sum(trees + grass + interactableObjs)
        OCEAN_setUp_Max['C'] = len(trees + grass + interactableObjs)

        if printResults:
            print(
                f"Environment O Score: {OCEAN_setUp['O']}\n"
                f"Environment C Score: {OCEAN_setUp['C']}\n"
                f"Environment E Score: {OCEAN_setUp['E']}\n"
                f"Environment A Score: {OCEAN_setUp['A']}\n"
                f"Environment N Score: {OCEAN_setUp['N']}\n"
            )

        # Set-up OCEAN Trait Levels
        OCEAN_setUp_Trait_levels['O'] = OCEAN_setUp['O'] / OCEAN_setUp_Max['O'] * 100
        OCEAN_setUp_Trait_levels['C'] = OCEAN_setUp['C'] / OCEAN_setUp_Max['C'] * 100
        OCEAN_setUp_Trait_levels['E'] = OCEAN_setUp['E'] / OCEAN_setUp_Max['E'] * 100
        OCEAN_setUp_Trait_levels['A'] = OCEAN_setUp['A'] / OCEAN_setUp_Max['A'] * 100
        OCEAN_setUp_Trait_levels['N'] = OCEAN_setUp['N'] / OCEAN_setUp_Max['N'] * 100

        if printResults:
            print(
                f"Environment O level: {OCEAN_setUp_Trait_levels['O']}%\n"
                f"Environment C level: {OCEAN_setUp_Trait_levels['C']}%\n"
                f"Environment E level: {OCEAN_setUp_Trait_levels['E']}%\n"
                f"Environment A level: {OCEAN_setUp_Trait_levels['A']}%\n"
                f"Environment N level: {OCEAN_setUp_Trait_levels['N']}%\n"
            )
            print(
                f"Cluster O level: {OCEAN_Levels['O']}%\n"
                f"Cluster C level: {OCEAN_Levels['C']}%\n"
                f"Cluster E level: {OCEAN_Levels['E']}%\n"
                f"Cluster A level: {OCEAN_Levels['A']}%\n"
                f"Cluster N level: {OCEAN_Levels['N']}%\n"
            )
        # endregion

        # region Calculate Fitness
        """
        - Compare the set-up OCEAN trait levels to the OCEAN trait levels of the cluster
        """
        # Compare Trait levels
        successfulTraits = []
        for trait in list(OCEAN_Levels.keys()):
            if OCEAN_Levels[trait] - 5 < OCEAN_setUp_Trait_levels[trait] < OCEAN_Levels[trait] + 5:
                successfulTraits.append(trait)
            else:
                if trait in successfulTraits:
                    successfulTraits.remove(trait)

        fitness = len(successfulTraits)

        if printResults:
            print(f'Successful Traits: {successfulTraits}')
        # endregion

        # region Save Result to CSV file
        if saveFile:
            with open(
                    'Unity Game Build/MSc_AI_RMCE__Project_Data/StreamingAssets/Genetic Algorithm Results/'
                    'Set Up Result.csv',
                    mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.GetBlocks(setUpList))
            print(f"Nested list saved to 'Set Up Result' .")

            with open('Environment_Info.txt', 'w') as file:
                # Write the string to the file
                file.write(environ_info)
        # endregion

        return fitness


# endregion

# region Set up Genetic Algorithm
def GeneticAlgorithm(OCEAN_Levels, population_size, generations, pCrossover, pMutation, m_IndMultiplier):
    # Main Variables
    setUp = SetUp()
    setUp.m_IndMultiplier = m_IndMultiplier
    randomSeed = 243
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
        # return setUp.Fitness_NumOFSuccessBlocks(individual, OCEAN_Levels, False, False),
        return setUp.Fitness(individual, OCEAN_Levels, False, False),

    toolbox.register("evaluate", Fitness)

    # Define genetic operators
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", setUp.Mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)
    # endregion

    # region Run Genetic Algorithm
    population = toolbox.PopulationCreator(n=population_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    hof = tools.HallOfFame(15)

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

    # print('Full Best Environment:')
    # print(best)
    print('Fitness: ', setUp.Fitness(best, OCEAN_Levels, False, True))

    print('Best Environment: ', setUp.GetBlocks(best)[0])
    print(setUp.Fitness(best, OCEAN_Levels, True, False))
    # print('Worst Environment: ', hof.items[len(hof.items)-1][0:10])
    # print(setUp.Fitness(hof.items[len(hof.items) - 1], OCEAN_Levels, True, False))

    plt.plot(maxFitnessValues, color="red")
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Max/average fitness')
    plt.ylabel('Generations')
    plt.show()

    return best
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

# region Main-----------------------------------------------------------------------------------------------------------
# region Set up the game environment
def SetUpGame(predictedCluster, runGA):
    # Define the cluster trait percentages referring to the Clusters Summary text file
    OCEAN_levels_C1 = {"O": 82, "C": 65, "E": 74, "A": 79, "N": 68}
    OCEAN_levels_C2 = {"O": 83, "C": 77, "E": 73, "A": 83, "N": 42}
    OCEAN_levels_C3 = {"O": 72, "C": 66, "E": 54, "A": 60, "N": 46}
    OCEAN_levels_C4 = {"O": 76, "C": 69, "E": 54, "A": 73, "N": 75}

    clusters_info = [OCEAN_levels_C1,
                     OCEAN_levels_C2,
                     OCEAN_levels_C3,
                     OCEAN_levels_C4]

    if runGA:
        if predictedCluster == 1:
            print('Cluster 1')
            GeneticAlgorithm(OCEAN_levels_C1, 50, 25, .9, .65, 0.7)
            # GeneticAlgorithm(OCEAN_levels_C1, 50, 20, .9, .6, 0.7)
        elif predictedCluster == 2:
            print('Cluster 2')
            GeneticAlgorithm(OCEAN_levels_C2, 50, 20, .45, .65, 0.4)
        elif predictedCluster == 3:
            print('Cluster 3')
            GeneticAlgorithm(OCEAN_levels_C3, 40, 40, .8, .6, 0.5)
            # GeneticAlgorithm(OCEAN_levels_C3, 40, 40, .7, .8, 0.5)
        elif predictedCluster == 4:
            print('Cluster 4')
            GeneticAlgorithm(OCEAN_levels_C4, 40, 30, .6, .6, 0.6)

    return clusters_info
# endregion

def Main():
    OCEAN_levels_C1 = {"O": 82, "C": 65, "E": 74, "A": 79, "N": 68}
    OCEAN_levels_C2 = {"O": 83, "C": 77, "E": 73, "A": 83, "N": 42}
    OCEAN_levels_C3 = {"O": 72, "C": 66, "E": 54, "A": 60, "N": 46}
    OCEAN_levels_C4 = {"O": 76, "C": 69, "E": 54, "A": 73, "N": 75}

    print('Cluster 1')
    GeneticAlgorithm(OCEAN_levels_C1, 50, 25, .9, .65, 0.7)
    print('Cluster 2')
    GeneticAlgorithm(OCEAN_levels_C2, 50, 20, .45, .65, 0.4)
    print('Cluster 3')
    GeneticAlgorithm(OCEAN_levels_C3, 40, 40, .8, .6, 0.5)
    print('Cluster 4')
    GeneticAlgorithm(OCEAN_levels_C4, 40, 30, .6, .6, 0.6)
    return


def Test():
    setup = SetUp()
    # binaryList = setup.GenerateIndividual()
    OCEAN_levels_C1 = {"O": 82, "C": 65, "E": 74, "A": 79, "N": 68}
    OCEAN_levels_C2 = {"O": 83, "C": 77, "E": 73, "A": 83, "N": 42}
    OCEAN_levels_C3 = {"O": 72, "C": 66, "E": 54, "A": 60, "N": 46}
    OCEAN_levels_C4 = {"O": 76, "C": 69, "E": 54, "A": 73, "N": 75}
    # setup.Fitness(binaryList, OCEAN_levels_C1, True, False)
    # print(setup.Fitness(binaryList, OCEAN_levels_C1, False, False))

    binaryList = [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0,
                  1]
    print(binaryList)
    print(len(binaryList))
    setup.GetBlockFeatures(binaryList, True)

    # print(setup.GenerateIndividual())
    return


# endregion ------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Test()
    Main()
