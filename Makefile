PYTHON_PACKAGE_NAME := yaml-pipe
TEST_PYPI := -r testpypi
TEST_PYPI_INDEX_URL := --index-url https://test.pypi.org/simple/

.PHONY: develop-install
develop-install:
	poetry install

.PHONY: rebuild-dist
rebuild-dist:
	${MAKE} clean
	poetry build

.PHONY: pypi-upload
pypi-upload:
	${MAKE} rebuild-dist
	poetry publish ${TEST_PYPI}

.PHONY: pypi-install
pypi-install:
	${MAKE} clean
	poetry run python -m pip install \
		--no-cache-dir \
		--upgrade \
		${TEST_PYPI_INDEX_URL} \
		${PYTHON_PACKAGE_NAME}

.PHONY: clean
clean:
	-rm -rf dist
	-poetry run python -m pip uninstall -y ${PYTHON_PACKAGE_NAME}
	-poetry run python -m pip cache purge
