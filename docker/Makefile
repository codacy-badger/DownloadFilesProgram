.PHONY: build run

REPO  ?= denden047/scraping

build:
	docker build -t $(REPO):latest .
	docker push $(REPO):latest