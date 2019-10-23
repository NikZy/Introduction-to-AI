import copy
import itertools


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.backtrack_counter = 0
        self.failed_counter = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())
        print_sudoku_solution(assignment)
        print(assignment)

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        self.backtrack_counter +=1
        #print("Backtrack_called: " + str(self.backtrack_counter))
        # Check if complete
        number_of_values = list(filter(lambda node: len(node[1]) > 1, assignment.items()))
        if (len(number_of_values) == 0): return assignment

        # var = select unnasigned variable
        var = self.select_unassigned_variable(assignment)
       # print("---NEW BACKTRACK RECURSION---")
       # print("var: {}".format(var))
       # print(assignment)

        # loop over domain of var.
        for value in assignment[var]:
            copy_assignment = copy.deepcopy(assignment)
            #If value is allowed -> var = value
            copy_assignment[var] = [value]
            # if changed value inference over all naighboors removing value from domain
            inference = self.inference(copy_assignment, self.get_all_neighboring_arcs(var))

            if inference == True:
                result = self.backtrack(copy_assignment)

                # Return true if assignment complete
                if result:
                    return result
            else:
                self.failed_counter += 1
                print("Failed: " + str(self.failed_counter))

        # No solution found
        return False

            # if inference != false
                # add inference to assignment
                # result = backtrack(assignment, self)
            # if result != failure
                #return result

            # remove var = value and inference from assignment

        # return failure


    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        for (key, value) in assignment.items():
            if len(value) > 1:
                return key

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while len(queue) > 0:
            pair = queue.pop()
            if self.revise(assignment, pair[0], pair[1]):
                # Incorrect solution. no more moves left
                if len(assignment[pair[0]]) == 0:
                    return False
                # Add all neighbors to que, so we can update their domains aswell
                for neighbor in self.get_all_neighboring_arcs(pair[0]): queue.append(neighbor)
        return True
        # Assignment = domain
        # que = all neighboring arcs

        # While que not empty
            # pair = que.pop()

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        revised = False
        constraints = self.constraints[i][j]
        # for each x in i.domains
        #if len(assignment[j]) == 1:
            #print(assignment[j])
        for value in assignment[i]:
            # if no value y in j.domains satify constrains between i and j
            filtered = list(filter(lambda pair: pair[0] == value, constraints))
            found_move = False
            for v in assignment[j]:
                for c in filtered:
                    if c[1] == v:
                        found_move = True


            #print("Node: {}, {}. Remove value: {}".format(i,j,value))
            #print(assignment)
            if not found_move:
                assignment[i].remove(value)
                revised = True
                # delete x from i.domains
                # revised = true
        #return revised
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)

    for constraint in csp.constraints:
        for entry in csp.constraints[constraint]:
            csp.constraints[constraint][entry] = list(csp.constraints[constraint][entry])
    return csp


def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str, range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    for constraint in csp.constraints:
        for entry in csp.constraints[constraint]:
            csp.constraints[constraint][entry] = list(csp.constraints[constraint][entry])
    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" "),
            if col == 2 or col == 5:
                print('|', end=" "),
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')

if __name__ == "__main__":
    print("start")
    csp = create_sudoku_csp("hard.txt")
    #print("Variables: ")
    #print(csp.variables)
    #print("Domains: ")
    #print(csp.domains)
    #print( "Constraints: " )
    #print(csp.constraints)
    print_sudoku_solution(csp.backtracking_search())
    #print("All arcs:")
    #print(csp.get_all_arcs())
    #print(csp.get_all_neighboring_arcs())

