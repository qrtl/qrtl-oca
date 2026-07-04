from odoo.tests.common import TransactionCase

from ..models.mail_message import SNIPPET_LEN


class TestMailMessageSearch(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Search Test Partner"})
        cls.partner.message_post(body="The quick brown fox jumps")

    def test_search_messages_hit(self):
        result = self.env["mail.message"]._ai_search_messages(terms=["quick brown"])
        hits = result["results"]["quick brown"]
        self.assertTrue(hits)
        self.assertEqual(hits[0]["model"], "res.partner")
        self.assertEqual(hits[0]["id"], self.partner.id)
        self.assertIn("quick brown", hits[0]["content"])
        self.assertEqual(hits[0]["record_name"], self.partner.name)
        self.assertEqual(hits[0]["author"], self.env.user.partner_id.name)
        self.assertTrue(hits[0]["date"])

    def test_search_messages_miss(self):
        result = self.env["mail.message"]._ai_search_messages(
            terms=["no such phrase xyz"]
        )
        self.assertEqual(result["results"]["no such phrase xyz"], [])

    def test_search_messages_word_order_independent(self):
        # Each word must appear somewhere in the message, not necessarily
        # contiguous or in the original order.
        result = self.env["mail.message"]._ai_search_messages(terms=["fox quick"])
        hits = result["results"]["fox quick"]
        self.assertTrue(hits)
        self.assertEqual(hits[0]["id"], self.partner.id)

    def test_search_messages_empty_term(self):
        # An empty/whitespace-only term must not fall back to an unfiltered
        # (match-everything) search.
        result = self.env["mail.message"]._ai_search_messages(terms=["  "])
        self.assertEqual(result["results"]["  "], [])

    def test_search_messages_multiple_terms(self):
        result = self.env["mail.message"]._ai_search_messages(
            terms=["quick brown", "no such phrase xyz"]
        )
        self.assertTrue(result["results"]["quick brown"])
        self.assertEqual(result["results"]["no such phrase xyz"], [])

    def test_search_messages_snippet_truncated(self):
        partner = self.env["res.partner"].create({"name": "Long Body Partner"})
        partner.message_post(body="uniquetoken " + "x" * 600)
        result = self.env["mail.message"]._ai_search_messages(terms=["uniquetoken"])
        hits = result["results"]["uniquetoken"]
        self.assertTrue(hits)
        self.assertEqual(len(hits[0]["content"]), SNIPPET_LEN)

    def test_search_messages_email_from_fallback(self):
        self.env["mail.message"].create(
            {
                "model": "res.partner",
                "res_id": self.partner.id,
                "author_id": False,
                "email_from": "external@example.com",
                "body": "unauthored message",
                "message_type": "email",
            }
        )
        result = self.env["mail.message"]._ai_search_messages(terms=["unauthored"])
        hits = result["results"]["unauthored"]
        self.assertTrue(hits)
        self.assertEqual(hits[0]["author"], "external@example.com")

    def test_search_messages_excludes_unlinked_messages(self):
        # A message with no model/res_id (e.g. a private note) must not be
        # returned even if its body matches.
        self.env["mail.message"].create(
            {"body": "orphankeyword message", "model": False, "res_id": False}
        )
        result = self.env["mail.message"]._ai_search_messages(terms=["orphankeyword"])
        self.assertEqual(result["results"]["orphankeyword"], [])

    def test_get_messages_for_records(self):
        partner2 = self.env["res.partner"].create({"name": "Second Partner"})
        partner2.message_post(body="another message here")
        result = self.env["mail.message"]._ai_get_messages_for_records(
            records=[
                {"model": "res.partner", "id": self.partner.id},
                {"model": "res.partner", "id": partner2.id},
            ]
        )
        record_result, record_result2 = result["records"]
        self.assertEqual(record_result["model"], "res.partner")
        self.assertEqual(record_result["id"], self.partner.id)
        self.assertEqual(record_result["record_name"], self.partner.name)
        self.assertTrue(
            any(
                "quick brown" in message["content"]
                for message in record_result["messages"]
            )
        )
        self.assertEqual(
            record_result["messages"][0]["author"], self.env.user.partner_id.name
        )
        self.assertTrue(record_result["messages"][0]["date"])
        self.assertEqual(record_result2["id"], partner2.id)
        self.assertTrue(
            any(
                "another message here" in message["content"]
                for message in record_result2["messages"]
            )
        )

    def test_get_messages_for_records_no_match(self):
        result = self.env["mail.message"]._ai_get_messages_for_records(
            records=[{"model": "res.partner", "id": self.partner.id + 999999}]
        )
        self.assertEqual(result["records"][0]["messages"], [])
