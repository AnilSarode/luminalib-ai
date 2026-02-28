from infrastructure.ai.pdf_reader import extract_text_from_pdf
from infrastructure.ai.embedding_service import OllamaEmbeddingService

class SummarizeBookUseCase:
    def __init__(self, book_repository, llm_client):
        self.book_repository = book_repository
        self.llm_client = llm_client

    def execute(self, book_id: str, file_path: str):
        text = extract_text_from_pdf(file_path)
        summary = self.llm_client.summarize(text)

        embedding_service = OllamaEmbeddingService()
        embedding = embedding_service.generate(summary)

        updated =self.book_repository.update(
            book_id,
            {
                "summary": summary,
                "embedding": embedding
            }
        )
        print("✅ DB updated:", bool(updated))