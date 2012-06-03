from numpy import array as na
from collections import deque

class Node(object):
    # [<missionaries>,<cannibals>,<boat>] on the wrong side
    goal = na([0,0,0])
    possible_moves = (na([1,0,1]),na([2,0,1]),na([0,1,1]),na([0,2,1]),na([1,1,1]))
    max_depth = 15
    
    def __init__(self, state=na([3,3,1]), parent=None, to_goal_bank=True):
        self.state = state
        self.parent = parent
        self.to_goal_bank = to_goal_bank
        self.examined = set()
    
    def __eq__(self, other):
        return (self.state == other.state).all()
    
    def __hash__(self):
        return self.__unicode__().__hash__()
    
    def __str__(self):
        return self.__unicode__()
    
    def __unicode__(self):
        return u'{0}'.format(self.state)
    
    def dfs(self, depth=0):
        stack = self.children()
        while stack:
            node = stack.pop()
            if node in self.examined: continue
            self.examined.update([node])
            if node.is_goal():
                return node
            stack.extend(node.children())
        return None
        
    def bfs(self):
        queue = deque(self.children())
        while queue:
            node = queue.popleft()
            if node in self.examined: continue
            self.examined.update([node])
            if node.is_goal():
                return node
            queue.extend(node.children())
    
    def children(self):
        return [node for node in [self.transition(move) for move in self.possible_moves] if node.is_valid()]
    
    def transition(self, move):
        return Node(self.state - move if self.to_goal_bank else self.state + move, self, not self.to_goal_bank)
        
    def is_goal(self):
        return (self.state==self.goal).all()

    def is_valid(self):
        # an invalid state is one in which there are more cannibals than missionaries on either side, unless there are no missionaries
        m,c = self.state[0:2]
        correct_manipulation = (m >= 0 and c >= 0 and 3-m >= 0 and 3-c >=0)
        wrong_side = (m == 0 or m >= c)
        right_side = (3-m == 0 or 3-m >= 3-c)
        return correct_manipulation and wrong_side and right_side
    
    def get_path_to_root(self):
        node = self
        while node != None:
            yield node
            node = node.parent
        return

def tests():
    assert Node(na([3,3,1])).is_valid()
    assert Node(na([2,2,0])).is_valid()
    assert Node(na([3,1,0])).is_valid()
    assert Node(na([1,2,1])).is_valid() == False
    assert Node(na([2,1,0])).is_valid() == False
    assert Node(na([-1,2,1])).is_valid() == False
    assert Node(na([2,-1,0])).is_valid() == False
    assert Node(na([0,0,0])).is_goal()
    assert Node(na([0,1,1])).is_goal() == False
    assert Node().is_goal() == False

tests()

def run():
    for node in list(Node().bfs().get_path_to_root())[::-1]:
        print node
    for node in list(Node().dfs().get_path_to_root())[::-1]:
        print node

if __name__ == '__main__':
    run()