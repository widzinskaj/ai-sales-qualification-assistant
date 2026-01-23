from pathlib import Path
import json
import yaml
import os
import subprocess

from extract_signals import extract_signals, load_text
from rag_search import get_rag_context


def call_llm(prompt: str, model: str) -> str:
    """
    Call local LLM via Ollama CLI.
    One model, non-streaming.
    Stable on Windows, suitable for MVP/demo.
    """

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


def main():
    base_dir = Path(__file__).resolve().parent.parent

    # --- Runtime config ---
    email_file = os.getenv("QUAL_EMAIL_FILE", "client_email_01.txt")
    llm_model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

    # --- Paths ---
    email_path = base_dir / "queries" / email_file
    criteria_path = base_dir / "config" / "decision_criteria_bess.yaml"
    qualification_prompt_path = base_dir / "prompts" / "qualification_prompt.md"
    extract_prompt_path = base_dir / "prompts" / "extract_signals_prompt.md"

    # --- Load inputs ---
    customer_email = load_text(email_path)
    qualification_prompt_template = load_text(qualification_prompt_path)
    extract_prompt_template = load_text(extract_prompt_path)

    with open(criteria_path, encoding="utf-8") as f:
        decision_criteria = yaml.safe_load(f)

    # --- Step 1: extract explicit signals (LLM-based, extraction only) ---
    signals = extract_signals(customer_email, extract_prompt_template)

    # --- Step 2: retrieve RAG context (background only) ---
    rag_context = get_rag_context(customer_email)

    # --- Step 3: build final qualification prompt ---
    filled_prompt = (
        qualification_prompt_template
        .replace("{{customer_email}}", customer_email)
        .replace(
            "{{known_facts}}",
            json.dumps(signals, indent=2, ensure_ascii=False),
        )
        .replace("{{rag_context}}", rag_context)
        .replace(
            "{{decision_criteria}}",
            yaml.dump(decision_criteria, allow_unicode=True),
        )
    )

    print("\n=== QUALIFICATION PROMPT (SENT TO LLM) ===\n")
    print(filled_prompt)

    # --- Step 4: call LLM for qualification ---
    print("\n=== LLM RESPONSE ===\n")
    response = call_llm(filled_prompt, model=llm_model)
    print(response)

    print("\n=== END ===\n")


if __name__ == "__main__":
    main()
