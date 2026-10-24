# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L47 — 信念修订账本（多轮一致）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l47_update(prior, likelihood, false_positive=0.1):
    """简化贝叶斯更新：后验 = 先验×似然 / (先验×似然 + (1-先验)×误报率)。

    账本要求三件事都留：先验、似然、用来更新的证据。
    """
    prior = min(max(prior, 1e-6), 1 - 1e-6)
    hit = prior * likelihood
    fp = (1 - prior) * false_positive
    post = hit / (hit + fp) if (hit + fp) else prior
    return {
        "prior": round(prior, 4),
        "likelihood": likelihood,
        "posterior": round(post, 4),
        "delta": round(post - prior, 4),
        "verdict": "strengthened" if post > prior else "weakened",
        "note": "似然高但误报率也高时，后验涨不动——这就是「看起来像证据」的陷阱",
    }


def l47_demo():
    for pr, lk, fp in ((0.5, 0.9, 0.1), (0.5, 0.9, 0.6), (0.9, 0.5, 0.1), (0.2, 0.95, 0.05)):
        r = l47_update(pr, lk, fp)
        print("  先验%.1f 似然%.2f 误报%.2f -> 后验%.3f (%+.3f) %s"
              % (pr, lk, fp, r["posterior"], r["delta"], r["verdict"]))


def l47_selftest():
    r = l47_update(0.5, 0.9, 0.1)
    assert r["posterior"] == round(0.45 / (0.45 + 0.05), 4)
    assert r["verdict"] == "strengthened"
    # 误报率拉高，后验明显涨不动
    assert l47_update(0.5, 0.9, 0.6)["posterior"] < l47_update(0.5, 0.9, 0.1)["posterior"]
    return True


if __name__ == "__main__":
    l47_demo()
