from Assignment2.astar import Astar, Node
from Assignment2.map import Map_Obj
from unittest import TestCase
class TestAstar(TestCase):
    m = Map_Obj(task=1)
    a = Astar(m)
    n = Node([0,0])

    def test_calc_h(self):
        self.n.calc_h([0,1])
        assert self.n.h == 1
        self.n.calc_h([2,2])
        self.n.calc_f()
        assert self.n.h == 4
        assert self.n.f == 4
        self.a.push_and_sort(self.n)

    def test_push_and_sort(self):
        n1 = Node([1,1])
        n1.calc_h([2,2])
        n1.calc_f()

        assert (n1.f == 2)
        self.a.push_and_sort(n1)

        assert (self.a.Open[0].pos == [1,1])
# currently testing push and sort method

    def test_generate_sucs(self):
        m = Map_Obj(task=1)
        star = Astar(m)
        generated_moves = star.generate_all_successors(star.x, m)
        pos = star.x.pos

        allowed_moves = []
        for i in range(-1, 2):
            for j in range(-1,2):
                if m.get_cell_value([pos[0] + i, pos[1] + j]) != -1:
                    if ((i == 0 or j == 0) and ([j,i] != [0,0])):
                        allowed_moves.append([pos[0] + i, pos[1] + j])

        #expanded_positions = [[cn[0], cn[1] + 1], [cn[0]+1, cn[1], cn[1]]
        self.assertListEqual(generated_moves, allowed_moves)

        # assert some wronge moves
        node = star.x
        node.pos[1] += 5
        m.set_cell_value(pos, '2')
        m.print_map(m.int_map)
        print("Current node: {}".format(node.pos))
        generated_moves = star.generate_all_successors(node, m)
        print (generated_moves)
        allowed_moves = []
        for i in range(-1, 2):
            for j in range(-1,2):
                if m.get_cell_value([pos[0] + i, pos[1] + j]) != -1:
                    if ((i == 0 or j == 0) and ([j,i] != [0,0])):
                        allowed_moves.append([pos[0] + i, pos[1] + j])

        self.assertListEqual(generated_moves, allowed_moves)

    def test_has_bee_generated_before(self):
        m = Map_Obj(task=1)
        star = Astar(m)
        node1 = Node([0,0])
        star.push_and_sort(node1)
        node2 = Node([0,0])
        t = 1
        t = star.has_been_generated_before(node2) == Node([1,1])
        print("this is t {}".format(t))
        assert (node1 == node2)
        assert(star.has_been_generated_before(node2) == node1)
        self.assertFalse(star.has_been_generated_before(node2) == Node([1,1]))

