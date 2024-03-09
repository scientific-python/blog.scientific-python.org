.PHONY: help prepare teams teams-clean html serve clean
.DEFAULT_GOAL := help

# Add help text after each target name starting with '\#\#'
help:   ## show this help
	@echo -e "Help for this makefile\n"
	@echo "Possible commands are:"
	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\(.*\):.*##\(.*\)/    \1: \2/'

prepare:
	git submodule update --init --recursive
	pre-commit install || echo "Install 'pre-commit' in a Python environment with: 'pip install pre-commit'"
	hugo version || echo "Install Hugo from: https://gohugo.io"

TEAMS_DIR = content/about
TEAMS = blog-editor-in-chief blog-editors blog-reviewers
TEAMS_QUERY = python themes/scientific-python-hugo-theme/tools/team_query.py

$(TEAMS_DIR)/%.toml:
	$(TEAMS_QUERY) --org scientific-python --team "$*"  >  $(TEAMS_DIR)/$*.toml

teams-clean:
	for team in $(TEAMS); do \
	  rm -f $(TEAMS_DIR)/$${team}.toml ;\
	done

teams: ## generates team gallery pages
teams: | teams-clean $(patsubst %,$(TEAMS_DIR)/%.toml,$(TEAMS))

html: ## Build site in `./public`
html: prepare
	hugo

serve: ## Serve site, typically on http://localhost:1313
serve: prepare
	@hugo --printI18nWarnings server

clean: ## Remove built files
clean:
	rm -rf public
