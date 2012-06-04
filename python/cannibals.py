import numpy
from collections import deque

class Node(object):
    # [<missionaries>,<cannibals>,<boat>] on the wrong side
    goal = numpy.array([0,0,0])
    possible_moves = (numpy.array([1,0,1]),numpy.array([2,0,1]),numpy.array([0,1,1]),numpy.array([0,2,1]),numpy.array([1,1,1]))
    max_depth = 15
    
    def __init__(self, state=numpy.array([3,3,1]), parent=None, to_goal_bank=True):
        self.state = state
        self.parent = parent
        self.to_goal_bank = to_goal_bank
    
    def __eq__(self, other):
        return (self.state == other.state).all()
    
    def __hash__(self):
        return self.__unicode__().__hash__()
    
    def __str__(self):
        return self.__unicode__()
    
    def __unicode__(self):
        return u'{0}'.format(self.state)
    
    def dfs(self):
        depth = 0
        examined = set()
        stack = self.children()
        while stack:
            node = stack.pop()
            if node in examined: continue
            examined.update([node])
            if node.is_goal():
                return node
            depth += 1
            if depth >= self.max_depth: break
            stack.extend(node.children())
        return None
        
    def bfs(self):
        examined = set() # memoize reduces ~ 11,000 nodes to ~ 30
        queue = deque(self.children())
        while queue:
            node = queue.popleft()
            if node in examined: continue
            examined.update([node])
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
        
    def get_moves(self):
        return abs(numpy.diff(numpy.array([node.state for node in list(self.get_path_to_root())[::-1]]), axis=0))

def tests():
    assert Node(numpy.array([3,3,1])).is_valid()
    assert Node(numpy.array([2,2,0])).is_valid()
    assert Node(numpy.array([3,1,0])).is_valid()
    assert Node(numpy.array([1,2,1])).is_valid() == False
    assert Node(numpy.array([2,1,0])).is_valid() == False
    assert Node(numpy.array([-1,2,1])).is_valid() == False
    assert Node(numpy.array([2,-1,0])).is_valid() == False
    assert Node(numpy.array([0,0,0])).is_goal()
    assert Node(numpy.array([0,1,1])).is_goal() == False
    assert Node().is_goal() == False

tests()

def format_move(current_state, move):
    right_arrow = int(current_state[2])
    left_arrow = int(not current_state[2])
    return 'M'*current_state[0] + 'C'*current_state[1] + ' ' + '<'*left_arrow+'--' + 'M'*move[0]+ 'C'*move[1] +'--' + '>'*right_arrow + ' ' + 'M'*(3-current_state[0]) + 'C'*(3-current_state[1]) 

def run():
    print 'Breadth First: \n'
    goal = Node().bfs()
    for node, move in zip(list(goal.get_path_to_root())[::-1], goal.get_moves()):
        print format_move(node.state, move)
    
    print '\nDepth First: \n'
    goal = Node().dfs()
    for node, move in zip(list(goal.get_path_to_root())[::-1], goal.get_moves()):
        print format_move(node.state, move)

if __name__ == '__main__':
    run()