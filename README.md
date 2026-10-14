# Campus Access Manager

## Project Description

Campus Access Manager is a Python command-line application
for managing access card requests for campus fellows.

The system allows users to create, approve, issue, and
return access cards.

## Team Members

- Engineer A: Request validation and JSON storage
- Engineer B: Access card workflow and command-line interface

## Features

1. Create access card requests.
2. View existing requests.
3. Approve requests.
4. Issue approved cards.
5. Return issued cards.
6. List all requests.
7. Save records to JSON.
8. Load saved records.
9. Exit the application.

## Technologies Used

- Python 3
- JSON
- Git and GitHub
- Python unittest

## How to Run

Open a terminal in the project folder.

Run:

```bash
python3 main.py
```

Follow the instructions displayed in the menu.

## How to Run Tests

Run:

```bash
python3 -m unittest discover -s tests -v
```

## Project Structure

- main.py: Runs the application.
- campus_access/storage.py: Manages requests and data storage.
- campus_access/workflow.py: Manages card approval, issuance, and returns.
- tests/: Contains automated tests.
- docs/: Contains project documentation.

## Access Card Workflow

requested → approved → issued → returned

Each request must follow the correct order.

## Collaboration

Both engineers worked on separate Git branches.

Engineer A implemented request validation and storage.

Engineer B implemented the access card workflow and CLI.

Each engineer submitted a pull request that was reviewed
by the other engineer before merging into main.