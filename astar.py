from map import Map_Obj
class Node ():
    # global state counter for generating unique ids
    state_counter = 0
    def __init__(self):
        # an object describing a state of the search process
        self.state = state_counter
        state_counter += 1
        # cost of getting to this node
        self.g = 0
        # estimated cost to goal
        self.h = 0
        # estimated total cost of a solution path going through this node
        self.f = self.g + self.h
        # open or closed
        self.status = 'open'
        # pointer to best parent node
        self.parent = None
        # list of all successor nodes, whether or not this node is currently their best parent
        self.kids = None

    # ---methods---
    # getters and setters?

    # update children?

class Astar():
    def __init__(self, map_obj):
        # map
        self.map_obj = mab_obj
        # unexplored nodes
        self.Open = []
        # explored nodes
        self.Closed = []
        # successors
        self.Succ = []

        # generate initial start node
        self.x = Node()
        self.x.h = self.calc_h(map_obj)

    def search(self):
        while True:
            if len(Open) == 0:
                # failed to found a solution
                return False

            # pops first element i list
            x = Open.pop(0)
            Closed.append(x)

            # if x is a solution. Return Succ

            # Succ = generate-all-successors(x)

            for s in Succ:
                # check if s has been created before and is the same state. Then fetch from open or closed list
                s.kids.append(s) # already exists?

                # if s has not been created before.
                #then attach-and-eval(s,x)
                # insert s to open. sort open

                # if s exists and it's a cheaper path
                # attach and eval(s,x)

                # if s in closed then propogate-path-improvements
    def calc_h(map_obj):
        pass
    def generate_all_successors(self, x):
        """
        Explore surrounding nodes based on allowed moves?
        """
        pass

    def attach_and_eval(self, child, parent):
        """
        When a new unique node is found:
        attaches a child node to a node that is now considered its best parent.
        Childs value of g is then computed based on parent's value plus cost of moving from parent to child.
        The heuristic value of C is assessed and childs f is updated.
        """
        # p = parent(c)

        child.g = parent.g + 1

        # child.h = compute h(child)

        child.f = child.g + child.g


    def propagate_path_improvements(self, parent):
        """
        Recurses through children and possibly manyy other descendants.
        Some children may not have had parent as the best parent.
        """
        cost = 1
        for child in parent.kids:
            if child.g + cost < child.g:
                child.parent = parent
                child.g = p.g + cost
                child.f = child.g + child.h
                propagate_path_improvements(child)
if __name__ == "__main__":
    print("Start")
    map_obj = Map_Obj()
    astar = Astar(map_obj)
