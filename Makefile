DEFAULT_URL := "https://digitallibrary.un.org/record/515307/files/E_CN.6_2004_NGO_4-EN.pdf"

test:
	poetry run python unml/main.py -u $(DEFAULT_URL) -v
