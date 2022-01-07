"""
@authors - Yehonatan Barel
           Nadav Moyal
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from GraphAlgo import GraphAlgo
import networkx as nx
from Node import Node
import matplotlib.pyplot as plt
from time import sleep
import math

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

# EPS = 0.0000000000001
EPS = 0.001

"""
real function to check on pokemon
we need to check what we want to give this function as an input, maybe we will just give it the pokemon id
"""
def find_pokemon_edge(pokemon):
    # for p in pokemons:
    for edge in list(graph_x.edges):
        edge_src = edge[0]   # [(0, 1), (0, 10),.... graph_x.edges look like this
        edge_dest = edge[1]
        edge_src_x = graph_x.nodes.get(edge_src)['pos'][0] # x
        edge_src_y = graph_x.nodes.get(edge_src)['pos'][1] # y
        edge_dest_x = graph_x.nodes.get(edge_dest)['pos'][0] # x
        edge_dest_y = graph_x.nodes.get(edge_dest)['pos'][1] # y
        dist_src_edge = math.sqrt( (edge_src_x - edge_dest_x) ** 2 + ( (edge_src_y-edge_dest_y) ** 2))
        dist_src_n = math.sqrt( (edge_src_x - pokemon.pos.x) ** 2 + ( (edge_src_y-pokemon.pos.y) ** 2))
        dist_n_dest = math.sqrt( (pokemon.pos.x - edge_dest_x) ** 2 + ( (pokemon.pos.y - edge_dest_y) ** 2))
        if dist_src_edge == dist_src_n + dist_n_dest + EPS or dist_src_edge == dist_src_n + dist_n_dest - EPS :
            if n.type > 0: # if type == 1
                return edge_src, edge_dest
            else:
                return edge_dest, edge_src
"""
just for test on node '999' that is on edge between nodes '0' <-> '1'
in here it doesnt check for the type because in the example i enter the node '999' but it's not like the pokemon, it doesnt have a type
also we need to check how much epsilon to gave to the function. the 'EPS' variable for epsilon in here is 0.001 because it fit the example i did
"""
def find_pokemon_edge_test(pokemon_id):
    pokemon_id_src_x = graph_x.nodes.get(pokemon_id)['pos'][0]  # x
    pokemon_id_src_y = graph_x.nodes.get(pokemon_id)['pos'][1]  # y

    for edge in list(graph_x.edges):
        edge_src = edge[0]   # [(0, 1), (0, 10),.... graph_x.edges look like this
        edge_dest = edge[1]
        edge_src_x = graph_x.nodes.get(edge_src)['pos'][0] # x
        edge_src_y = graph_x.nodes.get(edge_src)['pos'][1] # y
        edge_dest_x = graph_x.nodes.get(edge_dest)['pos'][0] # x
        edge_dest_y = graph_x.nodes.get(edge_dest)['pos'][1] # y
        dist_src_edge = math.sqrt( (edge_src_x - edge_dest_x) ** 2 + ( (edge_src_y-edge_dest_y) ** 2))
        dist_src_n = math.sqrt( (edge_src_x - pokemon_id_src_x) ** 2 + ( (edge_src_y-pokemon_id_src_y) ** 2))
        dist_n_dest = math.sqrt( (pokemon_id_src_x - edge_dest_x) ** 2 + ( (pokemon_id_src_y - edge_dest_y) ** 2))
        if abs(dist_src_edge - (dist_src_n + dist_n_dest)) <  EPS:
            # if n.type > 0: # if type == 1
            return edge_src, edge_dest
            # else:
            #     return edge_dest, edge_src

        """
        find if there is a free agent 
        @param agents: list of agents
        @return: the id of the free agent , if there is no free agent returns -1   
        """
def find_free_agent(agents):
    for agent in agents:
        if(agent.get_dest() == -1): #maybe "agent.dest" .. think its the same..
            return agent.get_id()
    # if we didnt find a free agent.
    return -1
"""
        find if there is a free agent 
        @param agent_id: list of agents
        @param p_edge_src: src of the pokemon's edge  
        @param p_edge_dest: dest of the pokemon's edge  
        @return: the id of the ideal agent and the idial path 
        Note: 
"""
def find_agent_edge(agent_id):
    agent_id_src_x = graph_x.nodes.get(agent_id)['pos'][0]  # x
    agent_id_src_y = graph_x.nodes.get(agent_id)['pos'][1]  # y

    for edge in list(graph_x.edges):
        edge_src = edge[0]  # [(0, 1), (0, 10),.... graph_x.edges look like this
        edge_dest = edge[1]
        edge_src_x = graph_x.nodes.get(edge_src)['pos'][0]  # x
        edge_src_y = graph_x.nodes.get(edge_src)['pos'][1]  # y
        edge_dest_x = graph_x.nodes.get(edge_dest)['pos'][0]  # x
        edge_dest_y = graph_x.nodes.get(edge_dest)['pos'][1]  # y
        dist_src_edge = math.sqrt((edge_src_x - edge_dest_x) ** 2 + ((edge_src_y - edge_dest_y) ** 2))
        dist_src_n = math.sqrt((edge_src_x - agent_id_src_x) ** 2 + ((edge_src_y - agent_id_src_y) ** 2))
        dist_n_dest = math.sqrt((agent_id_src_x - edge_dest_x) ** 2 + ((agent_id_src_y - edge_dest_y) ** 2))
        if abs(dist_src_edge - (dist_src_n + dist_n_dest)) < EPS:
            # if n.type > 0: # if type == 1
            return edge_src, edge_dest



    """
        find the agent with the minimal path weight
        @param agents: list of agents
        @param p_edge_src: src of the pokemon's edge  
        @param p_edge_dest: dest of the pokemon's edge  
        @return: the id of the ideal agent and the ideal path
        Note: 
    """
def find_ideal_agent(agents,p_edge_src,p_edge_dest):
    min_dist =100000000 # need to change to infinity
    ideal_path = []
    ideal_agent = -1
    for agent in agents:
        agent_edge = find_agent_edge(agent.id)
        agent_edge_src = agent_edge [0]
        agent_edge_dest =agent_edge [1]
        agent_path = nx.shortest_path(graph_x,agent_edge_dest,p_edge_dest,weight='weight')
        agent_path_dist = nx.path_weight(graph_x,agent_path,weight='weight')
        if(agent_path_dist<min_dist):
            ideal_path =agent_path
            min_dist=agent_path_dist
            ideal_agent=agent.id
        if (n in ideal_path):
            pass
        else:
            ideal_path.insert(len(ideal_path),p_edge_src)
            ideal_path.insert(len(ideal_path),p_edge_dest)
    return ideal_agent , ideal_path

"""
        find the path that agent need to reach 
        @param agent_id : id of the agent
        @param p_src: src of the pokemon's edge  
        @param p_dest: dest of the pokemon's edge  
        @return:list that represent the path that agent need to reach 
        Note: 
"""
def get_agent_path(agent_id,p_src,p_dest):
    # a=agents.get(agent_id) # need to check if this is the way to get agent by id. I think its wrong
    # a=agents[agent_id].id # this will work only if the agents is in a list seperate from the nodes graph and if their index will start from '0'. at start i put thier index to start from '1000'\'2000'
    a_index=agents.index(agent_id) # this is better, this will get us the index of our agent index in the list of the agents, so then we could go that index in the list and get the agent from it. this will work also if the agent_id is more then the len of list (like '1000')
    a=agents[a_index].id
    path=nx.shortest_path(graph_x,a.src ,p_dest)
    contained=0
    for p in path:
        if(p==p_src):
         contained =1
    if(contained==0):
         path.insert(len(path),p_src)
         path.insert(len(path),p_dest)
    return  path


# distance = math.sqrt( ((int(p1[0])-int(p2[0]))**2)+((int(p1[1])-int(p2[1]))**2) )
# def find_edge(graph:GraphAlgo):
#     for p in pokemons:
#         lst_of_pokemon_dest =
#         p_src=-1
#         p_dest=-1
#         for n_1 in graph_algo.get_graph().get_all_v().keys():
#             node_1: Node = graph_algo.get_graph().get_all_v().get(n_1)
#             for n_2 in graph_algo.get_graph().get_all_v().keys():
#                 node_2: Node = graph_algo.get_graph().get_all_v().get(n_2)
#                 dist_1_2 = math.sqrt( (node_1.get_x() - node_2.get_x()) ** 2 + ( (node_1.get_y()-node_2.get_y()) ** 2))
#                 dist_1_p = math.sqrt( (node_1.get_x() - p.pos.x) ** 2 + ( (node_1.get_y()-p.pos.y) ** 2))
#                 dist_p_2 = math.sqrt( (p.pos.x - node_2.get_x()) ** 2 + ( (p - node_2.get_y()) ** 2))
#                 if dist_1_2 == dist_1_p + dist_p_2:
#                     if p.type > 0: # if type == 1
#                         # graph_x.add_edge(node_1.get_key(), node_2.get_key())
#                         # lst_of_pokemon_dest[]
#                         p_src=node_1.get_key()
#                         p_dest=node_2.get_key()
#
#                     else: # if type == -1
#                         # graph_x.add_edge(node_2.get_key(), node_1.get_key())
#                         p_dest =node_1.get_key()
#                         p_src =node_2.get_key()
#                     for agent):
#                         if (agent.dest == -1)




                # dist_1_2 = math.sqrt(((nod - node_2.get_x())) ** 2) + ((int(p1[1]) - int(p2[1])) ** 2)):
                # if math.dist(node_1.get_x(),node_1.get_pos()) == math.dist(float(p.pos),node_1.get_pos()) + math.dist(p.pos,node_2.get_pos())





print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

 # get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y

print(f"-------------------------------------------min_x() = {min_x}")
print(f"-------------------------------------------max_x() = {max_x}")
print(f"-------------------------------------------min_y() = {min_y}")
print(f"-------------------------------------------max_y() = {max_y}")

def put_all_in_graph_algo_so_we_can_use_short_path_and_load_from_json_2():
    # load the json string into SimpleNamespace Object
    # ==== ADD ALL OF THE NODE TO THE GRAH-ALGO (POK_NODE, AGENT_NODE, NODE IN GIVEN GRAPH)
    for pok_node in pokemons:
        graph_algo.get_graph().add_node(pok_node.get_key(), pok_node.get_pos())
    for ag_node in agents:
        graph_algo.get_graph().add_node(ag_node, ag_node.get_pos())
def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values



def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

def put_agent_on_graph():
    num_of_agent = client.get_info()
    num_of_agent = num_of_agent.partition("agents")[2]
    num_of_agent = num_of_agent.replace("\"", '')
    num_of_agent = num_of_agent.replace(':', '')
    num_of_agent = num_of_agent.replace("}", '')
    num_of_agent = int(num_of_agent)
    print(f"num_of_agent = {num_of_agent}")
    for i in range(num_of_agent):
        client.add_agent('{\"id\":' + str(i) + '}')
# client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")




put_agent_on_graph()

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':


    """
    i add in here graph algo
    """
    # print(f"graph = {graph}")
    graph_x = nx.DiGraph()
    graph_algo = GraphAlgo()
    graph_algo.load_from_json_3(graph)
    for n in graph_algo.get_graph().get_all_v().keys():
        node:Node = graph_algo.get_graph().get_all_v().get(n)
        graph_x.add_node(node.get_key(),pos=(node.get_x(),node.get_y()),value=0,type=0)
        for dest_id,weight, in graph_algo.get_graph().all_out_edges_of_node(node.get_key()).items():
            graph_x.add_edge(node.get_key(),dest_id,weight=weight)
            # nx.set_node_attributes(graph_x,{0: 0},name= 'value') # node.get_key() - is
            # nx.set_node_attributes(graph_x,{1: 0},name= 'type') # node.get_key() - is
    graph_x.add_node(999, pos=(35.189,32.107)) ############################3 NOTICE THAT THIS NODE IS ADDED FOR TEST THE FUCNTION 'find_pokemon_edge_test'

    # print(nx.shortest_path(graph_x, source=0, target=6))
    lst = nx.shortest_path(graph_x, source=0, target=6)
    # print(nx.path_weight(graph_x, lst,weight='weight'))
    # print(f"graph_x.nodes = {graph_x.nodes}")
    # print(f"graph_x.nodes.data() = {graph_x.nodes.data()}")
    # print(f"graph_x.edges = {list(graph_x.edges)[0][0]}")
    # print(f"graph_x.edges = {list(graph_x.edges)[0][1]}")
    # print(f"graph_x.get_edge_data = {graph_x.get_edge_data(0,10)}")
    # print(f"graph_x.nodes.data() = {graph_x.nodes.data()}")
    # print(f"graph_x.nodes.get(0) = {graph_x.nodes.get(999)}")
    #
    print(f"================= {find_pokemon_edge_test(999)}")
    # for edge in list(graph_x.edges):
    #         print(f"edge_src = edge[0] = {edge[0]}")
    #         print(f"edge_dest = edge[1] = {edge[1]}")
    # print(f"graph_x.nodes.get(0)['pos'] = {graph_x.nodes.get(0)['pos'][0]}")

    #         for edge in list(graph_x.edges):
    #             edge_src = edge[0]
    #             edge_dest = edge[1]
    #             edge_src_x = graph_x.nodes.get()
    #             dist_src_edge = math.sqrt( (graph_x.get_edge_data() - node_2.get_x()) ** 2 + ( (node_1.get_y()-node_2.get_y()) ** 2))
    # print(f"dijkstra_path = {nx.dijkstra_path(graph_x, 0, 6, weight='weight')}")


    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    # print(f"=============={pokemons}")
    """
    i add in here the pokemon to graph algo and i gave an id to them start from 2000
    """
    for p in pokemons:
        p_id = 2000

        x, y, _ = p.pos.split(',')
        """
        i put in comment the two line below. i dont understand why but the pos of the pokemon
         is already scale and if we wont comment this two line and acutally do the
          scale function it mess up the pokemon pos
        """
        """
        ************* THE SOLUTION WAS TO CHANGE THE LINE ORDER LIKE I DID BLEOW INSTED *************
        ************* LIKE  IT WAS ON THE SUDENT_CODE THEY GAVE US, I DONT UNDESTAND WHY *************
         ************* IT IS HAPPENING BUT IT'S WORK NOW *************
        """
        p.pos = SimpleNamespace(x=float(x), y=float(y))
        graph_x.add_node(p_id,pos=(p.pos.x,p.pos.y),value=p.value,type=p.type)
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

        # graph_algo.get_graph().add_node(p_id, (p.pos.x,p.pos.y,0.0) )


        # graph_algo.get_graph().add_node(p_id, ((my_scale(float(x), x=True)),my_scale(float(y), y=True),0.0) )
        p_id = p_id+1
        # print(f"=========================================={pokemons}")


    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    # print(f"********************************{agents}")
    """
    i add in here the agent to graph algo and i gave an id to them start from 1000
    """
    # print(f"agents ********************************* {agents}")
    # print(f"agents ********************************* {agents[0].id}")
    for a in agents:
        x, y, _ = a.pos.split(',')
        print(f"======== BEFORE ======{a.pos}")
        """
        i put in comment the two line below. i dont understand why but the pos of the pokemon
         is already scale and if we wont comment this two line and acutally do the
          scale function it mess up the pokemon pos
        """
        """
        ************* THE SOLUTION WAS TO CHANGE THE LINE ORDER LIKE I DID BLEOW INSTED *************
        ************* LIKE  IT WAS ON THE SUDENT_CODE THEY GAVE US, I DONT UNDESTAND WHY *************
         ************* IT IS HAPPENING BUT IT'S WORK NOW *************
        """
        a.pos = SimpleNamespace(x=float(x), y=float(y))
        graph_x.add_node(a.id+1000,pos=(a.pos.x,a.pos.y),value=a.value,src=a.src,dest=a.dest,speed=a.speed)
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
        # print(f"vvvvvvvvvvvvvvv{a.pos.x,a.pos.y}")
        # graph_algo.get_graph().add_node(a.id+1000, (a.pos.x,a.pos.y,0.0))
        print(f"======== AFTER ======{a.pos}")

        # graph_algo.get_graph().add_node(a.id+1000, ((my_scale(float(x), x=True)),my_scale(float(y), y=True),0.0))
    print(f"graph_x.nodes = {graph_x.nodes}")
    print(f"graph_x.nodes.data() = {graph_x.nodes.data()}")
    pos = nx.get_node_attributes(graph_x, 'pos')
    nx.draw(graph_x,pos,with_labels=True)
    plt.show()
   # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.Nodes:
        """
        also from here i comment this two scale function and just put x,y
        """
        # x=n.pos.x
        # y=n.pos.y
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    zip_agent_pokemon = zip(agents,pokemons)
    # print(f"zip_agent_pokemon = {zip_agent_pokemon}")
    for agent ,p in zip_agent_pokemon:
        # print(p)
        # agent.pos = p.pos
        pygame.draw.circle(screen, Color(122, 61, 23),(int(agent.pos.x-5), int(agent.pos.y-5)), 10)
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
    # for agent in agents:
    #     agent.pos = pokemons[0].pos #(pokemons[0].pos.x, pokemons[0].pos.y, 0.0)
    #     pygame.draw.circle(screen, Color(122, 61, 23),
    #                        (int(agent.pos.x-5), int(agent.pos.y-5)), 10)
    # # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    # for p in pokemons:
    #     pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)


    # print(f"graph_algo = {graph_algo.get_graph()}")
    # print(f"graph_algo.get_graph().all_out_edges_of_node() = {graph_algo.get_graph().all_out_edges_of_node(1000)}")
    # print(f"graph_algo.get_graph().get_all_v() = {graph_algo.get_graph().get_all_v().keys()}")

    go_to = []
    #
    # for n in graph_x.nodes.keys():
    #     if n < 1000: # if the node is a node in the graph - continue
    #         continue
    #     if n >= 2000: # if p in an pokemon
    #        p_src , p_dest = find_pokemon_edge(a)
    #        free_agent_id = find_free_agent(agents) # need to check if it recognize the agents.
    #        if ( free_agent_id != -1 ): # if we have found a free agent
    #            a_path =get_agent_path(free_agent_id,p_src,p_dest)






    #      if a < 1000: # if the node is a node in the graph - continue
    #              #     continue
    #     if a >=1000 and a < 2000: # if the node is an agent , check him to the pokemon start from index 2000
    #         for p in graph_algo.get_graph().get_all_v().keys():
    #             if p >= 2000: # if p in an pokemon
    #                 find_the_agent: Node = graph_algo.get_graph().get_all_v().get(a)
    #                         if find_the_agent== -1:
    #                             close_node = graph_algo.shortest_path(n_1,n_2)[0]

    # for n in graph_algo.get_graph().get_all_v():

    # for a in graph_algo.get_graph().get_all_v().keys():
    #     # if a < 1000: # if the node is a node in the graph - continue
    #     #         #     continue
    #     if a >=1000 and a < 2000: # if the node is an agent , check him to the pokemon start from index 2000
    #         for p in graph_algo.get_graph().get_all_v().keys():
    #             if p >= 2000: # if p in an pokemon
    #                 find_the_agent: Node = graph_algo.get_graph().get_all_v().get(a)
    #                         if find_the_agent== -1:
    #                             close_node = graph_algo.shortest_path(n_1,n_2)[0]




    # choose next edge
    # for agent in agents:
    #     if agent.dest == -1:
    #         next_node = (agent.src - 1) % len(graph.Nodes)
    #         # agent.pos = pokemons
    #         ## ============= in here i gave the agent the samoe pos as the pokemon ====================
    #         print(f"=========================================={pokemons}")
    #         print(f"***************************************8**{pokemons[0].pos}")
    #         print(f"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{pokemons[0].pos.x}")
    #         print(f"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy{pokemons[0].pos.y}")
    #         # agent.pos = (pokemons[0].pos.x, pokemons[0].pos.y ,0.0)
    #         print(f"agent.pos = {agent.pos}")
    #         # for p in pokemons:
    #
    #
    #         client.choose_next_edge(
    #             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
    #         ttl = client.time_to_end()
    #         print(ttl, client.get_info())
    #
    # client.move()
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# game over: