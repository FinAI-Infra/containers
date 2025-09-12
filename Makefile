.PHONY: all fmt

all: fmt

fmt:
	@for file in $$(find . -maxdepth 2 -mindepth 2 -name requirements.txt); do \
		echo "Sorting: $$file"; \
		sort -o "$$file" "$$file"; \
	done
	@echo "All requirements.txt files in subdirectories have been sorted alphabetically."