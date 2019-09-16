from map import Map_Obj
class Node ():
    # global state counter for generating unique ids
    state_counter = 0
    def __init__(self, pos, cost=1):
        # an object describing a state of the search process
        #self.state = state_counter
        #state_counter += 1
        # position
        self.pos = pos
        # cost of getting to this node
        self.g = 0
        # estimated cost to goal
        self.h = 0
        # estimated total cost of a solution path going through this node
        self.f = self.g + self.h
        # open or closed
        self.status = 'open'
        # pointer to best parent node
        self.parent = []
        # list of all successor nodes, whether or not this node is currently their best parent
        self.kids = []
        # cost of moving to this node (1-4)
        self.cost = cost

    # ---methods---
    def char_to_cost(self):
        """
        Converts the given cost
        """
        pass
    def calc_h(self, goal):
        """
        calculates best case shortest path by
        adding together differansen between
        x and y axis
        """
        self.h =  abs(self.pos[0] - goal[0]) + abs(self.pos[1] -goal[1])

    def calc_f(self):
        self.f = self.g + self.h
    # getters and setters?

    # update children?
    def __eq__(self, other):
        return self.pos == other.pos
    def __str__(self):
        return str(self.pos)


class Astar():
    def __init__(self, map_obj):
        # map
        self.map_obj = map_obj
        # unexplored nodes
        self.Open = []
        # explored nodes
        self.Closed = []
        # successors
        self.Succ = []

        # generate initial start node
        self.x = Node(map_obj.get_start_pos(), map_obj.get_cell_value(map_obj.get_start_pos()))
        # estimate length to goal
        self.x.calc_h(self.map_obj.get_end_goal_pos())
        # estimate total length to goal from start
        self.x.calc_f()
        self.push_and_sort(self.x)

    def paint_road(self, x):
        """
        when goal is reached, recursivily paint each parent with red
        to see path taken
        """
        print("parent of x: {}".format(x.parent))
        if (x.parent):
            pos = x.parent.pos
            print("pos: {}".format(pos))
            self.map_obj.set_cell_value(pos, ' P ')
            self.paint_road(x.parent)

        else:
            return True
    def search(self):
        """
        Main function of astar class.
        initiates the Astar algorithm
        """
        while True:
            if len(self.Open) == 0:
                # failed to found a solution
                return False

            # pops first element i list
            self.x = self.Open.pop(0)
            self.Closed.append(self.x) # need more testing?

            # if x is a solution. Return Succ
            if (self.x.pos == self.map_obj.goal_pos):
                print("Found Goal!")
                print("Goal position: {}".format(self.x))
                self.paint_road(self.x)
                return self.x

            self.generate_all_successors(self.x, self.map_obj)

            for s in self.Succ:
                # check if s has been created before and is the same state. Then fetch from open or closed list
                if (self.has_been_generated_before(s)):
                    s = self.has_been_generated_before(s)
                self.x.kids.append(s) # add sucsessor as child of this node

                if (not self.has_been_generated_before(s)): # working?
                    # if s has not been created before.
                    #then attach-and-eval(s,x)
                    self.attach_and_eval(s, self.x)
                    # insert s to open. sort open
                    self.push_and_sort(s)

                elif (self.has_been_generated_before(s) and self.x.g + s.cost < s.g):
                    # if s exists and it's a cheaper path
                    self.attach_and_eval(s, self.x)
                    if (s in self.Closed):
                        # update children of S aswell
                        # if s in closed then propogate-path-improvements
                        self.propagate_path_improvements(s)



    def has_been_generated_before(self, node):
        if(node in self.Open):
            return self.Open[self.Open.index(node)]
        elif (node in self.Closed):
            return self.Closed[self.Closed.index(node)]
    def push_and_sort(self, node):
        """
        pushes a new node to Open stack, and sorts the it based on f value
        """
        self.Open.append(node)
        self.Open = sorted(self.Open, key= lambda n: n.f)

    def generate_all_successors(self, x, map_obj):
        """
        Explore surrounding nodes based on allowed moves?
        """
        pos = x.pos
        allowed_modes = []
        for i in range(-1, 2):
            for j in range(-1,2):
                n = [pos[0] + i, pos[1] + j]
                #print(map_obj.get_cell_value(n))
                if map_obj.get_cell_value([pos[0] + i, pos[1] + j]) != -1:
                    if ((i == 0 or j == 0) and ([j,i] != [0,0])):
                        cost = map_obj.get_cell_value(n)
                        new_node = Node([pos[0] +i, pos[1] + j], cost)
                        self.Succ.append(new_node)
                        allowed_modes.append([pos[0] +i, pos[1] + j])
        return allowed_modes

    def attach_and_eval(self, child, parent):
        """
        When a new unique node is found:
        attaches a child node to a node that is now considered its best parent.
        Childs value of g is then computed based on parent's value plus cost of moving from parent to child.
        The heuristic value of C is assessed and childs f is updated.
        """
        # p = parent(c)
        child.parent = parent

        child.g = parent.g + child.cost

        # child.h = compute h(child)

        child.f = child.g + child.h


    def propagate_path_improvements(self, parent):
        """
        Recurses through children and possibly manyy other descendants.
        Some children may not have had parent as the best parent.
        """
        for child in parent.kids:
            if parent.g + child.cost < child.g:
                child.parent = parent
                child.g = parent.g + child.cost
                child.f = child.g + child.h
                propagate_path_improvements(child)
if __name__ == "__main__":
    print("Start")
    map_obj = Map_Obj(task=4)
    astar = Astar(map_obj)
    print(astar.search())
    astar.map_obj.print_map(astar.map_obj.str_map)
    astar.map_obj.show_map()
