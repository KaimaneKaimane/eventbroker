clean-pycache:
	find . -type d -name __pycache__ -exec rm -r {} \+

base: clean-pycache
	docker build . -f ./docker/Dockerfile -t eventbroker/base:latest --cache-from eventbroker/base:latest --build-arg PROJECT=eventbroker
