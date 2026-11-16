工业机器人具身数据采集编排中心

数据集封存：Application.publish_dataset(dataset_id, session_ids) 从已登记采集
会话建立可重放的封存数据集，Application.dataset_manifest(dataset_id) 读取当时
的会话版本、质量隔离标记、工况单元与覆盖摘要。重复封存相同证据保持幂等；
不同证据不得覆盖同一个已发布的数据集。清单与采集记录共用运行时数据库。

运行验收：
python3 -m robot_corpus run --fixture fixtures/acceptance.json --database /tmp/robot_corpus.sqlite3 --output /tmp/robot_corpus-output

核验：
python3 -m robot_corpus verify --database /tmp/robot_corpus.sqlite3 --output /tmp/robot_corpus-output

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.synchronization.test_quality_gates -v

构建检查：
python3 -m compileall -q robot_corpus tests
