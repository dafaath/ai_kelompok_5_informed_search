import json
from os import error
from search import Graph, GraphProblem, UndirectedGraph, astar_search, best_first_graph_search, greedy_best_first_graph_search


class TestCase():
    initial: str
    goal: str
    astar_cost: float
    greedy_cost: float
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

    def __init__(self, initial: str, goal: str):
        if initial not in self.StationName:
            raise TypeError(f"{initial} harus merupakan salah satu nama stasiun")
        elif goal not in self.StationName:
            raise TypeError(f"{goal} harus merupakan salah satu nama stasiun")
        self.initial = initial
        self.goal = goal

    def update_cost(self, astar_cost: float, greedy_cost: float):
        self.astar_cost = astar_cost
        self.greedy_cost = greedy_cost


def open_file_data():
    # Opening data from json files
    with open("KRL_STATION_COORDINATE.json") as f:
        krl_station_coordinates_data = json.loads(f.read())
    with open("KRL_STATION_GRAPH.json") as f:
        krl_station_graph_data = json.loads(f.read())
    return krl_station_coordinates_data, krl_station_graph_data


def do_search(search_type: str, initial: str, goal: str, undirected_graph: Graph, coordinates_data, graph_data, verbose=True):
    krl_station_problem = GraphProblem(initial, goal, undirected_graph)

    if(verbose):
        print(f"{search_type} Search")

    # Validasi
    if(search_type == "astar"):
        path = astar_search(krl_station_problem).path()
    elif(search_type == "greedy"):
        path = greedy_best_first_graph_search(krl_station_problem, krl_station_problem.h).path()
    else:
        raise TypeError("search_type hanya bisa astar dan greedy")

    cost = 0
    for i, node in enumerate(path, 1):
        if(verbose):
            print(i, node.state)
        if(i == 1):
            pass
        else:  # Mengambil graph data dari file dan menghitung cost setiap state yang dilewati
            cost += graph_data[node_state_before][node.state]
        node_state_before = node.state  # Menyimpan node yang sebelumnya (i-1)
    return cost


def compare_astar_and_greedy(test_cases: list, undirected_graph: Graph, coordinates_data, graph_data):
    for test in test_cases:
        print(f"Melakukan perbandingan dari {test.initial} ke {test.goal}")
        astar_cost = do_search("astar", test.initial, test.goal,
                               undirected_graph, coordinates_data, graph_data)
        greedy_cost = do_search("greedy", test.initial, test.goal,
                                undirected_graph, coordinates_data, graph_data)
        test.update_cost(astar_cost, greedy_cost)


def check_different_cost():
    """Mencari apakah ada perbedaan dari hasil greedy search dan astar search untuk setiap stasiun yang ada"""
    coordinates_data, graph_data = open_file_data()
    undirected_graph = UndirectedGraph(graph_data)
    undirected_graph.location = coordinates_data

    # Menambahkan test case untuk semua kemungkinan stasiun
    test_cases = []
    for initial in TestCase.StationName:
        for goal in TestCase.StationName:
            if(initial == goal):
                pass
            else:
                test_cases.append(TestCase(initial, goal))

    is_there_difference = False
    sum_test = 0
    for test in test_cases:
        astar_cost = do_search("astar", test.initial, test.goal,
                               undirected_graph, coordinates_data, graph_data, verbose=False)
        greedy_cost = do_search("greedy", test.initial, test.goal,
                                undirected_graph, coordinates_data, graph_data, verbose=False)
        test.update_cost(astar_cost, greedy_cost)
        if(astar_cost != greedy_cost):
            is_there_difference = True
            print(test.initial, test.goal, astar_cost, greedy_cost)
        sum_test += 1
    print(f"Testing {sum_test}/{len(test_cases)} cases")
    print(f"Is there any difference? {is_there_difference}")


def main():
    coordinates_data, graph_data = open_file_data()
    undirected_graph = UndirectedGraph(graph_data)
    undirected_graph.location = coordinates_data

    # Initialize train path to test
    test_cases = []
    test_cases.append(TestCase("Bogor", "TanjungPriok"))
    test_cases.append(TestCase("RangkasBitung", "Bekasi"))
    test_cases.append(TestCase("Nambo", "Tangerang"))
    test_cases.append(TestCase("Nambo", "RangkasBitung"))
    test_cases.append(TestCase("Nambo", "Rajawali"))
    test_cases.append(TestCase("Rajawali", "Tangerang"))
    test_cases.append(TestCase("RangkasBitung", "Ancol"))
    test_cases.append(TestCase("Citayam", "Duri"))
    test_cases.append(TestCase("Bogor", "Tangerang"))
    test_cases.append(TestCase("JakartaKota", "Tangerang"))

    compare_astar_and_greedy(test_cases, undirected_graph, coordinates_data, graph_data)


if __name__ == "__main__":
    # main()
    check_different_cost()
