import json
import tempfile
import unittest
from pathlib import Path
from campus_access.storage import RequestManager


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.manager = RequestManager()
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "requests.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_create_request(self):
        self.assertEqual(self.manager.create_request("F001", "visitor"),
                         {"id": "A001", "fellow_id": "F001", "card_type": "visitor", "status": "requested", "approved_by": None})

    def test_reject_blank_fellow(self):
        with self.assertRaises(ValueError):
            self.manager.create_request("  ", "visitor")
        self.assertEqual(self.manager.list_requests(), [])

    def test_reject_invalid_card_type(self):
        with self.assertRaises(ValueError):
            self.manager.create_request("F001", "vip")

    def test_reject_wrong_input_type(self):
        with self.assertRaises(ValueError):
            self.manager.create_request(123, "staff")

    def test_reject_malformed_and_unicode_id(self):
        self.manager.create_request("F001", "staff")
        for request_id in ("A1", "A٠٠١", "AABC", "B001"):
            with self.subTest(request_id=request_id), self.assertRaises(ValueError):
                self.manager.get_request(request_id)

    def test_reload_generates_next_id(self):
        self.manager.create_request("F001", "visitor")
        self.manager.save_requests(self.path)
        other = RequestManager()
        other.load_requests(self.path)
        self.assertEqual(other.create_request("F002", "staff")["id"], "A002")

    def test_corrupt_json_preserves_memory(self):
        self.manager.create_request("F001", "visitor")
        before = self.manager.list_requests()
        self.path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.manager.load_requests(self.path)
        self.assertEqual(self.manager.list_requests(), before)

    def test_duplicate_id_rejected(self):
        row = self.manager.create_request("F001", "visitor")
        self.path.write_text(json.dumps({"requests": [row, row], "next_number": 2}), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.manager.load_requests(self.path)

    def test_missing_keys_rejected(self):
        row = self.manager.create_request("F001", "visitor")
        del row["status"]
        self.path.write_text(json.dumps({"requests": [row], "next_number": 2}), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.manager.load_requests(self.path)

    def test_read_only_lookup(self):
        self.manager.create_request("F001", "visitor")
        copy = self.manager.get_request("A001")
        copy["status"] = "returned"
        self.assertEqual(self.manager.get_request("A001")["status"], "requested")

    def test_invalid_state_rejected(self):
        row = self.manager.create_request("F001", "visitor")
        row["status"] = "magic"
        self.path.write_text(json.dumps({"requests": [row], "next_number": 2}), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.manager.load_requests(self.path)

    def test_failed_save_preserves_file(self):
        self.path.write_text("original", encoding="utf-8")
        with self.assertRaises(TypeError):
            self.manager.save_requests(None)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "original")


if __name__ == "__main__":
    unittest.main()
