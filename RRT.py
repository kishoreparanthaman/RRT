import pygame
import random
import math


class rrtstar:
    def __init__(self, start, goal, mapdimensions, obsdim, obsnum):

        (x, y) = start
        self.start = start
        self.goal = goal
        self.mapdimensions = mapdimensions
        # print(mapdimensions)
        self.mapw, self.maph = self.mapdimensions
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.fill((255, 255, 255))
        self.nodeRad = 2
        self.nodeThickness = 0
        self.edgeThinckness = 1
        self.step_length = 50
        self.obstacles = []

        self.obsdim = obsdim
        self.obsnum = obsnum
        self.goal_flag = False
        self.x = []
        self.y = []
        self.parent = []

        # initialise the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        self.goalstate = None
        self.path = []



        # colors
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (70, 70, 70)
        self.orange = (255, 165, 0)
        self.pink = (255,192,203)

    def dmap(self, obstacles):
        print(obstacles)
        pygame.draw.circle(self.map, self.blue, self.start, self.nodeRad + 5, 0)
        pygame.draw.circle(self.map, self.green, self.goal, self.nodeRad + 10, 0)
        self.obstacle(obstacles)

    def dpath(self, path):
        cost=0
        for node in path:
            cost+=1 # unit cost between each node
            pygame.draw.circle(self.map, self.red, node, self.nodeRad + 3, 0)
        return cost


    def obstacle(self, obstacles):
        i = 1
        obstaclelist = obstacles.copy()
        while (len(obstaclelist) > 0):
            obstacle = obstaclelist.pop(0)
            if i==1:
                pygame.draw.rect(self.map, self.pink, obstacle)
                print("polygon")
            elif i % 2 == 0:
                pygame.draw.rect(self.map, self.grey, obstacle)
            else:
                pygame.draw.ellipse(self.map, self.orange, obstacle)
            i += 1


    def Randomrectangle(self):
        uppercorner_x = int(random.uniform(0,self.mapw-self.obsdim))
        uppercorner_y = int(random.uniform(0,self.maph-self.obsdim))
        return (uppercorner_x,uppercorner_y)


    def makeobs(self,manualobstacle):
        obs = []
        (man_up_x, man_lip_y), (man_low_x, man_low_y) = manualobstacle
        Rect = pygame.Rect((man_up_x, man_lip_y), (man_low_x, man_low_y))
        obs.append(Rect)
        for i in range (0,self.obsnum):
            # print(self.obsnum)
            rectangle= None
            startgoalcol = True

            while startgoalcol:
                upper = self.Randomrectangle()
                randobsdim1 = random.randint(self.obsdim-40,self.obsdim+ 40)
                randobsdim2 = random.randint(self.obsdim - 40, self.obsdim + 40)
                rectangle = pygame.Rect(upper,(randobsdim1,randobsdim2))
                if rectangle.collidepoint(self.start) or rectangle.collidepoint(self.goal):
                    startgoalcol= True
                    # print(i)
                else :
                    startgoalcol = False
            obs.append(rectangle)
        self.obstacles = obs.copy()
        return obs


    def add_node(self, n, x, y):
        self.x.insert(n,x)
        self.y.insert(n,y)

    def remove_node(self,n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child,parent)

    def remove_edge(self,n):
        self.parent.pop(n)

    def number_of_nodes(self):
        return len(self.x)

    def distance(self, n1, n2):
        (x1,y1) = (self.x[n1], self.y[n1])
        (x2,y2) = (self.x[n2], self.y[n2])
        return ((((float(x1)-float(x2))**2 )+ ((float(y1)-float(y2))**2)))**0.5

    def sample_env(self):
        x = int(random.uniform(0, self.mapw))
        y = int(random.uniform(0, self.maph))
        return x,y

    def nearest(self,n):
        dmin = self.distance(0,n)
        nnear = 0
        for i in range(0,n):
            if self.distance(i,n)<dmin:
                dmin = self.distance(i,n)
                nnear= i
        return nnear


    def isfree(self):
        n = self.number_of_nodes()-1
        (x,y) = (self.x[n], self.y[n])
        obs = self.obstacles.copy()
        while len(obs)>0:
            rectangle = obs.pop(0)
            if rectangle.collidepoint(x,y):
                self.remove_node(n)
                return False
        return True

    def crossobstacle(self,x1,x2,y1,y2):
        obs= self.obstacles.copy()
        while(len(obs)>0):
            rectangle = obs.pop(0)
            for i in range(0,1001):
                u = i/1000
                x = x1*u + x2*(1-u)
                y = y1*u + y2*(1-u)
                if rectangle.collidepoint(x,y):
                    return True
        return False

    def connect(self,n1,n2):
        (x1,y1) = (self.x[n1],self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        if self.crossobstacle(x1,x2,y1,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True

    def step(self, nnear, nrand, steplength):
         d = self.distance(nnear,nrand)
         if d>steplength:
             u = steplength/d
             (xnear,ynear) = (self.x[nnear], self.y[nnear])
             (xrand, yrand) = (self.x[nrand], self.y[nrand])
             (px,py)  = (xrand - xnear, yrand - ynear)
             theta = math.atan2(py,px)
             (x,y) = (int(xnear+steplength * math.cos(theta)), int(ynear + steplength * math.sin(theta)))
             self.remove_node(nrand)
             if abs(x-self.goal[0])<steplength and abs(y-self.goal[1])<steplength:
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate = nrand
                self.goal_flag= True
             else:
                self.add_node(nrand,x,y)

    def path_to_goal(self):
        cost = 0
        if self.goal_flag:
            self.path=[]
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while(newpos != 0):
                self.path.append(newpos)
                newpos = self.parent[newpos]
                self.path.append(0)
        return self.goal_flag


    def get_path_cord(self):
        pathcord = []
        for node in self.path:
            x,y = (self.x[node],self.y[node])
            pathcord.append((x,y))
        print("Path Coordinates :")
        print(pathcord)
        return pathcord


    def extend(self):
        stepl = self.step_length
        n = self.number_of_nodes()
        x,y = self.sample_env()
        self.add_node(n,x,y)
        if self.isfree():
            xnearest = self.nearest(n)
            self.step(xnearest,n,stepl)
            self.connect(xnearest,n)
        return self.x, self.y, self.parent


def main():
    dimensions = (1000, 1000)
    start = (500, 50)
    goal = (510, 700)
    obsdim = 50
    obsnum = 30
    iteration =0
    manual_obstacle= [(350,390),(25,30)]
    pygame.init()
    rrtpath = rrtstar(start,goal,dimensions,obsdim,obsnum)
    obstacles = rrtpath.makeobs(manual_obstacle)
    rrtpath.dmap(obstacles)



    while(not rrtpath.path_to_goal()):

        X, Y, Parent = rrtpath.extend()
        pygame.draw.circle(rrtpath.map, rrtpath.grey, (X[-1], Y[-1]), rrtpath.nodeRad+2, 0)
        pygame.draw.line(rrtpath.map, rrtpath.blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), rrtpath.edgeThinckness)
        pygame.display.update()
        iteration+=1
    cost=rrtpath.dpath(rrtpath.get_path_cord())
    print("The cost of the path is "+ str(cost) +" units")
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)


if __name__ == '__main__':
    main()
