#!/usr/bin/env python3
"""Analyze service call edges for cycles, blast radius, and single points."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def analyze(edges, changed=None):
    graph, inbound = defaultdict(set), defaultdict(set)
    for edge in edges:
        source, target = edge["source"], edge["target"]
        graph[source].add(target); inbound[target].add(source)
        graph.setdefault(target, set())
    cycles = []
    def visit(node, path):
        if node in path:
            cycle = path[path.index(node):] + [node]
            if cycle not in cycles: cycles.append(cycle)
            return
        for child in graph[node]: visit(child, path + [node])
    for node in graph: visit(node, [])
    affected = set()
    def descend(node):
        for child in graph[node]:
            if child not in affected: affected.add(child); descend(child)
    if changed: descend(changed)
    single_points = sorted(node for node, callers in inbound.items() if len(callers) >= 2)
    return {"services": sorted(graph), "cycles": cycles, "blast_radius": sorted(affected), "shared_dependencies": single_points}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edges"); parser.add_argument("--changed")
    args = parser.parse_args()
    print(json.dumps(analyze(json.loads(Path(args.edges).read_text()), args.changed), indent=2))


if __name__ == "__main__":
    main()
