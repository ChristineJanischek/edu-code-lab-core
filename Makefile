.PHONY: build test lint release-check ci

build:
	./scripts/build.sh

test:
	./scripts/test.sh

lint:
	./scripts/lint.sh

release-check:
	./scripts/release_check.sh

ci: build test lint release-check
