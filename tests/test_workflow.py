import unittest
from campus_access.storage import RequestManager
from campus_access.workflow import approve_request, issue_card, return_card, run_menu


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.manager = RequestManager()
        self.manager.create_request("F001", "visitor")

    def test_issue_before_approval_unchanged(self):
        before = self.manager.get_request("A001")
        with self.assertRaises(ValueError):
            issue_card(self.manager, "A001")
        self.assertEqual(self.manager.get_request("A001"), before)

    def test_blank_approver_unchanged(self):
        before = self.manager.get_request("A001")
        with self.assertRaises(ValueError):
            approve_request(self.manager, "A001", "  ")
        self.assertEqual(self.manager.get_request("A001"), before)

    def test_full_workflow(self):
        self.assertEqual(approve_request(self.manager, "A001", "M01")["status"], "approved")
        self.assertEqual(issue_card(self.manager, "A001")["status"], "issued")
        self.assertEqual(return_card(self.manager, "A001")["status"], "returned")

    def test_double_return_and_reissue_rejected(self):
        approve_request(self.manager, "A001", "M01")
        issue_card(self.manager, "A001")
        return_card(self.manager, "A001")
        before = self.manager.get_request("A001")
        for action in (return_card, issue_card):
            with self.assertRaises(ValueError):
                action(self.manager, "A001")
            self.assertEqual(self.manager.get_request("A001"), before)

    def test_unknown_id(self):
        with self.assertRaises(ValueError):
            approve_request(self.manager, "A999", "M01")

    def test_invalid_menu_option_retries(self):
        answers = iter(["oops", "6", "9"])
        output = []
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            run_menu(self.manager, Path(directory) / "requests.json",
                     input_fn=lambda prompt: next(answers), output_fn=output.append)
        self.assertTrue(any("Invalid option" in str(line) for line in output))
        self.assertTrue(any("Goodbye" in str(line) for line in output))


if __name__ == "__main__":
    unittest.main()