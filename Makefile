LANG=en_US.utf-8

export LANG

Pipfile.lock: Pipfile
	docker-compose run --rm --name helix_fhir_profiles dev pipenv lock --dev

.PHONY:devdocker
devdocker: ## Builds the docker for dev
	docker-compose build

.PHONY:init
init: devdocker up setup-pre-commit  ## Initializes the local developer environment

.PHONY: up
up: Pipfile.lock
	docker-compose up --build -d --remove-orphans

.PHONY: down
down:
	docker-compose down

.PHONY:clean-pre-commit
clean-pre-commit: ## removes pre-commit hook
	rm -f .git/hooks/pre-commit

.PHONY:setup-pre-commit
setup-pre-commit: Pipfile.lock
	cp ./pre-commit-hook ./.git/hooks/pre-commit

.PHONY:run-pre-commit
run-pre-commit: setup-pre-commit
	./.git/hooks/pre-commit

.PHONY:update
update: down Pipfile.lock setup-pre-commit  ## Updates all the packages using Pipfile
	docker-compose run --rm --name helix_fhir_profiles dev pipenv sync && \
	make devdocker && \
	make pipenv-setup

.PHONY:tests
tests: up
	docker-compose run --rm --name helix_fhir_profiles dev pytest tests

.PHONY:shell
shell:devdocker ## Brings up the bash shell in dev docker
	docker-compose run --rm --name helix_fhir_profiles dev /bin/bash

.PHONY:build
build:
	docker-compose run --rm --name helix_fhir_profiles dev rm -rf dist/
	docker-compose run --rm --name helix_fhir_profiles dev python3 setup.py sdist bdist_wheel

.PHONY:testpackage
testpackage:build
	docker-compose run --rm --name helix_fhir_profiles dev python3 -m twine upload -u __token__ --repository testpypi dist/*
# password can be set in TWINE_PASSWORD. https://twine.readthedocs.io/en/latest/

.PHONY:package
package:build
	docker-compose run --rm --name helix_fhir_profiles dev python3 -m twine upload -u __token__ --repository pypi dist/*
# password can be set in TWINE_PASSWORD. https://twine.readthedocs.io/en/latest/ (note this is the token not your password)

.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help.
	# from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY:pipenv-setup
pipenv-setup:devdocker ## Brings up the bash shell in dev docker
	docker-compose run --rm --name mockserver_client dev pipenv-setup sync --pipfile