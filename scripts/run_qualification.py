from pathlib import Path
import json
import yaml

from extract_signals import extract_signals, load_text


def main():
    base_dir = Path(__file__).resolve().parent.parent

    # Paths
    email_path = base_dir / "queries" / "client_email_01.txt"
    criteria_path = base_dir / "config" / "decision_criteria_bess.yaml"
    qualification_prompt_path = base_dir / "prompts" / "qualification_prompt.md"
    extract_prompt_path = base_dir / "prompts" / "extract_signals_prompt.md"
    rag_context_path = base_dir / "scripts" / "rag_context_example.txt"

    # Load inputs
    customer_email = load_text(email_path)
    qualification_prompt_template = load_text(qualification_prompt_path)
    extract_prompt_template = load_text(extract_prompt_path)
    rag_context = load_text(rag_context_path)

    with open(criteria_path, encoding="utf-8") as f:
        decision_criteria = yaml.safe_load(f)

    # --- NEW PART: extract signals ---
    signals = extract_signals(customer_email, extract_prompt_template)

    # Build final prompt
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

    print("\n=== QUALIFICATION PROMPT (READY FOR LLM) ===\n")
    print(filled_prompt)
    print("\n=== END ===\n")


if __name__ == "__main__":
    main()
