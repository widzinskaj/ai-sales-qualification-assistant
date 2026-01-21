from pathlib import Path
import yaml


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def main():
    base_dir = Path(__file__).resolve().parent.parent

    email_path = base_dir / "queries" / "client_email_01.txt"
    criteria_path = base_dir / "config" / "decision_criteria_bess.yaml"
    prompt_path = base_dir / "prompts" / "qualification_prompt.md"
    rag_context_path = base_dir / "scripts" / "rag_context_example.txt"

    customer_email = load_text(email_path)

    with open(criteria_path, encoding="utf-8") as f:
        decision_criteria = yaml.safe_load(f)

    rag_context = load_text(rag_context_path)
    prompt_template = load_text(prompt_path)

    filled_prompt = (
        prompt_template
        .replace("{{customer_email}}", customer_email)
        .replace("{{rag_context}}", rag_context)
        .replace("{{decision_criteria}}", yaml.dump(decision_criteria, allow_unicode=True))
    )

    print("\n=== QUALIFICATION PROMPT (READY FOR LLM) ===\n")
    print(filled_prompt)
    print("\n=== END ===\n")


if __name__ == "__main__":
    main()
