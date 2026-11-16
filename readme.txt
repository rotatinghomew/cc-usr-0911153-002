工业机器人具身数据采集编排中心

数据集封存：Application.publish_dataset(dataset_id, session_ids) 从已登记采集
会话建立可重放的封存数据集，Application.dataset_manifest(dataset_id) 读取当时
的会话版本、质量隔离标记、工况单元与覆盖摘要。重复封存相同证据保持幂等；
不同证据不得覆盖同一个已发布的数据集。清单与采集记录共用运行时数据库。

质量判定 / 覆盖 / 准入一致性：
- synchronisation.timeline.alignment 是唯一权威的对齐隔离依据
  （对齐质量 < 0.55 或 |clock_skew_ms| > 150ms 即隔离），quarantine_reasons
  保留可供审计的隔离理由。
- 被隔离的会话作为审计证据保留，但 coverage_lattice 只统计未隔离会话，
  隔离证据不能占据任何可用工况单元；coverage_gap_report 逐单元列出可用会话、
  隔离会话与仍然开放的覆盖缺口，覆盖多机型、重复片段与部分恢复。
- orchestration.session_lifecycle 的 decide/advance_for_outcome 以对齐隔离为准：
  隔离会话进入 quarantined 且不能进入 curated/sealed；纠正后对齐恢复的会话可
  从 quarantined 释放回 curated。合成评分只驱动 review 证据，不再把会话直接
  推入 superseded。
- Application.reevaluate(record_ids) 在纠正片段后重评受影响会话并重算覆盖缺口，
  而不是简单改低总分；Application.coverage_report() 给出当前可用覆盖与隔离证据。
- 封存清单的 coverage/usable_item_count 与交付门禁指向同一批有效证据；仍处于
  planned/capturing 等未准入状态的会话不能封存。
- 已封存数据集保留封存当时采用的 quality_basis 与覆盖快照且不可变；
  Application.review_dataset(dataset_id) 生成可区分的复核意见（含 recovered /
  regressed / still-quarantined / still-usable 会话级结论），不改动封存清单。

运行验收：
python3 -m robot_corpus run --fixture fixtures/acceptance.json --database /tmp/robot_corpus.sqlite3 --output /tmp/robot_corpus-output

核验：
python3 -m robot_corpus verify --database /tmp/robot_corpus.sqlite3 --output /tmp/robot_corpus-output

覆盖与复核（同一数据库）：
python3 -m robot_corpus coverage --database /tmp/robot_corpus.sqlite3
python3 -m robot_corpus reevaluate --database /tmp/robot_corpus.sqlite3 [--session <id> ...]
python3 -m robot_corpus review --dataset <dataset_id> --database /tmp/robot_corpus.sqlite3

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.synchronization.test_quality_gates -v

构建检查：
python3 -m compileall -q robot_corpus tests
