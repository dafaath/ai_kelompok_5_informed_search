import json
import numpy as np
from os import error
from search import Graph, GraphProblem, UndirectedGraph, astar_search, best_first_graph_search, greedy_best_first_graph_search


class TestCase():
    initial: str
    goal: str
    astar_cost: float
    greedy_cost: float
    astar_path: list
    greedy_path: list
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

    def update_path(self, astar_path: list, greedy_path: list):
        self.astar_path = astar_path
        self.greedy_path = greedy_path


def open_file_data():
    # Opening data from json files
    with open("KRL_STATION_COORDINATE.json") as f:
        krl_station_coordinates_data = json.loads(f.read())
    with open("KRL_STATION_GRAPH.json") as f:
        krl_station_graph_data = json.loads(f.read())
    return krl_station_coordinates_data, krl_station_graph_data


def do_search(search_type: str, initial: str, goal: str, undirected_graph: Graph, coordinates_data, graph_data):
    krl_station_problem = GraphProblem(initial, goal, undirected_graph)

    # Validasi
    if(search_type == "astar"):
        path = astar_search(krl_station_problem).path()
    elif(search_type == "greedy"):
        path = greedy_best_first_graph_search(krl_station_problem, krl_station_problem.h).path()
    else:
        raise TypeError("search_type hanya bisa astar dan greedy")

    cost = 0
    paths = []
    for i, node in enumerate(path, 1):
        paths.append(node.state)
        if(i == 1):
            pass
        else:  # Mengambil graph data dari file dan menghitung cost setiap state yang dilewati
            cost += graph_data[node_state_before][node.state]
        node_state_before = node.state  # Menyimpan node yang sebelumnya (i-1)
    return cost, path


def compare_astar_and_greedy(test_cases: list, undirected_graph: Graph, coordinates_data, graph_data):
    for i, test in enumerate(test_cases, 1):
        print(f"Melakukan perbandingan dari {test.initial} ke {test.goal} : ", end="")
        astar_cost, astar_path = do_search("astar", test.initial, test.goal,
                                           undirected_graph, coordinates_data, graph_data)
        greedy_cost, greedy_path = do_search("greedy", test.initial, test.goal,
                                             undirected_graph, coordinates_data, graph_data)
        test.update_cost(astar_cost, greedy_cost)
        test.update_path(astar_path, greedy_path)
        if astar_cost != greedy_cost:
            print(f"Ada perbedaan di jalur {test.initial} menuju {test.goal}")
            print(f"A* search {test.astar_cost}")
            for i, path, in enumerate(test.astar_path, 1):
                print(i, path.state)
            print(f"Greedy Search {test.greedy_cost}")
            for i, path in enumerate(test.greedy_path, 1):
                print(i, path.state)
        else:
            print("Tidak ada perbedaan")


def check_different_cost():
    """Mencari apakah ada perbedaan dari hasil greedy search dan astar search untuk setiap stasiun yang ada"""
    coordinates_data, graph_data = open_file_data()
    undirected_graph = UndirectedGraph(graph_data)
    # Menambahkan test case untuk semua kemungkinan stasiun
    undirected_graph.locations = coordinates_data
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
                               undirected_graph, coordinates_data, graph_data)
        greedy_cost = do_search("greedy", test.initial, test.goal,
                                undirected_graph, coordinates_data, graph_data)
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
    undirected_graph.locations = coordinates_data    # Initialize train path to test
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


def crate_test_case_data():
    coordinates_data, graph_data = open_file_data()
    undirected_graph = UndirectedGraph(graph_data)
    undirected_graph.locations = coordinates_data

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

    test_cases_json = []
    for test in test_cases:
        x_initial = coordinates_data[test.initial][0],
        y_initial = coordinates_data[test.initial][1],
        x_goal = coordinates_data[test.goal][0],
        y_goal = coordinates_data[test.goal][1],
        a = np.array((x_initial, y_initial))
        b = np.array((x_goal, y_goal))
        test_cases_json.append({
            "initial": test.initial,
            "goal": test.goal,
            "x_initial": x_initial[0],
            "y_initial": y_initial[0],
            "x_goal": x_goal[0],
            "y_goal": y_goal[0],
            "eucledian_cost": np.linalg.norm(a - b),
        })
    print(test_cases_json)


if __name__ == "__main__":
    main()
    # check_different_cost()
    # crate_test_case_data()
