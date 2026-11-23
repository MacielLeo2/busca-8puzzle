from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:
            return SearchResult(solution=None)

        if initial.is_goal:
            return SearchResult(solution=initial, nodes_generated=1, max_frontier_size=1, depth=0)

        frontier = deque([initial])
        reached = {initial.tiles}
        expanded = 0
        generated = 1
        max_frontier = 1

        while frontier:
            node = frontier.popleft()
            expanded += 1
            for child in node.neighbors():
                generated += 1
                if child.tiles in reached:
                    continue
                # Teste de objetivo na geração: a BFS já garante o caminho mais curto
                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=expanded,
                        nodes_generated=generated,
                        max_frontier_size=max_frontier,
                        depth=child.cost,
                    )
                reached.add(child.tiles)
                frontier.append(child)
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=expanded,
            nodes_generated=generated,
            max_frontier_size=max_frontier,
        )
