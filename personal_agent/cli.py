import argparse
from .agent import PersonalAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Personal AI Agent")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("chat")
    remember = sub.add_parser("remember"); remember.add_argument("content")
    search = sub.add_parser("search-memory"); search.add_argument("query")
    ingest = sub.add_parser("ingest"); ingest.add_argument("path")
    args = parser.parse_args()
    agent = PersonalAgent()
    if args.command == "chat":
        print("Personal AI Agent. Type 'exit' to quit.")
        while True:
            message = input("You: ").strip()
            if message.lower() in {"exit", "quit"}:
                break
            if message:
                print(f"Agent: {agent.respond(message)}")
    elif args.command == "remember":
        agent.memory.remember(args.content); print("Remembered.")
    elif args.command == "search-memory":
        print("\n".join(agent.memory.search(args.query)) or "No matching memories.")
    else:
        print(agent.ingest(args.path))


if __name__ == "__main__":
    main()
