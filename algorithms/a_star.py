import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo
GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça até sua posição final.
        É admissível porque cada movimento desloca uma única peça em uma casa."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            gr, gc = GOAL_POSITIONS[tile]
            total += abs(r - gr) + abs(c - gc)
        return total

    def search(self, initial: State) -> SearchResult:
        if not initial.is_solvable:
            return SearchResult(solution=None)

        tie = count()  # desempate estável entre nós com mesmo f
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: 0}
        expanded = 0
        generated = 1
        max_frontier = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)
            # Ignora entradas obsoletas (já encontramos caminho melhor para este estado)
            if node.cost > best_g.get(node.tiles, float("inf")):
                continue
            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=expanded,
                    nodes_generated=generated,
                    max_frontier_size=max_frontier,
                    depth=node.cost,
                )

            expanded += 1
            for child in node.neighbors():
                generated += 1
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, next(tie), child))
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=expanded,
            nodes_generated=generated,
            max_frontier_size=max_frontier,
        )
