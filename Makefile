SUMMARIZER := "led"

both:
	poetry run python unml/main.py \
		-f urls.txt \
		-v \
		--summarize \
		--ner \
		--summarizer ${SUMMARIZER}

summarize:
	poetry run python unml/main.py \
		-f urls.txt \
		-v \
		--summarize \
		--summarizer ${SUMMARIZER}


ner:
	poetry run python unml/main.py \
		-f urls.txt \
		-v \
		--ner
