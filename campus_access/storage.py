"""Engineer A: create, validate, save and load card requests."""
import json
import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path

FIELDS = {'id', 'fellow_id', 'card_type', 'status', 'approved_by'}
TYPES = {'visitor', 'student', 'staff'}
STATES = {'requested', 'approved', 'issued', 'returned'}


class RequestManager:
    def __init__(self):
        self.requests = {}
        self.next_number = 1

    def check_id(self, request_id):
        if not isinstance(request_id, str) or not re.fullmatch(r'A[0-9]{3,}', request_id):
            raise ValueError('Invalid request ID')

    def check_record(self, record):
        if not isinstance(record, dict) or set(record) != FIELDS:
            raise ValueError('Missing or extra fields')
        self.check_id(record['id'])
        if not isinstance(record['fellow_id'], str) or not record['fellow_id'].strip():
            raise ValueError('Invalid fellow ID')
        if record['card_type'] not in TYPES or record['status'] not in STATES:
            raise ValueError('Invalid card type or status')
        approver = record['approved_by']
        if record['status'] == 'requested':
            if approver is not None:
                raise ValueError('New requests cannot have an approver')
        elif not isinstance(approver, str) or not approver.strip():
            raise ValueError('Approval is required')

    def create_request(self, fellow_id, card_type):
        if not isinstance(fellow_id, str) or not fellow_id.strip():
            raise ValueError('Fellow ID cannot be blank')
        if not isinstance(card_type, str) or card_type not in TYPES:
            raise ValueError('Invalid card type')
        key = f'A{self.next_number:03d}'
        record = dict(id=key, fellow_id=fellow_id.strip(), card_type=card_type,
                      status='requested', approved_by=None)
        self.requests[key] = record
        self.next_number += 1
        return deepcopy(record)

    def get_request(self, request_id):
        self.check_id(request_id)
        if request_id not in self.requests:
            raise ValueError('Request not found')
        return deepcopy(self.requests[request_id])

    def list_requests(self):
        return deepcopy(list(self.requests.values()))

    def change_status(self, request_id, expected, new, approved_by=None):
        steps = {('requested', 'approved'), ('approved', 'issued'),
                 ('issued', 'returned')}
        if (expected, new) not in steps:
            raise ValueError('Invalid transition')
        record = self.get_request(request_id)
        if record['status'] != expected:
            raise ValueError('Wrong current status')
        if new == 'approved':
            if not isinstance(approved_by, str) or not approved_by.strip():
                raise ValueError('Approver cannot be blank')
            record['approved_by'] = approved_by.strip()
        elif approved_by is not None:
            raise ValueError('Unexpected approver')
        if new == 'issued' and not record['approved_by']:
            raise ValueError('Approval required before issue')
        record['status'] = new
        self.check_record(record)
        self.requests[request_id] = record  # Change only after all checks pass
        return deepcopy(record)

    def save_requests(self, path):
        path = Path(path)
        data = {'requests': self.list_requests(), 'next_number': self.next_number}
        # Save to a temporary file first, so a failed write won't destroy old data.
        name = None
        try:
            with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False,
                                             encoding='utf-8') as file:
                name = file.name
                json.dump(data, file, indent=2)
            os.replace(name, path)
        finally:
            if name and os.path.exists(name):
                os.unlink(name)

    def load_requests(self, path):
        try:
            with open(path, encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError('Broken JSON file') from error
        if not isinstance(data, dict) or set(data) != {'requests', 'next_number'}:
            raise ValueError('Invalid saved data')
        rows, number = data['requests'], data['next_number']
        if not isinstance(rows, list) or type(number) is not int or number < 1:
            raise ValueError('Invalid saved data')
        found = {}
        for row in rows:
            self.check_record(row)
            key = row['id']
            if key in found or int(key[1:]) >= number:
                raise ValueError('Duplicate ID or invalid next number')
            found[key] = deepcopy(row)
        self.requests, self.next_number = found, number  # Update only if valid