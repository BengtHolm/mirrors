# A simple application that solves the Mirror and laser cases in
# the instruction sheet from Ascent Robotics
# Assumes numpy is installed



import numpy as np

def readInput(f):
	# Reads input in format presented in instructions
    r,c,m,n =np.fromfile(f, dtype=int, count=4, sep=" ")
    coordinates = np.fromfile(f, dtype=int, count=(m+n)*2, sep=" ").reshape((m+n,2))
    grid = np.zeros([r,c],dtype=int)
    
    for i in range(m):
        grid[coordinates[i][0]-1,coordinates[i][1]-1] = 1
        
    for j in range(m, m+n):
        grid[coordinates[j][0]-1,coordinates[j][1]-1] = -1
        
    return grid
	
def step_in_beam_direction(cur_pos, cur_dir):
	# This function handles the generation of one step in the grid.
	# parameters are current position (cur_pos or cp)
	# and current direcion(cur_dir or cd), one of r,l,u,d.
	
    if cur_dir == 'r':
        cur_pos[1] += 1
    elif cur_dir == 'l':
        cur_pos[1] -= 1
    elif cur_dir == 'd':
        cur_pos[0] += 1
    elif cur_dir == 'u':
        cur_pos[0] -= 1
    else:
        print("Error direction not correct")
    return cur_pos
        

def find_next_mirror(grid, cp, cd, inside= True):
	# This function follows the beam until the next mirror is found
	# Terminates if beam leaves grid and returns exit position
    rows,cols = grid.shape
    current_object = 0
    while current_object == 0:
        cp = step_in_beam_direction(cp, cd)
        in_row = 0 < cp[0] & cp[0] < rows + 1
        in_col = 0 < cp[1] & cp[1] < cols + 1
        if(in_row & in_col):
            current_object = grid[cp[0]-1,cp[1]-1]
            
        else:
            inside = False
            return cp,inside
    
    return cp,inside
	
def bounce_off_mirror(cd, orientation):
	# Changes direction of beam at mirror.
	# Orientation / is represented by 1
	# Orientation \ is represented by -1
    if orientation == 1:
        if cd == 'r':
            cd = 'u'
        elif cd == 'l':
            cd = 'd'
        elif cd == 'u':
            cd = 'r'
        elif cd == 'd':
            cd = 'l'
    elif orientation == -1:
        if cd == 'r':
            cd = 'd'
        elif cd == 'l':
            cd = 'u'
        elif cd == 'u':
            cd = 'l'
        elif cd == 'd':
            cd = 'r'
    else:
        print("No mirror ")

    return cd
            
			
def trace_beam(grid,cp,cd):
	# Traces beam and returns exit point
	# Our entry point is cp=[1,0]
	# and direction cd = 'r'
	
    inside = True
    while inside:
        cp, inside = find_next_mirror(grid, cp, cd, inside)

        if inside:
            orientation = grid[cp[0]-1,cp[1]-1]
            cd = bounce_off_mirror(cd, orientation)
        else:
            return cp

    
	
def detected(grid):
	# This function determines whether the beam reaches the detector
	# positioned to the right of the bottom right square
    rows,cols = grid.shape
    cp=[1,0]
    cd = 'r'
    cp = trace_beam(grid,cp,cd)
    return cp == [rows,cols+1]
	
	
def step_and_place_mirror(grid, cp, cd, inside= True, count=0, placement =[]):
	# Traces the beam and inserts a mirror at each vacant square
	# Then checks if detector is activated
    rows,cols = grid.shape
    current_object = 0
    while current_object == 0:
        cp = step_in_beam_direction(cp, cd)
        in_row = 0 < cp[0] & cp[0] < rows + 1
        in_col = 0 < cp[1] & cp[1] < cols + 1
        if(in_row & in_col):
            current_object = grid[cp[0]-1,cp[1]-1]
            if current_object == 0:
                ac = insert_mirror_and_examine(grid,cp)
                if ac == True:
                    count += 1
                    placement.append(cp.copy())
        else:
            inside = False
            return cp, inside,count,placement
    
    return cp, inside,count,placement
    
def insert_mirror_and_examine(grid,cp):
	# Inserts both orientations for the mirror and checks
	# if detector is activated	
    activates = False
    grid[cp[0]-1,cp[1]-1] = 1
    if(detected(grid)):
        #print("Detection activated with / mirror at " + str(cp))
        activates = True
    grid[cp[0]-1,cp[1]-1] = -1
    if(detected(grid)):
        #print("Detection activated with \\ mirror at " + str(cp))
        activates = True
    grid[cp[0]-1,cp[1]-1] = 0
   
    return activates
    
def trace_beam_and_place_mirror(grid,cp,cd):
    inside = True
    count = 0
    placement = []
    while inside:
        cp, inside, count, placement = step_and_place_mirror(grid, cp, cd, inside, count, placement)

        if inside:
            orientation = grid[cp[0]-1,cp[1]-1]
            cd = bounce_off_mirror(cd, orientation)
        else:
            return count, placement
			
def collect_info_about_grid(grid):
    det=detected(grid)
    cp=[1,0]
    cd = 'r'
    n_of_mirrors,placement=trace_beam_and_place_mirror(grid, cp, cd)
    
    return n_of_mirrors,placement,det
	
def summarize(file = 'case1.txt'):
	# Returns results in format as described by the info sheet
    result = ""
    f = open(file, "r")
    grid=readInput(f)

    k, placement, activates_w_no_mirror=collect_info_about_grid(grid)

    if (k==0 and activates_w_no_mirror==False):
        result = "Impossible"
    
    if k==0 and activates_w_no_mirror==True:
        result = str(k)
        
    if len(placement)>0:
        result = str(k) + ' ' + str(placement[0][0]) + ' ' + str(placement[0][1])
        
    f.close()
    return result

