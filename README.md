# integreat-chatbot


We use [haystack](https://docs.haystack.deepset.ai/) to search the documents


## Script 1: Split and format json response
Currently there is a script, which splits the response from e.g. `https://cms.integreat-app.de/api/muenchen/de/pages` into different documents. It also removes the HTML tags. These generated files can easily be converted and stored by haystack document.
To run this script use `python3 parse-files.py`


## Script 2: Run first prototyp
To run the first prototype you need to download a LLM. There are different available on [huggingface](https://huggingface.co/). For example [google-flan-t5-xl](https://huggingface.co/google/flan-t5-xl)

Before running the script some dependencies need to be installed, therefore create a virtual environment and activate it. The script will download the llm and it will be saved in `home/.cache/huggingface`, so expect the first run of the script to be significantly slower than the following ones.

`python3 -m venv .venv
source .venv/bin/activate`

then install

`
pip install --upgrade pip
pip install pip install farm-haystack==1.17.2
`
