# Machine Learning pipeline for United Nations Digital Library 🇺🇳

![Style](https://img.shields.io/badge/style-black-black) ![Packages](https://img.shields.io/badge/package%20manager-poetry-blue) ![Linter](https://img.shields.io/badge/linter-ruff-orange) ![Version](https://img.shields.io/github/v/release/ClementSicard/un-unbis-thesaurus-scraper?display_name=tag&label=version&logo=python&logoColor=white)

- [Machine Learning pipeline for United Nations Digital Library 🇺🇳](#machine-learning-pipeline-for-united-nations-digital-library-)
  - [Pipeline description](#pipeline-description)
  - [Summarization models](#summarization-models)
  - [NER models](#ner-models)
  - [Usage](#usage)
  - [Useful links](#useful-links)
    - [Summarizing](#summarizing)

## Pipeline description

**TODO**: Add pipeline diagram

## Summarization models

|      Model       |                              File                               |                    Paper                     |     Authors     | Year | HuggingFace 🤗 model |
| :--------------: | :-------------------------------------------------------------: | :------------------------------------------: | :-------------: | :--: | :------------------: |
| DistillBART-CNN  |  [`DistillBARTCNN.py`](unml/models/summarize/DistilBARTCNN.py)  | [Link](https://arxiv.org/pdf/2010.13002.pdf) | Shleifer et al. | 2020 |       **TODO**       |
| DistillBART-XSUM | [`DistillBARTXSUM.py`](unml/models/summarize/DistilBARTXSUM.py) | [Link](https://arxiv.org/pdf/2010.13002.pdf) | Shleifer et al. | 2020 |       **TODO**       |
| DistilPegasusCNN | [`DistilPegasusCNN.py`](unml/models/summarize/DistilPegasusCNN) | [Link](https://arxiv.org/pdf/2010.13002.pdf) | Shleifer et al. | 2020 |       **TODO**       |
|    Longformer    |            [`LED.py`](unml/models/summarize/LED.py)             |   [Link](https://arxiv.org/pdf/2004.05150)   | Beltagy et al.  | 2020 |       **TODO**       |
|      LongT5      |         [`LongT5.py`](unml/models/summarize/LongT5.py)          |   [Link](https://arxiv.org/pdf/2112.07916)   |   Guo et al.    | 2022 |       **TODO**       |

## NER models

|  Model   |                    File                    |                    Paper                     |   Authors    | Year | HuggingFace 🤗 model |
| :------: | :----------------------------------------: | :------------------------------------------: | :----------: | :--: | :------------------: |
| RoBERTa  | [`RoBERTa.py`](unml/models/ner/RoBERTa.py) | [Link](https://arxiv.org/pdf/1907.11692.pdf) |  Liu et al.  | 2019 |       **TODO**       |
|  FLERT   |   [`FLERT.py`](unml/models/ner/FLERT.py)   | [Link](https://arxiv.org/pdf/2011.06993.pdf) | Akbik et al. | 2020 |       **TODO**       |
| spaCyNER |   [`spaCy.py`](unml/models/ner/spaCy.py)   |                      -                       |    spaCy     | 2023 |       **TODO**       |

## Usage

## Useful links

### Summarizing
