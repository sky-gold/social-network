.PHONY: build_api-gateway test_api-gateway build_user-service test_user-service

VENV_DIR = .venv
TEST_ENV = TESTING=1 PYTHONPATH=.

build_api-gateway:
	@echo "Building API Gateway..."
	cd api-gateway && \
	python3 -m venv $(VENV_DIR) && \
	. $(VENV_DIR)/bin/activate && \
	pip install -r requirements.txt

test_api-gateway:
	@echo "Testing API Gateway..."
	cd api-gateway && \
	. $(VENV_DIR)/bin/activate && \
	PYTHONPATH=src pytest tests/ -v -p no:warnings

build_user-service:
	@echo "Building User Service..."
	cd user-service && \
	python3 -m venv $(VENV_DIR) && \
	. $(VENV_DIR)/bin/activate && \
	pip install -r requirements.txt

test_user-service:
	@echo "Testing User Service..."
	cd user-service && \
	. $(VENV_DIR)/bin/activate && \
	$(TEST_ENV) pytest tests/ -v -p no:warnings --cov=app --cov-report=term-missing