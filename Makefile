# Project tooling for the vyrn.ru Hugo site.
# All tools (hugo, prettier, lighthouse, pre-commit) are provided by mise:
#   mise install
# Then just use the targets below.

CHROME_PATH ?= /usr/bin/chromium-bin
URL_HOME   ?= https://vyrn.ru/
URL_POST   ?= https://vyrn.ru/basic-golang/
REPORTS    := reports
LHC        := mise x -- lighthouse

.PHONY: build serve fmt check measure clean

build:
	mise x -- hugo --gc --minify

serve:
	mise x -- hugo server -D

fmt:
	mise x -- prettier --write .

check:
	mise x -- prettier --check .
	mise x -- hugo --gc --minify

measure: $(REPORTS)
	CHROME_PATH=$(CHROME_PATH) $(LHC) "$(URL_HOME)" --quiet \
		--only-categories=performance,accessibility,best-practices,seo \
		--chrome-flags="--headless=new --no-sandbox" \
		--output=json --output-path=$(REPORTS)/home.json
	CHROME_PATH=$(CHROME_PATH) $(LHC) "$(URL_POST)" --quiet \
		--only-categories=performance,accessibility,best-practices,seo \
		--chrome-flags="--headless=new --no-sandbox" \
		--output=json --output-path=$(REPORTS)/post.json
	python3 scripts/lighthouse-report.py $(REPORTS)/home.json $(REPORTS)/post.json

$(REPORTS):
	mkdir -p $(REPORTS)

clean:
	rm -rf $(REPORTS) public resources
