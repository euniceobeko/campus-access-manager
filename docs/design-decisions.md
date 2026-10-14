# Design Decisions

## 1. Programming Language

We chose Python because it is easy to read and suitable
for building command-line applications.

## 2. Project Structure

We divided the project into separate files to make
development and teamwork easier.

- storage.py handles requests, validation, and data storage.
- workflow.py handles card approval, issuance, and returns.
- main.py provides the command-line interface.

## 3. Data Storage

We used JSON to save information because it is simple
to read and supported by Python's standard library.

## 4. Request Status

Each access card request follows this order:

requested → approved → issued → returned

This prevents cards from being issued before approval
or returned before issuance.

## 5. Input Validation

The program checks user input to prevent invalid
information and incorrect operations.

## 6. Testing

We used Python's unittest module to test the program.

Automated tests help us confirm that important
functions work correctly.

## 7. Team Collaboration

We used separate Git branches to avoid editing
the same files simultaneously.

Both engineers reviewed each other's pull requests
before merging their contributions.