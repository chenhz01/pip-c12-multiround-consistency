# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L45 — 多轮一致性（多轮一致）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l45_consistency(answers, min_shared=1):
    """多轮答案的要素一致性：两两 Jaccard，报告最小/均值。

    多个答案「看起来都对」不算一致；共享要素才算。
    """
    if len(answers) < 2:
        return {"pairs": 0, "verdict": "insufficient"}
    sets = [set(a) for a in answers]
    scores = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            inter = len(sets[i] & sets[j])
            union = len(sets[i] | sets[j]) or 1
            scores.append(inter / union)
    lo, hi = min(scores), max(scores)
    avg = sum(scores) / len(scores)
    verdict = "consistent" if lo >= 0.6 else ("core-stable" if lo >= 0.35 else "inconsistent")
    return {"pairs": len(scores), "min": round(lo, 3), "avg": round(avg, 3), "max": round(hi, 3),
            "verdict": verdict,
            "note": "最小对（%.2f）才是可信度下界，均值会掩盖分歧" % lo}


def l45_demo():
    a1 = ["离线", "零依赖", "可回滚"]
    a2 = ["离线", "零依赖", "可回滚", "带日志"]
    a3 = ["云端", "高并发"]
    print("  两轮 ->", l45_consistency([a1, a2]))
    print("  三轮 ->", l45_consistency([a1, a2, a3]))


def l45_selftest():
    r = l45_consistency([["a", "b"], ["a", "b"]])
    assert r["min"] == 1.0 and r["verdict"] == "consistent"
    r2 = l45_consistency([["a", "b", "c"], ["x", "y"]])
    assert r2["min"] == 0.0 and r2["verdict"] == "inconsistent"
    assert l45_consistency([["a"]])["verdict"] == "insufficient"
    return True


if __name__ == "__main__":
    l45_demo()
