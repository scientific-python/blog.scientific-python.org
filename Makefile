.PHONY: help prepare html serve clean
.DEFAULT_GOAL := help

# Add help text after each target name starting with '\#\#'
help:   ## show this help
	@echo -e "Help for this makefile\n"
	@echo "Possible commands are:"
	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\(.*\):.*##\(.*\)/    \1: \2/'

prepare:
	git submodule update --init

html: ## Build site in `./public`
html: prepare
	hugo

serve: ## Serve site, typically on http://localhost:1313
serve: prepare
	@hugo --i18n-warnings server

clean: ## Remove built files
clean:
	rm -rf public
