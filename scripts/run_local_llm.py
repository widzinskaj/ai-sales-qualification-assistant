import requests
from pathlib import Path
import yaml


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def main():
    base_dir = Path(__file__).resolve().parent.parent

    prompt_path = base_dir / "prompts" / "qualification_prompt.md"
    email_path = base_dir / "queries" / "client_email_01.txt"
    criteria_path = base_dir / "config" / "decision_criteria_bess.yaml"
    rag_context_path = base_dir / "scripts" / "rag_context_example.txt"

    prompt_template = load_text(prompt_path)
    customer_email = load_text(email_path)
    rag_context = load_text(rag_context_path)

    with open(criteria_path, encoding="utf-8") as f:
        decision_criteria = yaml.safe_load(f)

    prompt = (
        prompt_template
        .replace("{{customer_email}}", customer_email)
        .replace("{{rag_context}}", rag_context)
        .replace(
            "{{decision_criteria}}",
            yaml.dump(decision_criteria, allow_unicode=True),
        )
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    print("\n[local-llm] Sending prompt to Ollama...\n")
    print("[local-llm] Model is generating response, this may take a moment...")

    response = requests.post(OLLAMA_URL, json=payload, timeout=600)
    response.raise_for_status()

    result = response.json()["response"]

    print("\n=== DRAFT RESPONSE (LOCAL LLM) ===\n")
    print(result)
    print("\n=== END ===\n")


if __name__ == "__main__":
    main()
