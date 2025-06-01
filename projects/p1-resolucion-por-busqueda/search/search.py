# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from queue import Empty
from re import S
import ssl
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """


        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # En un stack almacenaremos los estados frontera posibles del agente pacman
    # y en otro, en paralelo, el camino a seguir hasta cada uno de ellos
    frontier_states = util.Stack()
    path_reached    = util.Stack()
    # lista de los estados expandidos que ya han sido "analizados" por el codigo
    reached_states  = []

    # comenzamos añadiendo como estado frontera el estado inicial
    frontier_states.push(problem.getStartState())
    path_reached.push([])
    reached_states.append(problem.getStartState())

    # ejecutamos mientras tengamos posibles estados frrontera
    while not frontier_states.isEmpty():
        actual_node = frontier_states.pop()
        path        = path_reached.pop()
        # la primera vez, path almacenara una lista vacia

        if problem.isGoalState(actual_node):
            return path
        else:
            # para cada posible hijo del nodo actual
            for child in problem.getSuccessors(actual_node):
                # almacenamos la posicion que se alcancaria y el movimiento a realizar
                # hasta la misma 
                next_node = child[0]
                next_mov = child[1]
                # en caso de que la nueva posicion a alcanzar no se haya registrado
                # hace lo propio y guarda el camino hasta la misma en el stack correspondiente
                if next_node not in reached_states:
                    frontier_states.push(next_node)
                    path_reached.push(path + [next_mov])
                    reached_states.append(actual_node)


    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # ahora utilizaremos colas en vez de stacks para ir analizando en anchura en vez
    # de en profundidad (gracias a la ordenacion de FIFO de esta estructura de datos)
    frontier_states = util.Queue()
    path_reached    = util.Queue()
    reached_states  = []

    # guardamos primero como estado frontera el estado inicial
    frontier_states.push(problem.getStartState())
    path_reached.push([])

    # ejecutamos mientras tengamos posibles estados frontera
    while not frontier_states.isEmpty():
        actual_node = frontier_states.pop()
        path        = path_reached.pop()
        # la primera vez, path almacenara una lista vacia

        if problem.isGoalState(actual_node):
            return path
        else:
            # esta vez mira primero si el nodo actual esta ya registrado
            # y en caso de no estaro, lo expande
            if actual_node not in reached_states:
                # registra el nodo actual en la lista de nodos ya visitados
                reached_states.append(actual_node)

                # para cada hijo
                for child in problem.getSuccessors(actual_node):
                    # guardamos la posicion que alcanzaria y el movimiento hacia la misma
                    next_node = child[0]
                    next_mov = child[1]
                    # y pasamos dicha informacion a las correspondientes colas
                    frontier_states.push(next_node)
                    path_reached.push(path + [next_mov])

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # ahora emplearemos colas con prioridad para ir ordenando los estados
    # frontera acorde al coste que genere el camino ya recorrido
    frontier_states = util.PriorityQueue()
    path_reached    = util.PriorityQueue()
    reached_states  = []

    # comenzamos añadiendo el estado inicial a la cola de fronteras con prioridad 0
    frontier_states.push(problem.getStartState(), 0)
    # el primer camino almacenado (lista vacia) tambien tendra prioridad 0
    path_reached.push([], 0)

    # ejecutamos mientras tengamos posibles estados frontera
    while not frontier_states.isEmpty():
        actual_node = frontier_states.pop()
        path        = path_reached.pop()
        # la primera vez, path almacenara una lista vacia

        if problem.isGoalState(actual_node):
            return path
        else:
            # comprueba que aun no se habia registrado el nodo actual
            if actual_node not in reached_states:
                # lo registra en la lista de alcanzados (o expandidos)
                reached_states.append(actual_node)

                # para cada hijo
                for child in problem.getSuccessors(actual_node):
                    # guardamos la posicion que alcanzaria y el movimiento hacia la misma
                    next_node = child[0]
                    next_mov = child[1]
                    # calculamos el coste del camino hasta el nodo hijo en cuestion
                    mov_cost = problem.getCostOfActions(path + [next_mov])
                    # añadimos el hijo a los estados frontera usando como prioridad
                    # el coste que generaria el camino hasta el mismo (desde el inicio)
                    frontier_states.push(next_node, mov_cost)
                    # con la misma prioridad, añadimos el camino a su cola
                    path_reached.push(path + [next_mov], mov_cost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#-- AQUI EMPIEZA EL CODIGO MODIFICADO 
"*** MODIFICACION 1 ***"
def chebyshovDistance(state, problem=None):
    """
    Heuristica que debera calcular la distancia de Chebyshov para la busqueda A*
    D = max(abs(x2-x1),abs(y2-y1))
    """
    # extrae las coordenadas x e y del estado actual y el estado de la meta
    x1, y1 = state
    x2, y2 = problem.goal

    # calcula la distancia de Chebyshov usando la formula dada anteriormente
    Chev_dist = max(abs(x2-x1),abs(y2-y1))

    return Chev_dist


"*** MODIFICACION 2 ***"
def getCostOfActions2(actions, problem):
    """
    Toma la lista de acciones de las que se quiere calcular el coste y el problema
    como parametros
    """

    N = "North"
    p = problem

    # crea una lista de acciones nueva en la que se copiaran todas excepto las
    # que sean hacia el norte
    actions_without_north = []
    for action in actions:
        if not (action == N):
            actions_without_north.append(action)

    # calcula ahora el coste con la funcion original de problem.getCostOfActions
    cost = p.getCostOfActions(actions_without_north)
    # dado que cada accion tendria el doble de su coste original, devuelve el
    # doble del coste total de dichas acciones (equivalente)
    return (2*cost)



def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # seguimos empleando colas con ordenacion por prioridad para los estados frontera
    # y los caminos a seguir
    frontier_states = util.PriorityQueue()
    path_reached    = util.PriorityQueue()
    reached_states  = []

    # añadimos el estado inicial con la prioridad que nos devuelva la heuristica para el mismo
    frontier_states.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    path_reached.push([], heuristic(problem.getStartState(), problem))

    # ejecutamos mientras tengamos posibles estados frontera
    while not frontier_states.isEmpty():
        actual_node = frontier_states.pop()
        path        = path_reached.pop()
        # la primera vez, path al acenara una lista vacia

        if problem.isGoalState(actual_node):
            return path
            
        # comprueba que aun no se habia registrado el nodo actual
        if actual_node not in reached_states:
            reached_states.append(actual_node)

            # para cada hijo
            for child in problem.getSuccessors(actual_node):
                # guardamos la posicion que alcanzaria y el movimiento hacia la misma
                next_node = child[0]
                next_mov = child[1]
                # extraemos por un lado el coste del camino hasta dicho nodo
                # y por otro el que generaria hasta el objetivo (con la heuristica)
                "MODIFICACION 2 APLICADA AQUI (LLAMADA A LA FUNCINO getCostOfActions2)"
                mov_cost = getCostOfActions2(path + [next_mov], problem)
                h        = heuristic(next_node, problem)
                # usando la suma de dichos costes como prioridad, añadimos el nodo hijo y
                # el camino hasta el mismo a sus correspondientes colas
                frontier_states.push(next_node, mov_cost + h)
                path_reached.push(path + [next_mov], mov_cost + h)

    util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
