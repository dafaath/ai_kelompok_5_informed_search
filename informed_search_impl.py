import json

# Opening data from json files
with open("KRL_STATION_COORDINATE.json") as f:
    KRL_STATION_COORDINATES = json.loads(f.read())
with open("KRL_STATION_GRAPH.json") as f:
    KRL_STATION_GRAPH = json.loads(f.read())


def greedy_search():
    pass


def astar_search():
    pass


def main():
    print(KRL_STATION_COORDINATES)
    print(KRL_STATION_GRAPH)
    pass


if __name__ == "__main__":
    main()
