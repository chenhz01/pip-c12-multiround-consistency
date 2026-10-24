# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L46 — 矛盾登记册（多轮一致）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l46_register(entries):
    """entries: [{"id","statement","supersedes","reason","ts"}]。
    只登记、不删除：被推翻的话要留下推翻理由，否则下次还会复活。"""
    active = {}
    retired = []
    for e in entries:
        if e.get("supersedes"):
            old = e["supersedes"]
            if old in active:
                retired.append({"id": old, "statement": active[old]["statement"],
                                "by": e["id"], "reason": e.get("reason", ""), "ts": e.get("ts")})
                active.pop(old)
        active[e["id"]] = e
    conflicts = []
    ids = list(active)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = active[ids[i]], active[ids[j]]
            if set(a.get("negates", [])) & set(b.get("negates", [])):
                continue
            if a.get("topic") and a.get("topic") == b.get("topic") and a.get("stance") != b.get("stance"):
                conflicts.append((a["id"], b["id"]))
    return {"active": len(active), "retired": retired,
            "unresolved_conflicts": conflicts,
            "verdict": "clean" if not conflicts else "has-unresolved",
            "advice": "未解冲突必须显式裁决，不能靠「后来者自然覆盖」" if conflicts else "档案一致"}


def l46_demo():
    entries = [
        {"id": "B1", "topic": "push方式", "stance": "HTTPS", "statement": "用 HTTPS 推"},
        {"id": "B2", "topic": "push方式", "stance": "SSH", "statement": "改 SSH",
         "supersedes": "B1", "reason": "本机 443 不通", "ts": "2026-10-24"},
    ]
    r = l46_register(entries)
    print("  在册 %d 条，推翻 %d 条 -> %s" % (r["active"], len(r["retired"]), r["verdict"]))
    print("  推翻记录:", [(x["id"], x["by"], x["reason"]) for x in r["retired"]])


def l46_selftest():
    r = l46_register([{"id": "B1", "topic": "t", "stance": "a", "statement": "s1"},
                      {"id": "B2", "topic": "t", "stance": "b", "statement": "s2"}])
    assert r["verdict"] == "has-unresolved"
    r2 = l46_register([{"id": "B1", "topic": "t", "stance": "a", "statement": "s1"},
                       {"id": "B2", "topic": "t", "stance": "b", "statement": "s2", "supersedes": "B1"}])
    assert r2["verdict"] == "clean" and len(r2["retired"]) == 1
    return True


if __name__ == "__main__":
    l46_demo()
