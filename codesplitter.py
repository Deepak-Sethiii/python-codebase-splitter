print("SCRIPT")
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
def split_app_code():
    file_path = os.path.join("requests", "app.py")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code_text = file.read()
        print(f"successfully read {file_path} ({len(code_text)} characters)")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return
    separators = [
        "\nclass",
        "n\def",
        "\n\n",
        " ",
        ""
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=separators,
        keep_separator=True,
        is_separator_regex=False
    )
    chunks = splitter.create_documents([code_text])
    print(f"Split into {len(chunks)} chunks.\n")
    for i, chunk in enumerate(chunks):
        print(f"[CHUNK {i+1}] Length: {len(chunk.page_content)}")
        print("-" * 30)
        print(chunk.page_content)
        print("-" * 30)
        print("\n")
    print("=" * 60)

if __name__ == "__main__":
    split_app_code()
