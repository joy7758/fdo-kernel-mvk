PYTHON ?= python3
RUNTIME_DIR ?= examples/runtime

.PHONY: run replay tamper smoke

run:
	$(PYTHON) -m kernel.cli run --runtime-dir $(RUNTIME_DIR)

replay:
	$(PYTHON) -m kernel.cli replay --runtime-dir $(RUNTIME_DIR)

tamper:
	$(PYTHON) -m kernel.cli tamper --runtime-dir $(RUNTIME_DIR)

smoke:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'
