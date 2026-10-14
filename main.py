from pathlib import Path
from campus_access.storage import RequestManager
from campus_access.workflow import run_menu


def main():
    data_path = Path(__file__).resolve().parent / "data" / "requests.json"
    manager = RequestManager()
    if data_path.exists():
        try:
            manager.load_requests(data_path)
        except (ValueError, OSError) as exc:
            print(f"Could not load saved requests: {exc}")
            print("The invalid file was not overwritten. Fix it before continuing.")
            return
    run_menu(manager, data_path)


if __name__ == "__main__":
    main()