"""Engineer B: card actions and terminal menu."""
from .storage import RequestManager


def approve_request(manager, request_id, approved_by):
    return manager.change_status(request_id, 'requested', 'approved', approved_by)


def issue_card(manager, request_id):
    return manager.change_status(request_id, 'approved', 'issued')


def return_card(manager, request_id):
    return manager.change_status(request_id, 'issued', 'returned')


def run_menu(manager=None, path='data/requests.json', input_fn=input, output_fn=print):
    manager = manager if manager is not None else RequestManager()
    while True:
        output_fn("\n" + "=" * 50)
        output_fn("           CAMPUS ACCESS MANAGER")
        output_fn("=" * 50)
        output_fn("  REQUEST MANAGEMENT")
        output_fn("  [1] Create Request")
        output_fn("  [2] View Request")
        output_fn("  [3] Approve Request")
        output_fn("")
        output_fn("  CARD MANAGEMENT")
        output_fn("  [4] Issue Card")
        output_fn("  [5] Return Card")
        output_fn("  [6] List All Requests")
        output_fn("")
        output_fn("  DATA MANAGEMENT")
        output_fn("  [7] Save Records")
        output_fn("  [8] Load Records")
        output_fn("  [9] Exit")
        output_fn("=" * 50)
        try:
            choice = input_fn('Choice: ').strip()
            if choice == '1':
                result = manager.create_request(input_fn('Fellow ID: '), input_fn('Card type: '))
            elif choice == '2':
                result = manager.get_request(input_fn('Request ID: '))
            elif choice == '3':
                result = approve_request(manager, input_fn('Request ID: '), input_fn('Approver: '))
            elif choice == '4':
                result = issue_card(manager, input_fn('Request ID: '))
            elif choice == '5':
                result = return_card(manager, input_fn('Request ID: '))
            elif choice == '6':
                result = manager.list_requests()
            elif choice == '7':
                manager.save_requests(path)
                result = 'Saved'
            elif choice == '8':
                manager.load_requests(path)
                result = 'Loaded'
            elif choice == '9':
                manager.save_requests(path)
                output_fn('Goodbye! Saved successfully.')
                return
            else:
                output_fn('Invalid option. Try 1 to 9.')
                continue
            output_fn(result)
        except (ValueError, OSError) as error:
            output_fn(f'Error: {error}')
        except (EOFError, KeyboardInterrupt):
            output_fn('Input interrupted. Unsaved changes may remain.')
            return
            