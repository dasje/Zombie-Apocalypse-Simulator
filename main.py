"""
Zombie Apocalypse simulator
Apocalypse class manages humans best escape options and zombies best chase options.
Dependencies available on codeskulptor.org
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = poc_grid.Grid.__str__(self)
        ans += "\nHumans: " + str(self._human_list)
        ans += "\nZombies: " + str(self._zombie_list)
        return ans

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zom in self._zombie_list:
            yield zom
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for hum in self._human_list:
            yield hum
        return

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # new grid same size as board, initialize cells to empty
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        # 2d list distance field, each entry product of grid height/width
        d_f = [[self.get_grid_height() * self.get_grid_width() for dummy_height in range(self.get_grid_width())]
               for dummy_width in range(self.get_grid_height())]
        # boundary queue that is copy of zombie or human list
        q_list = []
        if entity_type == HUMAN:
            q_list = self._human_list[:]
        else:
            q_list = self._zombie_list[:]
        bound = poc_queue.Queue()
        for item in q_list:
            bound.enqueue(item)
        # for cells in queue visited = FULL, distance field = 0. Use queue class
        for cell in bound:
            visited.set_full(cell[0], cell[1])
            d_f[cell[0]][cell[1]] = 0
        for h_c in range(self.get_grid_height()):
            for w_c in range(self.get_grid_width()):
                if self.is_empty(h_c, w_c) == False:
                    visited.set_full(h_c, w_c)
        # while boundary is not empty
        while len(bound) > 0:
            #	current cell = dequeue boundary
            current_cell = bound.dequeue()
            #	for all neighbour cell of current cell
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                #		if neighbour cell is not in visited and passable
                if visited.is_empty(neighbor[0], neighbor[1]) == True:
                    #			add neighbor cell to visited grid
                    visited.set_full(neighbor[0], neighbor[1])
                    #			enqueue neighbor cell into boundary
                    bound.enqueue(neighbor)
                    #			update neighbor distance to current cell +1
                    d_f[neighbor[0]][neighbor[1]] = d_f[current_cell[0]][current_cell[1]] + 1
        return d_f

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        # height, width = self.get_grid_height(), self.get_grid_width
        zdf = zombie_distance_field
        # iter through human list
        for human in range(self.num_humans()):
            # get 8x neighbors from each human
            neighbors = self.eight_neighbors(self._human_list[human][0], self._human_list[human][1])
            # move human to cell with highest number: make sure not obstacle
            dist_list = []
            for neighbor in neighbors:
                empty = self.is_empty(neighbor[0], neighbor[1])
                if empty == True:
                    # if neighbor != self.get_grid_height()*self.get_grid_width():
                    dist_list.append((zdf[neighbor[0]][neighbor[1]], neighbor))
            hum = max(dist_list)[1]
            zombied = zdf[hum[0]][hum[1]]
            if zombied == EMPTY:
                pass
            else:
                self._human_list[human] = hum

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        # height, width = self.get_grid_height(), self.get_grid_width
        hdf = human_distance_field
        # iter through zombie list
        for zombie in range(self.num_zombies()):
            if hdf[self._zombie_list[zombie][0]][self._zombie_list[zombie][1]] == 0:
                pass
            else:
                neighbors = self.four_neighbors(self._zombie_list[zombie][0], self._zombie_list[zombie][1])
                dist_list = []
                for neighbor in neighbors:
                    dist_list.append((hdf[neighbor[0]][neighbor[1]], neighbor))
                # find closest human in hdf
                zom = min(dist_list)[1]
                # move zombie in that direction
                self._zombie_list[zombie] = zom


# Start up gui for simulation

# poc_zombie_gui.run_gui(Apocalypse(3, 3, [], [], [(2, 2)]))
