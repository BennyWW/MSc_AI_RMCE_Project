"""
 Individual Assignment for CIO module
 Student Name:      BENNY WANYOIKE WAWERU
 TP No.:            TP072080
 Module Name:       Computational Intelligence Optimization (CIO)
 Module Code:       CT099-3-M
 Lecture:           Dr. Imran Medi
 Weightage:         70%
"""

# ---------------------------------------------------------------------------------------------------------------------
"""
Assignment description:
Summary for how the schedule system works for part time students:
    - 5 intakes a year
    - Students required to take modules one at a time. 
Challenges:
    - Students need to finish all the modules in 2.5 years. 
    - Each intake should accommodate old and new students
    - Certain modules are offered on multiple modules. They need to be offered at the same time
    - RMCE/RMCP modules need to be scheduled 3 times a year (Jan, May, Oct)
Goals:
    - Minimise costs (it takes approximately RM 5,000 to run each module)
    - 
Key Considerations:
    - Each programme offered maximum of 5 modules per intake
    - Modules offered consecutively. (if offered in Jan, it should not be offered in Mar)
    - RMCE/RMCP must be scheduled on in Jan, May and Oct
    - No. of students with no modules to take in an intake should be minimised. 
        * Students with RM module are allowed to skip an intake
"""
# ---------------------------------------------------------------------------------------------------------------------
"""
Ideas:
-   There are 3 different programmes each with its own modules. You need to create a schedule for part time students
    for 1 year. 
    There are 5 intakes in a year [Jan, Mar, May, Aug, and Oct]
    In 3 of those intakes, (Jan, May, and Oct), RMCE/RMCP modules can be taken. 
    If a student is taking RMCE/RMCP, they can skip the intake
    
-   The csv files contain students with the modules they have taken. You need to read the records and create 
    a schedule that suits all of the students. This can therefore be part of the fitness function for a GA algorithm. 
    
Structure:
-   Chromosome structures:
        > Year:     [[intake1],[intake2],[intake3],[intake4],[intake5]]
        > Intake:   [module1,module2,module3,...]
        > Module:   'AI','CIO','RMCE/RMCP'
-   Fitness function:
        > RMCE/RMCP violations
        > Empty intakes violations
        > Repeated modules violations
        > Student violations
            + Reduce number of students with empty intakes (if they are not taking RMCP in previous intake)
            
Notes:
- separate lists for DSBA pathways
- max electives:
    AI   =3
    SE   =3
    DSBA = 1
    DSBA specials are a must have. Must be taken. 
    
"""

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


class ProgrammeSchedule:
    def __init__(self):
        self.modules_AI = ['AI', 'IPCV', 'FL', 'AML', 'CIO', 'NLP', 'AR', 'PR', 'ESKE', 'BIS', 'MMDA', 'DL']
        self.electives_AI = ['AR', 'PR', 'ESKE', 'BIS', 'MMDA', 'DL']
        self.modules_SE = ['MSDP', 'RELM', 'OOSSE', 'SESE', 'SQE', 'SECT', 'IA', 'NDP', 'BDAT', 'DM', 'NLP']
        self.electives_SE = ['IA', 'NDP', 'BDAT', 'DM', 'NLP']
        self.modules_DSBA = ['BDAT', 'DM', 'BIS', 'AML', 'MMDA', 'DAP', 'ABAV', 'CP1', 'CP2', 'BSSMMA', 'TSF',
                             'MDA', 'SEM', 'ORO', 'CIS', 'DL', 'NLP', 'BIA', 'DPM']
        self.modules_DSBA_BI = ['BDAT', 'DM', 'BIS', 'AML', 'MMDA', 'DAP', 'ABAV', 'CP1', 'CP2', 'BSSMMA', 'TF']
        self.modules_DSBA_DE = ['BDAT', 'DM', 'BIS', 'AML', 'MMDA', 'DAP', 'ABAV', 'CP1', 'CP2', 'CIS', 'DL']
        self.electives_DSBA_BI = ['MDA', 'SEM', 'ORO']
        self.electives_DSBA_DE = ['NLP', 'BIA', 'DPM']
        self.DSBA_special_DE = ['CIS', 'DL']  # must
        self.DSBA_special_BI = ['BSSMMA', 'TSF']  # must
        self.commonModules = ['NLP', 'AML', 'BIS', 'DL', 'MMDA']
        self.intakes = [[], [], [], [], []]
        self.studentRecords_AI = {}
        self.studentRecords_SE = {}
        self.studentRecords_DSBA = {}
        self.studentRecords_DSBA_BI = {}
        self.studentRecords_DSBA_DE = {}
        self.data_AI = []
        self.data_SE = []
        self.data_DSBA = []

    def readRecords(self, AI_fileReference, SE_fileReference, DSBA_fileReference):
        # region AI Student Records
        # create the AI student records
        self.data_AI = pd.read_excel(AI_fileReference)
        records = self.data_AI.values
        print(self.data_AI)
        print(records[0][0])
        print()
        # Create records for each student
        studRecords = {}
        studCount = 0
        for record in records:
            if record[3] == 'Part time':
                if studRecords.get(record[0]) is None:
                    studRecords[record[0]] = [record[4][10:]]
                else:
                    studRecords[record[0]].append(record[4][10:])
                studCount += 1
        print('Student Count:', studCount)
        self.studentRecords_AI = studRecords
        # endregion

        # region SE Student Records
        # create the SE student records
        self.data_SE = pd.read_excel(SE_fileReference)
        records = self.data_SE.values
        print(self.data_SE)
        print(records[0][0])
        print()
        # Create records for each student
        studRecords = {}
        studCount = 0
        for record in records:
            if record[3] == 'Part time':
                if studRecords.get(record[0]) is None:
                    studRecords[record[0]] = [record[4][10:]]
                else:
                    studRecords[record[0]].append(record[4][10:])
                studCount += 1
        print('Student Count:', studCount)
        self.studentRecords_SE = studRecords
        # endregion

        # region DSBA Student Records
        # create the SE student records
        self.data_DSBA = pd.read_excel(DSBA_fileReference)
        records = self.data_DSBA.values
        print(self.data_DSBA)
        print(records[0][0])
        print()
        # Create records for each student
        studRecords = {}
        studCount = 0
        for record in records:
            if record[3] == 'Part time':
                if studRecords.get(record[0] + ' ' + record[1][14:16]) is None:
                    studRecords[record[0] + ' ' + record[1][14:16]] = [record[4][10:]]
                else:
                    studRecords[record[0] + ' ' + record[1][14:16]].append(record[4][10:])
                studCount += 1
        print('Student Count:', studCount)
        self.studentRecords_DSBA = studRecords

        # separate DSBA students based on the pathways
        studRecords = {}
        for stud in self.studentRecords_DSBA:
            if stud[len(stud) - 2:len(stud)] == 'BI':
                if studRecords.get(stud) is None:
                    studRecords[stud] = self.studentRecords_DSBA[stud]
        self.studentRecords_DSBA_BI = studRecords

        studRecords = {}
        for stud in self.studentRecords_DSBA:
            if stud[len(stud) - 2:len(stud)] == 'DE':
                if studRecords.get(stud) is None:
                    studRecords[stud] = self.studentRecords_DSBA[stud]
        self.studentRecords_DSBA_DE = studRecords
        # endregion

    def printStudRecords(self):
        # Print the student records
        print('*************AI STUDENTS*************')
        for stud in self.studentRecords_AI:
            print(stud, '\t\t\t', self.studentRecords_AI[stud])
        print("\n\n*************SE STUDENTS*************")
        for stud in self.studentRecords_SE:
            print(stud, '\t\t\t', self.studentRecords_SE[stud])
        print("\n\n*************DSBA STUDENTS*************")
        for stud in self.studentRecords_DSBA:
            print(stud[0:len(stud) - 4], '\t\t\t', self.studentRecords_DSBA[stud])
            print('\tpathway: ', stud[len(stud) - 2:len(stud)])
        print("\n\n*************DSBA (BI) STUDENTS*************")
        for stud in self.studentRecords_DSBA_BI:
            print(stud[0:len(stud) - 4], '\t\t\t', self.studentRecords_DSBA_BI[stud])
            print('\tpathway: ', stud[len(stud) - 2:len(stud)])
        print("\n\n*************DSBA (DE) STUDENTS*************")
        for stud in self.studentRecords_DSBA_DE:
            print(stud[0:len(stud) - 4], '\t\t\t', self.studentRecords_DSBA_DE[stud])
            print('\tpathway: ', stud[len(stud) - 2:len(stud)])

    def createIndividual(self):
        # Creating a chromosome (schedule)
        self.intakes = [
            [['RMCE/RMCP'], [], ['RMCE/RMCP'], [], ['RMCE/RMCP']],
            [['RMCE/RMCP'], [], ['RMCE/RMCP'], [], ['RMCE/RMCP']],
            [['RMCE/RMCP'], [], ['RMCE/RMCP'], [], ['RMCE/RMCP']],
            [['RMCE/RMCP'], [], ['RMCE/RMCP'], [], ['RMCE/RMCP']]
        ]
        modules = []
        # For each intake, add a random number of core modules (max of 5 modules per intake)
        for h in range(0, len(self.intakes)):
            for i in range(0, len(self.intakes[h])):
                if h == 0:
                    modules = self.modules_AI
                elif h == 1:
                    modules = self.modules_SE
                elif h == 2:
                    modules = self.modules_DSBA_BI
                elif h == 3:
                    modules = self.modules_DSBA_DE
                maxModules = random.randrange(1, len(modules))
                for j in range(0, maxModules):
                    randomModule = random.choice(modules)
                    # Make sure module is not offered more than once in same intake
                    if randomModule not in self.intakes[h][i]:
                        self.intakes[h][i].append(randomModule)
                    # Remove modules offered in previous intake
                    if i > 0:
                        if randomModule in self.intakes[h][i - 1]:
                            self.intakes[h][i].remove(randomModule)
        # Handle duplicates
        for i in range(0, len(self.intakes)):
            for j in range(0, len(self.intakes[i])):
                self.intakes[i][j] = list(set(self.intakes[i][j]))

        return self.intakes

    def fitness(self, schedule):
        violations = 0
        studentRecords = {}
        electives = []
        intakeCommonModules = [[], [], [], [], []]

        for i in range(0, len(schedule)):
            specials = []
            specialsOffered = []
            specialsTaken = []
            if i == 0:
                studentRecords = self.studentRecords_AI
                electives = self.electives_AI
            elif i == 1:
                studentRecords = self.studentRecords_SE
                electives = self.electives_SE
            elif i == 2:
                studentRecords = self.studentRecords_DSBA_BI
                electives = self.electives_DSBA_BI
                specials = self.DSBA_special_BI
            elif i == 3:
                studentRecords = self.studentRecords_DSBA_DE
                electives = self.electives_DSBA_DE
                specials = self.DSBA_special_DE

            for stud in studentRecords:
                intakeSkip = 0
                electivesTaken = 0
                for j in range(0, len(schedule[i])):
                    # region Number of modules violations
                    # Limit max number of modules per intake to 5
                    if len(schedule[i][j]) > 5:
                        violations += 1
                    if len(schedule[i][j]) < 3:
                        violations += .5
                    # endregion

                    # region Empty intakes for students
                    # If student has taken all the modules offered in an intake, violations + 1
                    # else if they have RMCE/RMCP in the taken modules, then violations + 0
                    intakeModules = set(schedule[i][j])
                    studModules = set(studentRecords[stud])
                    if set(intakeModules).issubset(set(studModules)):
                        if intakeSkip < 1:
                            if 'RMCE/RMCP' not in studModules:
                                violations += 1
                            else:
                                intakeSkip += 1
                        else:
                            violations += 1
                    if intakeSkip > 1:
                        violations += 1
                    # endregion

                    # region Only 3 electives for AI and SE and only 1 elective for DSBA
                    for module in schedule[i][j]:
                        if module in electives:
                            electivesTaken += 1
                    if i < 2:
                        if electivesTaken > 3:
                            violations += 1
                    else:
                        if electivesTaken > 1:
                            violations += 1
                    # endregion

                    # region Check for duplicates in intakes
                    if len(schedule[i][j]) > len(list(set(schedule[i][j]))):
                        violations += 1
                    # endregion

                    # region Check for module consecutive repeats
                    if j > 1:
                        if set(schedule[i][j - 1]) in set(schedule[i][j]):
                            violations += 2
                    # endregion

                    # region DSBA must have modules
                    for module in stud:
                        if module in specials:
                            specialsTaken.append(module)
                    for module in schedule[i][j]:
                        if module in specials:
                            specialsOffered.append(module)
                    # endregion

                    # region Check if CP1 and CP2 are in same intake
                    if {'CP1', 'CP2'}.issubset(set(schedule[i][j])):
                        violations += 1
                    # endregion

                # region Check if DE and BI got offered their specials
                if len(specialsTaken) < len(specialsOffered):
                    violations += 2
                # endregion

            # region Check consecutive common modules and try having them in same intake
            for j in range(0, len(schedule[i])):
                for module in schedule[i][j]:
                    if module in self.commonModules:
                        intakeCommonModules[j].append(module)
            for j in range(0, len(intakeCommonModules)):
                for module in intakeCommonModules[j]:
                    if j > 0:
                        if module in intakeCommonModules[j - 1]:
                            violations += 1
                    for k in range(0, len(intakeCommonModules)):
                        if k != j:
                            if module in intakeCommonModules[k]:
                                violations += 1
            # endregion

        return violations


def mutateIndividual(individual):
    for programme in individual:
        modules = []
        for intake in programme:
            for module in intake:
                if module != 'RMCE/RMCP':
                    modules.append(module)
                    intake.remove(module)
        for intake in programme:
            randomModule = random.choice(modules)
            intake.append(randomModule)
            modules.remove(randomModule)

    return individual,


# --------------------------------------------------------------------------------------------------------

# Easimple -------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------

# Main -----------------------------------------------------------------------------------------------------------------


sampleSchedule = ProgrammeSchedule()
sampleSchedule.readRecords('MScAI.xlsx', 'MScSE.xlsx', 'DSBA.xlsx')
sampleSchedule.printStudRecords()
x = sampleSchedule.createIndividual()
print(x)
for indiv in x:
    for i in indiv:
        print(i)
    print()
print()
# print(testSchedule.fitness(x))

x, = mutateIndividual(x)
print(x)
print('mutated')
for indiv in x:
    for i in indiv:
        print(i)
    print()
population_size = 500
generations = 100
pCrossover = 1
pMutation = 0.5
randomSeed = 243

random.seed(randomSeed)

# Set up the toolbox
toolbox = base.Toolbox()

# Define fitness, individual and population creators
# Create function to evaluate the individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Create function to create an individual
creator.create("Individual", list, fitness=creator.FitnessMin)
# Define/register a function to create and individual
toolbox.register("IndividualCreator", tools.initIterate,
                 creator.Individual, sampleSchedule.createIndividual)
# Define/Register a function to generate a population
toolbox.register("PopulationCreator", tools.initRepeat,
                 list, toolbox.IndividualCreator)


# Create a fitness function - evaluation
def fitnessFunction(individual):
    return sampleSchedule.fitness(individual),


# Set up the genetic operators
toolbox.register("evaluate", fitnessFunction)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutateIndividual)


def main():
    population = toolbox.PopulationCreator(n=population_size)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
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

    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")

    print(sampleSchedule.fitness(best))
    print('Best Schedule: ')
    for i in range(0, len(best)):
        programme = ''
        if i == 0:
            programme = 'Programme: AI'
        elif i == 1:
            programme = 'Programme: SE'
        elif i == 2:
            programme = 'Programme: DSBA (BI)'
        elif i == 3:
            programme = 'Programme: DSBA (DE)'

        print(programme)
        for j in range(0, len(best[i])):
            print('intake ', j + 1, ':', best[i][j])
    print(sampleSchedule.commonModules)

    plt.plot(minFitnessValues, color="red")
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Min/average fitness')
    plt.ylabel('Generations')
    plt.show()


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
