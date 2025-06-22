

.PHONY: test
test:
	@echo "Running 'make test'"
	rm -rf log.txt
	$(MAKE) test-implementation
	$(MAKE) test-log


.PHONY: test-implementation
test-implementation: \
    test-python \
    test-dummy-1 \
    test-dummy-2 \
    test-dummy-3 \


.PHONY: test-dummy-1
test-dummy-1:
	python -m mock_app.logger '[make:test-dummy-1] start'
	sleep 1
	python -m mock_app.logger '[make:test-dummy-1] stop'


.PHONY: test-dummy-2
test-dummy-2:
	python -m mock_app.logger '[make:test-dummy-2] start'
	sleep 1
	python -m mock_app.logger '[make:test-dummy-2] stop'


.PHONY: test-dummy-3
test-dummy-3:
	python -m mock_app.logger '[make:test-dummy-3] start'
	sleep 1
	python -m mock_app.logger '[make:test-dummy-3] stop'


.PHONY: test-python
test-python:
	python -m mock_app.logger '[make:test-python] start'
	pytest --numprocesses=8 mock_app
	python -m mock_app.logger '[make:test-python] stop'


.PHONY: test-log
test-log:
	@echo '=== log output ==='
	cat log.txt
	@echo '=================='
	@echo 'Testing max 3 running tasks (make -j3 in tox.ini)'
	grep '\[logger\] 3 running tasks' log.txt > /dev/null
	grep -v '\[logger\] 4 running tasks' log.txt > /dev/null
