from pathlib import Path


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def extract_signals(email_text: str, prompt_template: str | None = None) -> dict:
    """
    MVP stub:
    - no LLM call
    - no guessing
    - returns empty / unknown signals
    """

    return {
        "object_type": None,
        "has_pv": None,
        "mentions_backup": None
    }


def main():
    base_dir = Path(__file__).resolve().parent.parent
    email_path = base_dir / "queries" / "client_email_01.txt"
    email_text = load_text(email_path)

    signals = extract_signals(email_text)

    print("\n=== EXTRACTED SIGNALS ===\n")
    print(signals)


if __name__ == "__main__":
    main()
