"""
Group Members:
Ahsan
Keith
Zheng Yang
Wen Hao
Eson
"""

class Player:

    def __init__(self):
        """ Called during initialisation """

        self.frontier = []
        self.visited = []

        self.search_tree = []
        self.node_id = 1

    def reset(self):
        """
        To reset player to contain reset everything back to initial state
        """

        self.frontier = []
        self.visited = []

        self.search_tree = []
        self.node_id = 1

        # Adds initial state (entrance node state) to frontier
        entrance_state = {
            'position': self.entrance['position'],
            'actions' : self.entrance['actions']
        }

        root_node = Node(entrance_state, None)
        
        self.frontier.append(root_node)

        # Initialises the root node with information
        entrance_node = {
                'id' : 1,
                'state' : self.entrance['position'],
                'children' : [],
                'actions' : self.entrance['actions'],
                'removed' : False,
                'parent' : None
        }

        # Adds the root node (entrance node) to search tree
        self.search_tree.append(entrance_node)

    def set_maze(self, maze, entrance, exits):
        """
        To receive information of maze from the maze application

        input: maze to get the row and size
        input: entrance to get:
                a) coordinates of the cell
                b) available actions from the cell
                c) to know if it is an entrance
                d) to know if it is an exit
        input: exit are coordinates of exits
        """

        # Initializing the maze size with given information
        self.maze = {
            'n_row' : maze['n_row'],
            'n_col' : maze['n_col']
        }

        # Initializing the maze entrance
        self.entrance = {
            'position' : entrance['position'],
            'actions' : entrance['actions'],
            'entrance' : entrance['entrance'],
            'exit' : entrance['exit']
        }

        self.exits = exits

        # Adds initial state (entrance node state) to frontier
        entrance_state = {
            'position': entrance['position'],
            'actions' : entrance['actions']
        }

        # Creating a node class for the root node 
        root_node = Node(entrance_state, None)

        # Appending the root_node into the frontier
        self.frontier.append(root_node)

        # Initialises node of the entrance with information
        entrance_node = {
                'id' : 1,
                'state' : entrance['position'],
                'children' : [],
                'actions' : entrance['actions'],
                'removed' : False,
                'parent' : None
        }

        # Adds initial state (entrance node) to search tree
        self.search_tree.append(entrance_node)

    def checkDuplicateNode(self, current_node, node_list):
        """
        Loops through each node in node_list to 
        check if current node is a duplicate

        input: current_node to check if it is a duplicate node
        input: node_list is being loop through to check for duplicates

        returns True if it is a duplicate and False if it is not a duplicate
        """

        for node in node_list:

            # Compares if both nodes contains the same coordinates
            # using the dunder equals method from the Node class
            if current_node == node:
                # Returns True and exit the function immediately
                # if current node is a duplicate
                return True

        return False

    def expandAndReturnChildren(self, current_node):
        """
        Expand from current node to get its children based
        on the available actions it is provided

        input: current_node is to get its state information
        """

        # Gets coordinate of current node
        current_coordinate = current_node.state['position']

        # gets actions available for current node
        actions = current_node.state['actions']

        # An empty list that stores the children of the node
        children = []
        
        # Loops through all the actions in the node's action list
        for action in actions:

            if action == "n":
                action_coordinate = [0, 1]
            
            elif action == "e":
                action_coordinate = [1, 0]
            
            elif action == "s":
                action_coordinate = [0, -1]
            
            elif action == "w":
                action_coordinate = [-1, 0]
            
            # Calculates new coordinates as a result of an action
            new_coordinate = [current_coordinate[0] + action_coordinate[0],
                            current_coordinate[1] + action_coordinate[1]]

            # Creates child state
            child_state = {
                'position' : new_coordinate,
                'actions' : action
            }

            # Creates a Node object for each of the child
            # Node (state, parent) 
            child = Node(child_state, current_node)

            # Appends the child into the list of children
            children.append(child)

        # Retuns the list containing the children 
        return children

    def next_node(self):
        """
        To send coordinate of node to maze application to receive information
        about the new node

        returns: next node to be expanded in a 1D list
        """

        # Expanding the first node in the frontier list
        children = self.expandAndReturnChildren(self.frontier[0])

        # Adds the expanded nodes into the Visited list 
        self.visited.append(self.frontier[0])

        # Removes the node that was expanded
        del self.frontier[0]

        # Loops through each child in the children list 
        for child in children:

            # Checks for duplicates in visited list and frontier list 
            if (self.checkDuplicateNode(child, self.visited) != True
                    and self.checkDuplicateNode(child, self.frontier) != True):

                # Adds children to frontier list if there are no duplicates
                self.frontier.append(child)

                # Appends the child into the search tree
                self.append_node_to_search_tree(child)

            # Appends the redundantNode to the search tree 

            # Since its redundantNode value is True, it will be indicated 
            # on the search tree 
            else: 
                if (self.checkDuplicateNode(child, self.visited) == True): 
                    self.append_node_to_search_tree(child, True)

        # Returns the next node to be expanded 
        return self.frontier[0].state['position']

    def set_node_state(self, state):
        """
        Map application sends state of a node using this function

        input: state of a node in the form of dictionary
        returns solution(path)
        """

        # Extracts the actions available to the first node of the frontier
        self.frontier[0].state['actions'] = state['actions']

        # Checking if the node is an exit 
        if state['exit'] == True:

            # Assigns the first node of the frontier as an 'exit_node'
            exit_node = self.frontier[0]

            # To store the paths that leads to the solution 
            path = []

            # Performs backtracking to obtain the solution path 
            while exit_node is not None:
                path.append(exit_node.state['position'])
                exit_node = exit_node.parent
            solution_path = path[::-1]

            # Stores the solution_path
            solution = {
                'found' : True,
                'solution' : solution_path
            }

        else:
            solution = {
                'found' : False,
                'solution' : []
            }

        # Returns the path leading to the solution 
        return solution

    def append_node_to_search_tree(self, current_node, redundantNode = False):

        """
        Create a new node to be appended to search tree

        input: current_node to get the new_node position
        """

        # Increments the node's ID by one each time the function is called 
        self.node_id += 1

        # Creates a new node that will be appeded to the search tree
        new_node = {
            'id' : self.node_id,
            'state' : current_node.state['position'],
            'children': [],
            'actions': [],
            'removed' : False,
            'parent' : None
        }

        # Looping through each node in the search tree
        for node in self.search_tree:
            # Finds id of parent node for new node
            if node['state'] == current_node.parent.state['position']:
                
                # Adding the new node's ID into the parent's children list
                node['children'].append(self.node_id)

                # Adding the parent's action into the parent's action list
                # The action is found through how the child and parent coordinates
                # relate to each other 
                node['actions'] = current_node.parent.state['actions']

                # Adding the new_node's parent ID 
                new_node['parent'] = node['id']

        # To denote the node cannot be expanded due to it being redundant
        if redundantNode == True:
            new_node['removed'] = True

        # Adds the new_node into the search tree
        self.search_tree.append(new_node)

    def get_search_tree(self):
        """
        Returns: search tree up to the current node in the form of
                    of a list of nodes in the search tree
        """

        # Returns the search tree created in the 'append_node_to_search_tree' function
        return self.search_tree

class Node:
    
    def __init__(self, state = None, parent = None):
        """
        Initialise node attributes

        input: state holds the node's coordinates in a list and also actions
                in a dictionary
        input: parent node of the current node
        """

        self.state = state
        self.parent = parent

    # overrides dunder equals method to compare node position(coordinate)
    def __eq__(self, other_node):
        return other_node.state['position'] == self.state['position']