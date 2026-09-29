from pathlib import Path
import re


class MarkdownKnowledgeLoader:

    def __init__(
        self,
        knowledge_dir: str,
    ):
        self.knowledge_dir = Path(
            knowledge_dir
        )

    def load_documents(self) -> list[dict]:
        documents = []

        for file_path in self.knowledge_dir.glob(
            "*.md"
        ):
            content = file_path.read_text(
                encoding="utf-8"
            )

            documents.append(
                {
                    "source": file_path.name,
                    "content": content,
                }
            )

        return documents

    def split_into_sections(
        self,
        content: str,
    ) -> list[dict]:

        pattern = re.compile(
            r"(?m)^(#{1,3})\s+(.+)$"
        )

        matches = list(
            pattern.finditer(content)
        )

        sections = []

        for index, match in enumerate(matches):

            start = match.start()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(content)

            section_content = content[
                start:end
            ].strip()

            sections.append(
                {
                    "heading": match.group(2).strip(),
                    "content": section_content,
                }
            )

        return sections

    def split_large_section(
        self,
        section: dict,
        max_characters: int = 4000,
    ) -> list[dict]:

        content = section["content"]

        if len(content) <= max_characters:
            return [section]

        paragraphs = content.split("\n\n")

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            if (
                len(current_chunk)
                + len(paragraph)
                + 2
                <= max_characters
            ):
                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:

                if current_chunk:
                    chunks.append(
                        {
                            "heading": section["heading"],
                            "content": current_chunk,
                        }
                    )

                current_chunk = paragraph

        if current_chunk:
            chunks.append(
                {
                    "heading": section["heading"],
                    "content": current_chunk,
                }
            )

        return chunks


if __name__ == "__main__":

    loader = MarkdownKnowledgeLoader(
        "data/knowledge"
    )

    documents = loader.load_documents()

    total_chunks = 0

    for document in documents:

        sections = loader.split_into_sections(
            document["content"]
        )

        document_chunks = []

        for section in sections:

            chunks = loader.split_large_section(
                section
            )

            document_chunks.extend(chunks)

        print(
            f"\nSource: {document['source']}"
        )

        print(
            f"Sections: {len(sections)}"
        )

        print(
            f"Chunks: {len(document_chunks)}"
        )

        for index, chunk in enumerate(
            document_chunks[:3],
            start=1,
        ):
            print(
                f"Chunk {index}: "
                f"{len(chunk['content'])} characters"
            )

        total_chunks += len(document_chunks)

    print(
        f"\nTotal chunks: {total_chunks}"
    )