import sys
import copy

from crossword import *
from queue import Queue

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains.keys():
            word_to_remove = set()
            length = var.length
            for word in self.domains[var]:
                # Guarantee the word length equals to the blank length
                if len(word) != length:
                    word_to_remove.add(word)
            self.domains[var] -= word_to_remove        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        word_to_remove = set()
        revised = False
        if self.crossword.overlaps[(x, y)] == None:
            return revised

        i, j = self.crossword.overlaps[(x, y)]
        for word in self.domains[x]:
            if_exist = False
            # Arc consistency
            for another_word in self.domains[y]:
                if word[i] == another_word[j]:
                    if_exist = True
                    break
            if if_exist == False:
                word_to_remove.add(word)
                revised = True
        self.domains[x] -= word_to_remove        
        return revised
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        vars = list(self.domains.keys())
    
        q = Queue()

        if arcs == None:
            arcs = [(i, j) for i in self.domains.keys() for j in self.crossword.neighbors(i)]

        for i in arcs:
            q.put(i)

        while (not q.empty()):
            x, y = q.get()

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    # cannot guarantee the arc consistency
                    return False
                else:
                    for i in self.crossword.neighbors(x):
                        q.put((i, x))

        return True                

        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return set(assignment.keys()) == self.crossword.variables


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        vars = assignment.keys()
        values = assignment.values()
        set_values = set(values)
        # Make sure the answer word does not duplicate
        if len(set_values) != len(values):
            return False
        # Make sure the word length correct
        for i in vars:
            if i.length != len(assignment[i]):
                return False
            # Make sure overlap do not conflict
            for j in self.crossword.neighbors(i):
                if j in assignment:
                    x, y = self.crossword.overlaps[(i, j)]
                    if assignment[i][x] != assignment[j][y]:
                        return False
        return True            



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return sorted(self.domains[var], 
                      key = lambda value: self.least_constraining_value(assignment, value, var))
    
    def least_constraining_value(self, assignment, value, var):
        num = 0
        unassigned = [i for i in self.domains.keys() if i not in assignment]
        if unassigned == []:
            return 0
        else:
            for j in unassigned:
                if j != var:
                    for u in self.domains[j]:
                        if self.crossword.overlaps[(var, j)] != None:
                            x, y = self.crossword.overlaps[(var, j)]
                            if value[x] == u[y]:
                                num += 1

        return num            
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        vars = [i for i in self.domains.keys() if i not in assignment.keys()]
        vars.sort(key = lambda var: len(self.domains[var]))
        min_remaining = len(self.domains[vars[0]])
        min_vars = [var for var in vars if len(self.domains[var]) == min_remaining]
        if len(min_vars) == 1:
            return min_vars[0]
        else:
            min_vars.sort(key=lambda var: sum( 1 for i in self.crossword.neighbors(var) if i not in assignment), reverse=True)
            return min_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        else:
            var = self.select_unassigned_variable(assignment)
            var_list = self.order_domain_values(var, assignment)
            arcs = []
            for i in self.domains.keys():
                if i != var:
                    arcs.append((var, i))

            for value in var_list:
                assignment[var] = value
                if self.consistent(assignment):

                    # Add new inferences if it succeeded
                    saved = copy.deepcopy(self.domains)
                    self.domains[var] = {value}
                    inference = self.ac3()
                    if inference:
                         result = self.backtrack(assignment)
                         if result != None:
                            return result
                    self.domains = saved
                del assignment[var]
            return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
