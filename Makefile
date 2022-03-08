.PHONY: help prepare html serve clean executed_notebooks
.DEFAULT_GOAL := help

notebook_sources := $(wildcard content/*/notebook.md)
notebook_ipynbs := $(patsubst %notebook.md,%index.ipynb,$(notebook_sources))
notebook_mds := $(patsubst %.ipynb,%.md,$(notebook_ipynbs))

# Add help text after each target name starting with '\#\#'
help:   ## Display this message
help:
	@echo -e "Usage: make TARGET\n"
	@echo -e "where TARGET is one of\n"
	@grep -h "^\(\S*\):[ ]*##\(.*\)" $(MAKEFILE_LIST) | awk -F ':\\s*##\\s*' '{printf "%-19s %s\n", $$1, $$2}'

prepare:
	git submodule update --init

html: ## Build site in `./public`
html: prepare executed_notebooks
	hugo

serve: ## Serve site, typically on http://localhost:1313
serve: prepare executed_notebooks
	@hugo --printI18nWarnings server

clean: ## Remove built files
clean:
	rm -rf public

%/index.ipynb:%/notebook.md
	jupytext $< -o $@

%/index.md:%/index.ipynb
	jupyter nbconvert --execute $< --to markdown --TemplateExporter.extra_template_basedirs=. --template=mdoutput_template

$(notebook_mds): $(notebook_ipynbs)

executed_notebooks: ## Execute all outdated notebooks
executed_notebooks: $(notebook_mds)
