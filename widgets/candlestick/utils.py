






def intersect(r1: tuple[float, float], r2: tuple[float, float]) -> float:

    overlap = min(r1[1], r2[1]) - max(r1[0], r2[0])
    
    return overlap if overlap > 0 else 0.0