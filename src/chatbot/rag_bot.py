from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

VECTOR_DB_PATH = "data/vectorstore"

PROMPT_TEMPLATE = """
Tum ek HR policy assistant ho. Neeche diye gaye context ke basis par 
user ke sawal ka answer do. Agar context me answer nahi mila, to bolo 
"Mujhe is baare me policy document me information nahi mili."

Context:
{context}

Question: {question}

Answer:
"""

class HRPolicyRAGBot:
    def __init__(self):
        print("RAG chatbot load ho raha hai...")

        # Step 1: Embeddings model
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Step 2: Saved vector database load karo
        self.vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=self.embeddings,
        )

        # Step 3: Retriever banao
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # Step 4: Local Ollama LLM
        self.llm = OllamaLLM(model="llama3.2")

        # Step 5: Prompt template
        self.prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # Step 6: Modern LCEL chain banao (retriever -> prompt -> llm -> output)
        self.chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        print("RAG chatbot ready hai!")

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self, question):
        return self.chain.invoke(question)


# Quick test
if __name__ == "__main__":
    bot = HRPolicyRAGBot()

    test_questions = [
        "What is the leave policy?",
        "What is the notice period for a manager?",
        "How many days of work from home are allowed?",
    ]

    for q in test_questions:
        print(f"\nQ: {q}")
        answer = bot.ask(q)
        print(f"A: {answer}")