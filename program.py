import zipfile
import os

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever, PromptNode, PromptTemplate
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.pipelines import Pipeline
from haystack.utils import convert_files_to_docs, print_answers

#import logging
#logging.basicConfig(format="%(levelname)s - %(name)s - %(message)s", level=logging.WARNING)
#logging.getLogger("haystack").setLevel(logging.INFO)

# ChatGPT answers on wrong document for a question: "Sorry but the given Text does not contain any information about xy". It would be really nice if the LLM we choose would also be capable of this

document_store = InMemoryDocumentStore(use_bm25=True)
doc_dir = "test-data/munchen-de"

all_docs = convert_files_to_docs(dir_path=doc_dir)

files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

retriever = BM25Retriever(document_store=document_store, top_k=1)

lfqa_prompt = PromptTemplate(
    name="lfqa",
    prompt_text="""Stellen Sie aus dem folgenden Text eine umfassende Antwort auf die gegebene Frage zusammen. Nutzen Sie nur Informationen aus dem angegebenen Text. Geben Sie eine klare und prägnante Antwort, die die wichtigsten Punkte und Informationen des Textes zusammenfasst. Ihre Antwort sollte in Ihren eigenen Worten erfolgen. Frage: {query} \n\n Zugehöriger Text: {join(documents)} \n\n Antwort:""",
)

print("Download model")
prompt_node = PromptNode(model_name_or_path="google/flan-t5-xl", default_prompt_template=lfqa_prompt)
print("Download finished")

pipe = Pipeline()
pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
pipe.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])

output = pipe.run(query="Welche Sehenswürdigkeiten hat München?")

print(output['results'][0])


