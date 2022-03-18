.PHONY: all test clean

SHELL := $(shell which bash)
PROJECT := crawler

include .env.dev
export

clean:
	find . -name '*.py[co]' -delete
	find . -name '*.skp' -delete
	find . -name '.coverage*' -delete
	rm -rf build dist $(PROJECT).egg-info
	find . -path '*/__pycache__*' -delete
	find . -path '*/.pytest_cache*' -delete
	find . -path '*/cov.xml' -delete
	find . -path '*/.pymon' -delete
	rm -rf report
	rm -rf htmlcov

validate: clean
	flake8 app

rebuild: clean
	docker-compose down --remove
	docker system prune -f
	docker-compose up -d redis
	sleep 2
	docker-compose up -d --build crawler
	sleep 3
	docker-compose up -d --build flower nginx
	docker-compose exec crawler python cli/crawl.py
	sleep 5
	docker-compose logs -f crawler

test: clean
	poetry run coverage run -m pytest
	poetry run coverage report -m

%:
	@:
