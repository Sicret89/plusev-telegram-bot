# Makefile for PlusEV Telegram Bot

PROJECT_NAME=plusev-telegram-bot
IMAGE_NAME=$(PROJECT_NAME):latest

# Default environment file
ENV_FILE=.env

.PHONY: help build run test lint clean

help:
	@echo "Usage:"
	@echo "  make build     - Build the Docker image"
	@echo "  make run       - Run the container (ensure TELEGRAM_TOKEN is set)"
	@echo "  make test      - Run pytest inside Docker"
	@echo "  make lint      - Run flake8 linter"
	@echo "  make clean     - Remove Docker image"

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm --env-file $(ENV_FILE) $(IMAGE_NAME)

test:
	pytest

lint:
	flake8 .

clean:
	docker rmi $(IMAGE_NAME) || true
