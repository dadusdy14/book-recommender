# book-recommender

자료구조 수업 협업 과제 — 도서 추천 시스템의 **BFS 후보 수집** 단계.

## 파이프라인 내 위치

```
[1. 데이터 수집] → graph.pkl
        ↓
[2. BFS 후보 수집] ← 이 저장소가 담당
        ↓
[3. 점수 계산 → Top-N]   ← 다음 단계
        ↓
[4. 평가]
```

## 파일 구성

| 파일 | 역할 |
|---|---|
| `bfs_search.py` | **메인 모듈.** 입력 도서로부터 BFS로 후보 수집 |
| `storage.py` | `load_graph()` — pickle 그래프 로드 |
| `models.py` | `BookNode` 데이터클래스 (pickle 호환용) |
| `data/graph.pkl` | 정보나루 co-loan 그래프 (4,461 노드 / 25,918 엣지) |

## 의존성

표준 라이브러리만 사용 (추가 설치 불필요).

## 사용법

### 1) Python에서 함수로 호출

```python
from bfs_search import bfs_candidates
from storage import load_graph

graph = load_graph("data/graph.pkl")

# 시드 ISBN(들)을 입력하면 BFS 후보 리스트가 반환됨
candidates = bfs_candidates(
    graph,
    seed_isbns=["9791161571188"],  # 여러 권 입력 가능
    max_depth=2,                    # 1=직접 이웃, 2=이웃의 이웃까지
)

for c in candidates:
    print(c.isbn, c.depth, c.total_weight, c.paths_count, c.book.title)
```

### 2) CLI 데모 (단독 실행)

```
python bfs_search.py 9791161571188
```

## 다음 단계 담당자에게 — 출력 데이터 명세

`bfs_candidates()`가 반환하는 `list[Candidate]`. 정렬: depth ↑ → total_weight ↓.

| 필드 | 타입 | 설명 |
|---|---|---|
| `isbn` | str | 후보 도서 ISBN |
| `depth` | int | 시드로부터의 최단 거리 (1 또는 2) |
| `total_weight` | int | 시드들로부터 도달한 모든 경로의 co-loan 가중치 합 |
| `paths_count` | int | 시드들로부터 도달한 (최단 거리 기준) 경로 수 |
| `book` | BookNode | 메타 정보 (title, author, publisher, pub_year, genre, loan_count, keywords) |

이 리스트를 받아 점수를 매기고 Top-N을 추출하시면 됩니다.

## BFS 알고리즘 요약

- `collections.deque` 기반 표준 BFS (FIFO 큐)
- visited dict로 노드별 `{depth, weight, paths}` 추적
- 같은 노드를 더 깊은 경로로 재방문하면 무시 (BFS 최단경로 특성 보존)
- 같은 최단 거리에서 재도달 시 weight/paths 누적
- 시간 복잡도: **O(V + E)**
