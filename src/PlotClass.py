from src import DiGraph
from src import GraphAlgo
from Node import Node
import matplotlib as plt
import NumPy as np

class PlotClass:
    #needed for random pos
    maxX : float
    minX : float
    maxY : float
    minY : float

    def __init__(self):
        gAlgo :GraphAlgo = GraphAlgo()
        gAlgo.load_from_json("../data/A5")
        g: DiGraph = gAlgo.get_graph()

        for node in g.get_all_v():


