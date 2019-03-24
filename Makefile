artifacts = build dist lamby.spec

lamby: $(artifacts)
	pipenv run pyinstaller --onefile lamby/lamby.py --name lamby --clean

.PHONY: clean
clean:
	-rm -rf $(artifacts)

$(artifacts): lamby/lamby.py
