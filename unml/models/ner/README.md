# Named Entity Recognition models

- RoBERTa ([`RoBERTa.py`](unml/models/ner/RoBERTa.py))

## FLERT

### On `ontonotes` dataset

Predicts 18 tags:

|    **Tag**    |     **Meaning**      |
| :-----------: | :------------------: |
|    `NORP`     |     affiliation      |
|     `FAC`     |    building name     |
|  `CARDINAL`   |    cardinal value    |
|    `DATE`     |      date value      |
|    `EVENT`    |      event name      |
|     `GPE`     | geo-political entity |
|  `LANGUAGE`   |    language name     |
|     `LAW`     |       law name       |
|     `LOC`     |    location name     |
|    `MONEY`    |      money name      |
| `WORK_OF_ART` | name of work of art  |
|   `ORDINAL`   |    ordinal value     |
|     `ORG`     |  organization name   |
|   `PERCENT`   |    percent value     |
|   `PERSON`    |     person name      |
|   `PRODUCT`   |     product name     |
|  `QUANTITY`   |    quantity value    |
|    `TIME`     |      time value      |

(Table from [`Flair` documentation](https://huggingface.co/flair/ner-english-ontonotes-fast))
