import json
from search import Graph, GraphProblem, UndirectedGraph, astar_search, best_first_graph_search, greedy_best_first_graph_search


StationName = ["Bogor",
               "Citayam",
               "Nambo",
               "Manggarai",
               "Jatinegara",
               "Bekasi",
               "TanahAbang",
               "RangkasBitung",
               "JakartaKota",
               "KampungBandan",
               "Rajawali",
               "Duri",
               "Tangerang",
               "Ancol",
               "TanjungPriok"]


def open_file_data():
    # Opening data from json files
    with open("KRL_STATION_COORDINATE.json") as f:
        krl_station_coordinates_data = json.loads(f.read())
    with open("KRL_STATION_GRAPH.json") as f:
        krl_station_graph_data = json.loads(f.read())
    return krl_station_coordinates_data, krl_station_graph_data


def do_greedy_search(initial: str, goal: str, undirectedGraph: Graph):
    # Validasi
    if initial not in StationName:
        raise TypeError("initial harus merupakan salah satu nama stasiun")
    elif goal not in StationName:
        raise TypeError("goal harus merupakan salah satu nama stasiun")
    
    krl_station_problem = GraphProblem(initial, goal, undirectedGraph)
    print(f"Menyelesaikan problem Greedy Search dari {initial} ke {goal}, langkah-langkah:")
    for i, node in enumerate(greedy_best_first_graph_search(krl_station_problem, krl_station_problem.h).path(), 1):
        print(i, node.state)



def do_astar_search(initial: str, goal: str, undirectedGraph: Graph):
    # Validasi
    if initial not in StationName:
        raise TypeError("initial harus merupakan salah satu nama stasiun")
    elif goal not in StationName:
        raise TypeError("goal harus merupakan salah satu nama stasiun")

    krl_station_problem = GraphProblem(initial, goal, undirectedGraph)
    print(f"Menyelesaikan problem A-Star Search dari {initial} ke {goal}, langkah-langkah:")
    for i, node in enumerate(astar_search(krl_station_problem).path(), 1):
        print(i, node.state)


def main():
    krl_station_coordinates_data, krl_station_graph_data = open_file_data()
    krl_station_undirected_graph = UndirectedGraph(krl_station_graph_data)
    krl_station_undirected_graph.location = krl_station_coordinates_data
    do_astar_search("Bogor", "TanjungPriok", krl_station_undirected_graph)
    do_greedy_search("Bogor", "TanjungPriok", krl_station_undirected_graph)
    do_astar_search("RangkasBitung", "Bekasi", krl_station_undirected_graph)
    do_greedy_search("RangkasBitung", "Bekasi", krl_station_undirected_graph)
    do_astar_search("Nambo", "Tangerang", krl_station_undirected_graph)
    do_greedy_search("Nambo", "Tangerang", krl_station_undirected_graph)


if __name__ == "__main__":
    main()
