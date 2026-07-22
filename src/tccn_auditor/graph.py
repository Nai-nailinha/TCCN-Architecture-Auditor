from .models import Document
from .normalize import normalize_name


def find_cycles(
    documents: list[Document],
    document_index: dict[str, Document],
) -> list[list[str]]:
    graph: dict[str, set[str]] = {}
    titles: dict[str, str] = {}

    for document in documents:
        document_key = normalize_name(document.title)
        titles[document_key] = document.title
        graph.setdefault(document_key, set())

        for reference in document.references:
            reference_key = normalize_name(reference)
            referenced_document = document_index.get(reference_key)

            if referenced_document is None:
                continue

            target_key = normalize_name(referenced_document.title)
            graph[document_key].add(target_key)

    cycles: list[list[str]] = []
    visited: set[str] = set()
    active: set[str] = set()
    path: list[str] = []

    def visit(node: str) -> None:
        if node in active:
            cycle_start = path.index(node)
            cycle_keys = path[cycle_start:] + [node]
            cycle_titles = [
                titles.get(key, key)
                for key in cycle_keys
            ]

            if cycle_titles not in cycles:
                cycles.append(cycle_titles)

            return

        if node in visited:
            return

        visited.add(node)
        active.add(node)
        path.append(node)

        for neighbor in graph.get(node, set()):
            visit(neighbor)

        path.pop()
        active.remove(node)

    for node in graph:
        visit(node)

    return cycles