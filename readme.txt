工业机器人具身数据采集编排中心

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
