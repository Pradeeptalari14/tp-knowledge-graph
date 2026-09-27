#!/usr/bin/env python3
"""
NetworkX Graph Construction & Relations Mapping Engine
"""
import networkx as nx
import json
from typing import List, Dict, Any

def build_knowledge_graph(entity_list: List[Dict[str, Any]]) -> nx.DiGraph:
    G = nx.DiGraph()
    for ent in entity_list:
        G.add_node(ent["text"], label=ent["label"], score=ent["score"])
        
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            n1, n2 = nodes[i], nodes[j]
            l1 = G.nodes[n1]["label"]
            l2 = G.nodes[n2]["label"]
            
            if l1 == "SERVICE" and l2 == "DATABASE":
                G.add_edge(n1, n2, relation="CONNECTS_TO")
            elif l1 == "SERVICE" and l2 == "CONFIG":
                G.add_edge(n1, n2, relation="USES_CONFIG")
            elif l1 == "OUTAGE" and l2 == "SERVICE":
                G.add_edge(n1, n2, relation="IMPACTS")
            elif l1 == "SERVICE" and l2 == "DEPENDENCY":
                G.add_edge(n1, n2, relation="DEPENDS_ON")
    return G

if __name__ == "__main__":
    test_entities = [
        {"text": "auth-service", "label": "SERVICE", "score": 0.98},
        {"text": "postgres-db", "label": "DATABASE", "score": 0.99},
        {"text": "redis-cache", "label": "DATABASE", "score": 0.94},
        {"text": "connection-pool-exhaustion", "label": "OUTAGE", "score": 0.92}
    ]
    graph = build_knowledge_graph(test_entities)
    print(f"Graph nodes: {list(graph.nodes(data=True))}")
    print(f"Graph edges: {list(graph.edges(data=True))}")
