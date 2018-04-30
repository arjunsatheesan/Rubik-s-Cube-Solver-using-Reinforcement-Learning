'''
Cube_formulation.py
Final Project
CSE 415 Wi-18 by
Ajay Dhavane(ajayd92), Arjun Satheesan(arjun89)
Guide: S. Tanimoto

This file descibes the formulation of a 2x2 Rubik's cube

'''
import random
import itertools

#<COMMON_DATA>
num_moves = 2  # Use default, but override if new value supplied
             # by the user on the command line.
try:
  import sys
  arg1 = sys.argv[1]
  num_moves = int(arg1)
  print("Number of scrambling moves is: ", num_moves)
except:
  print("Using default number of scrambling moves: "+str(num_moves))
  print(" (To use a specific number, enter it on the command line, e.g.,")
  print("python3 RunRubiksCube.py 3")
#</COMMON_DATA>

# define state
class Cube():
    def __init__(self, d):
        self.d = d

    # textual description of a state
    def __str__(self):
        d = self.d
        txt = ""
        for row in range(2):
            for face in d:
                txt += " [ "
                for tile in face[row]:
                    txt = txt + str(tile) + " "
                txt = txt + "]"
            txt=txt+"\n"

        return txt

    def __eq__(self, s2):
        return self.d == s2.d

    def __hash__(self):
        return (str(self)).__hash__()

    # Performs an appropriately deep copy of a state.
    def __copy__(self):
        news = Cube([])
        for face in self.d:
            newf = copy_face(face)
            news.d.append(newf)
        
        return news

# copy all tiles of a face to a new face and return new face
def copy_face(face):
    newf = []
    for row in face:
        newr = []
        for n in row:
            newr.append(n)
        newf.append(newr)

    return newf

def goal_test(s):
    d = s.d
    for face_num in range(6):
        face = d[face_num]
        if not face[0][0] == face[0][1] == face[1][0] == face[1][1]:
            return False

    return True
            

def goal_message(s):
    return "Rubik's cube is solved!"

# Completed 2x2 cube        
GOAL_STATE_CUBE = [[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]]
GOAL_STATE = Cube(GOAL_STATE_CUBE)
        
# Since all rotations are valid, it should always return true
def can_rotate(s, face_num, rot_dir):
    return True
    
# Make the move. Input is the previous state, face to be moved and the rotation direction
# Returns the new state after the rotation has been performed
def rotate(s, face_num, rot_dir):
    news = s.__copy__()
    
    news.d[face_num] = rotate_face(s, face_num, rot_dir)
    new_faces = rotate_edge(s, face_num, rot_dir)
    for newf in new_faces:
        news.d[newf] = new_faces[newf]
        
    return news
    
# Rotate the values on a face only
# 1 -> clockwise
# -1 -> anti
# Returns the updated face
def rotate_face(s, face_num, rot_dir):
    face = s.d[face_num]
    newf = copy_face(s.d[face_num])
    
    #Rotate clockwise
    if rot_dir == 1:
        for row in range(2):
            for col in range(2):
                newf[row][col] = face[1-col][row]

    #Rotate anticlockwise
    else:
        for row in range(2):
            for col in range(2):
                newf[row][col] = face[col][1-row]
    
    return newf

# Update the tiles on the adjacent edges
# Returns the updated adjacent faces
def rotate_edge(s, face_num, rot_dir):
    adj_edges = adj_edge_dict[face_num]
    new_faces = {}
    for i in range(4):
        curr_edge = adj_edges[i][1]
        prev_edge = adj_edges[(i-rot_dir)%4][1]
        
        #current face we are looking at
        curr_face = s.d[adj_edges[i][0]]
        #previous face
        prev_face = s.d[adj_edges[(i-rot_dir)%4][0]]
        #edge of previous face
        prev_edge_tiles = get_edge_tiles(prev_face, prev_edge)
        #update edge of new face
        newf = set_edge_tiles(curr_face, curr_edge, prev_edge_tiles)
        #Update face
        new_faces[adj_edges[i][0]] = newf
    
    return new_faces
    
# Maps each face to a tuple. The first element of the tuple is an adjacent face,
# and the second element represents which edge of the adjacent face is to be
# rotated (0-top 1-right 2-bottom 3-left)
adj_edge_dict = {0:[(5,0),(4,0),(2,0),(1,0)], 1:[(0,3),(2,3),(3,3),(5,1)],\
                2:[(0,2),(4,3),(3,0),(1,1)],3:[(2,2),(4,2),(5,2),(1,2)],\
                4:[(2,1),(0,1),(5,3),(3,1)],5:[(0,0),(1,3),(3,2),(4,1)]}

# Returns the tiles on a particular edge of a particular face      
def get_edge_tiles(face, edge):
    edge_list = []
    # edge = 0 or 2, we need to compute row number
    # column will be either 0 or 1
    if (edge % 2) == 0:
        row = (edge*2) % 3
        for col in range(2):
            edge_list.append(face[row][col])

    # edge = 1 or 3, we need to compute column number
    # row will be either 0 or 1
    else:
        col = edge % 3
        for row in range(2):
            edge_list.append(face[row][col])
         
    return edge_list

# Sets the new tiles on a given edge of a given face
def set_edge_tiles(face, edge, updated_edge_tiles):
    newf = copy_face(face)
    # logic like get_edge_tiles
    if (edge % 2) == 0:
        edge = (edge*2) % 3
        newf[edge] = updated_edge_tiles

    # logic like get_edge_tiles        
    else:
        col = edge % 3
        for row in range(2):
            newf[row][col] = updated_edge_tiles[row]
    
    return newf

# Define operators
class Operator:

  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

face_rot_combinations = []
face_rot_combinations = list(itertools.product(range(6),[-1,1]))

OPERATORS = [Operator("Rotate face " + str(p) + str(" clockwise" if q == 1 else " anticlockwise"),
                      lambda s,p1=p, q1=q: can_rotate(s, p1, q1),
                      lambda s,p1=p, q1=q: rotate(s, p1, q1) )
             for (p, q) in face_rot_combinations]

# Returns count of those completed faces
# whose adjacent edges have the same color
def onelayercompleted(s):
    complete_faces = 0
    for face_num in range(6):
        face = s.d[face_num]
        # Check if all rows are the same
        if all(face[0] == row for row in face):
            # Check if all tiles in that row are same
            if all(face[0][0] == n for n in face[0]):
                # Check if the adjacent edges are complete as well
                if edges_complete(s, face_num):
                    complete_faces += 1
                    
    return complete_faces*10
    
# Check if the adjacent edges of a face are complete
def edges_complete(s, face_num):
    adj_edges = adj_edge_dict[face_num]
    for i in range(4):
        edge = adj_edges[i][1]
        # current adjacent face we are looking at
        adj_face = s.d[adj_edges[i][0]]
        # edge of current adjacent face
        adj_edge_tiles = get_edge_tiles(adj_face, edge)
        # Check if the tiles of the edge are equal
        if not (adj_edge_tiles[0] == adj_edge_tiles[1]):
            return False
    
    return True

# Return count of faces with all tiles of same color
def faces_completed(s):
    count = 0
    for face_num in range(6):
        face = s.d[face_num]
        if face[0][0] == face[0][1] == face[1][0] == face[1][1]:
            count += 1
            
    return count*6

# Return count of faces with 3 tiles of same color
def threescount(s):
    threescount = 0
    for face_num in range(6):
        face = s.d[face_num]
        face = list(itertools.chain.from_iterable(face))
        if face.count(max(set(face), key = face.count)) == 3:
            threescount += 1
            
    return threescount*2

# Return count of faces with 2 tiles of same color
def twoscount(s):
    twoscount = 0
    for face_num in range(6):
        face = s.d[face_num]
        face = list(itertools.chain.from_iterable(face))
        if face.count(max(set(face), key = face.count)) == 2:
            twoscount += 1
            
    return twoscount

# Return count of faces with all unique colors
def uniquecolorscount(s):
    uniquecolorscount = 0
    for face_num in range(6):
        face = s.d[face_num]
        if face[0][0] != face[0][1] != face[1][0] != face[1][1]:
            uniquecolorscount += 1
            
    return uniquecolorscount*6

FEATURES = [onelayercompleted, faces_completed, threescount, twoscount, uniquecolorscount]

# Return reqard after transition to state s
def Reward(s):
    if s == GOAL_STATE:
        reward = 100.0  # Goal has been reached 
    else:
        living_reward = -0.01
        reward = onelayercompleted(s) + faces_completed(s) + threescount(s) + twoscount(s) - uniquecolorscount(s) + living_reward
        
    return reward   # cost of living.

# Scramble the cube randomnly to get a start state
def scramble():
    global GOAL_STATE, num_moves
    START_STATE = GOAL_STATE
    rot_dir = [1,-1]
    while(goal_test(START_STATE)):
        for move_num in range(num_moves):
            START_STATE = rotate(START_STATE, random.choice(range(6)), random.choice(rot_dir))
                           
    print('Start state:')
    print(START_STATE)
    return START_STATE

START_STATE = scramble()

GOAL_TEST = lambda s: goal_test(s)

GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
