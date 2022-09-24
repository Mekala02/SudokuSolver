import numpy as np
import math
import copy

class sudoku_solver:
    def __init__(self):
        # Domains are our knowledge base for puzzle.
        self.domains = dict()
        # Every cell has a neighbor,neighbors are other cells that are in same coulumn, row
        # or same small square (grid, like 3X3 if puzzle is 9X9).
        self.neighbors = dict()

    def new_puzzle(self, puzzle):
        # Ai takes puzzle that represented by mXm matrix containing numbers form 1-9 and zeros
        # for empty squares.
        self.puzzle = puzzle
        # M is dimension of puzzle matrix (Puzzles are square).
        self.m = len(self.puzzle)
        # Grid size is small squares in puzzle.
        self.grid_size = int(math.sqrt(self.m))
        # Adding neighbors and domains to knowledge base.
        for row in range(self.m):
            for column in range(self.m):
                # Adding neighbors for this cell.
                self.neighbors[(row, column)] = self.findneighbors((row, column))
                # If that cells value not 0 it means we know its value so we adding it to knowledge base.
                if self.puzzle[row][column] != 0:
                    self.domains[(row, column)] = set([self.puzzle[row][column]])
                # If we don't know that cells value we adding all numbers to the domain of that cell.
                else:
                    self.domains[(row, column)] = set(range(1, self.m + 1))

    def findneighbors(self, variable_coordinates):
        x, y = variable_coordinates
        neighbors = set()
        for a in range(self.m):
            neighbors.add((x, a))
            neighbors.add((a, y))
        a, b = self.neighborbox((x, y))
        for row in range(self.grid_size * a, self.grid_size * a + self.grid_size):
            for column in range(self.grid_size * b, self.grid_size * b + self.grid_size):
                neighbors.add((row, column))
        neighbors.remove((x, y))
        return neighbors
        
    def neighborbox(self, variable_coordinates):
        x, y = variable_coordinates
        # Splitting mXm matrix to grid sized arrays
        split = np.array_split(range(self.m), self.grid_size)
        # Founding that particilor cells belongs to which grid
        for i in range(self.grid_size):
            if x in split[i]: a = i
            if y in split[i]: b = i
        return (a, b)

    def solve(self):
        self.ac3(self.domains)
        return self.backtrack(self.domains)

    # This function updating knowledge base
    def ac3(self, domains, arcs=None):
        # Arcs is a list of all damins that we want to inferance from.
        # If we not give specific list of domains this function will add all
        # domains to arcs this means we will make inferances among all knowledge base.
        # Arcs contains all 2 combinations of neighbor cells for making inferance among them.
        if arcs == None:
            arcs = []
            for variable1 in domains.keys():
                if not self.knownvalue(domains, variable1):
                    for neighbor in self.neighbors[(variable1)]:
                        arcs.append((variable1, neighbor))

        while arcs:
            # Arcs is our frontier since pop function takes last element of list,
            # this frontier is first in last out.
            x, y = arcs.pop()
            # If revise changed any domains we adding changed cell and its neighbors to the arcs
            # becouse maybe we can make further inferance from that cell.
            if self.revise(x, y):
                if not domains[x]:
                    # If there is no value in domain X it means we don't have solution for that case
                    # so we returning False
                    return False
                # We are not adding y with x becouse we checked it already in last revise
                for neighbor in self.neighbors[(x)] - {y}:
                    arcs.append((neighbor, x))
        return True

    # This function resolves conflictions between given two cells (only modifying first given cell) .
    def revise(self, variable_coordinates, neighbor_coordinate):
        if knownvalue:= self.knownvalue(self.domains, neighbor_coordinate):
            # If we know value for neighbor of that cell and that value in cells domain we removing
            # that value form cells domain. (Becouse if neighbor contains that value that means that cell can't).
            if knownvalue in self.domains[variable_coordinates]:
                self.domains[variable_coordinates].remove(knownvalue)
                # If we made a change returning True.
                return True
        return False

    def knownvalue(self, domains, variable_coordinates):
        # If there is only 1 element in domain for that cell it means we found
        # that cells value.
        if len(domains[variable_coordinates]) == 1:
            # If we found value for that cell we returning it
            return list(domains[variable_coordinates])[0]
        return None

    def backtrack(self, domains):
        # First we checking if we found solution or not
        # If we found solution we returning it
        if self.assignment_complete(domains):
            solution = self.solution(domains)
            return solution
        
        # We are copying domains becouse we will change it values and maybe we will change it wrongly
        # so if that happens basicly we will bring back old domains
        coppied = copy.deepcopy(domains)
        # Selecting unassigned variable
        variable_coordinates = self.select_unassigned_variable(domains)
        # Selecting value for it
        for value in self.domain_values(domains, variable_coordinates):
            # Pretending like this cells value is our choosed value and trying to solve puzzle
            domains[variable_coordinates] = {value}
                # We updating our knowledge base according to that value for that cell (pretending like value is correct)
            if self.ac3(domains, [(variable_coordinates, neighbor) for neighbor in self.neighbors[(variable_coordinates)]]):
                # If we still consistent after inferance we good to go
                if self.consistent(domains):
                    # We recursively trying to solve other variables values
                    solution = self.backtrack(domains)
                    # If that selected value routed us to solution we returning the solution
                    if (solution.all()):
                        return solution
            # If we are here that means we dont have solution for that particular domain value combination. So we basicly reverting
            # back our knowledge base to old one and starting new value prediction.
            # Of course we removing that value from that cells domain becouse we tryed it and saw its not correct.
            coppied[variable_coordinates].remove(value)
            domains = copy.deepcopy(coppied)
        # Returning False it means we don't have solution.
        return np.array(False)

    def assignment_complete(self, domains):
        # If all domains values are 1 it means our assignment is compleate.
        for value in domains:
            if len(domains[value]) != 1:
                return False
        return True

    def solution(self, domains):
        # Converting our list solutions to numpy array.
        solution = np.zeros((9, 9), np.int32)
        for x in range(9):
            for y in range(9):
                for s in domains[(x, y)]: break
                solution[x][y] = s
        return solution

    def select_unassigned_variable(self, domains):
        unassigned = []
        for variable_coordinates in domains:
            if len(domains[variable_coordinates]) != 1:
                unassigned.append(variable_coordinates)
        result = sorted(unassigned, key=lambda var: (len(domains[var]), -len(self.neighbors[(var)])))
        return result[0]

    def domain_values(self, domains, variable_coordinates):
        ruleout_count = {value: 0 for value in domains[variable_coordinates]}
        for value1 in domains[variable_coordinates]:
            for variable2_coordinate in self.neighbors[(variable_coordinates)]:
                for value2 in domains[variable2_coordinate]:
                    if value1 != value2:
                        ruleout_count[value1] += 1
        return sorted([x for x in ruleout_count], key=lambda x: ruleout_count[x])

    def consistent(self, domains):
        # Checking given particular domains for consistency among variables.
        for variable in domains.keys():
            if self.knownvalue(domains, variable):
                for neighbor in self.neighbors[(variable)]:
                    # If neighboring cell and cell has same value that means 
                    if self.knownvalue(domains, neighbor) and domains[variable] == domains[neighbor]:
                        return False
        return True