# Rag Diary

### Purpose
This repository primarily serves as a practical demonstrator for applying Retrieval-Augmented Generation (RAG) to 
manipulate personal data. Furthermore, it serves as an invaluable tool for my ongoing research, providing a hands-on 
experience in effectively leveraging Language Model Learning (LLM) within an applied context.

'Rag Diary' is constructed as a self-reflection aid, enabling users to assess their past life events more profoundly. 
It serves to merge users' queries with language model generated responses, juxtaposing their questions against the data 
populated from their localized diary entries or vector database.

It is crucial to note that 'Rag Diary' is not designed to replicate therapist functions. Users are discouraged from 
relying on suggestions output by the Language Learning Model (LLM) regarding life choices. The responses provided by 
the LLM primarily focus on encouraging further self-analysis and facilitating metabolic activities such as controlled 
breathing, regular exercising, and meditation.  


### Installation

This project requires an openai api key and python `3.10+`

Clone the repo into a folder. 

`cd` into the repo create a new virtural environment
```bash
python -m venv ./venv
```
activate the virtural environment.
```bash 
. ./venv/bin/activate
```

for windows
```bash
./venv/scripts/Activate
```

Once in the python virtural environment install the dependencies.
```bash 
pip install .
```
This command will run the build from the `pyproject.toml` file.


### Running cli

After installation activate the venv you can run the python module
```bash
python -m rag_diary --help
```

This will show you a list of available command to use. The Repo is in development. These
commands are subject to change


#### Create new entry
```bash
python -m rag_diary new-entry "You diary input goes here. for now paste text into cli to update vector db"
```

#### Get llm response about diary entries
```bash
python -m rag_diary query-retriver-agent "What did I do on January 1st"
```