from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:
            return SearchResult(solution=None)

        stack = [initial]
        # Guarda a menor profundidade com que cada estado já foi alcançado,
        # para evitar ciclos sem perder caminhos mais rasos.
        best_depth = {initial.tiles: 0}
        expanded = 0
        generated = 1
        max_frontier = 1

        while stack:
            node = stack.pop()
            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=expanded,
                    nodes_generated=generated,
                    max_frontier_size=max_frontier,
                    depth=node.cost,
                )
            if node.cost >= self.depth_limit:
                continue

            expanded += 1
            # Empilha em ordem inversa para explorar UP, DOWN, LEFT, RIGHT nessa ordem
            for child in reversed(node.neighbors()):
                generated += 1
                known = best_depth.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                stack.append(child)
            max_frontier = max(max_frontier, len(stack))

        return SearchResult(
            solution=None,
            nodes_expanded=expanded,
            nodes_generated=generated,
            max_frontier_size=max_frontier,
        )
