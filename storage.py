import os
import pickle
from collections import Counter


def save_graph(graph: dict, path: str = "data/graph.pkl") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(graph, f)

    nodes = graph["nodes"]
    edges = graph["edges"]
    edge_count = sum(len(v) for v in edges.values()) // 2
    print(f"  저장 완료: {path} | 노드 {len(nodes):,}개 | 엣지 {edge_count:,}개")


def load_graph(path: str = "data/graph.pkl") -> dict:
    with open(path, "rb") as f:
        return pickle.load(f)


def print_stats(graph: dict) -> None:
    nodes = graph["nodes"]
    edges = graph["edges"]

    total_nodes = len(nodes)
    edge_count = sum(len(v) for v in edges.values()) // 2
    degrees = [len(v) for v in edges.values()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0

    genre_counter: Counter = Counter()
    for book in nodes.values():
        genre_counter[book.genre or "기타"] += 1

    failed_count = 0
    if os.path.exists("failed_isbns.txt"):
        with open("failed_isbns.txt", encoding="utf-8") as f:
            failed_count = sum(1 for line in f if line.strip())

    print("\n===== 그래프 통계 =====")
    print(f"총 노드 수     : {total_nodes:,}")
    print(f"총 엣지 수     : {edge_count:,}")
    print(f"평균 degree    : {avg_degree:.2f}")
    print(f"수집 실패 ISBN : {failed_count:,}")
    print("\n장르별 노드 분포:")
    for genre, count in sorted(genre_counter.items()):
        bar = "█" * (count * 30 // max(genre_counter.values()))
        print(f"  KDC {genre:>3} | {count:>6,} | {bar}")
    print("=" * 22)
