from odoo import models
from odoo.osv import expression
from odoo.tools import html2plaintext

from odoo.addons.ai_tool.tools import aitool

SNIPPET_LEN = 500
DEFAULT_LIMIT = 20
# Same field list/word-tokenization approach as qrtlrepos/axls-oca/mail_message_search's
# mail.thread._search_message_search, adapted here to search mail.message directly
# across all models instead of being scoped to one already-known model.
SEARCH_FIELDS = ["record_name", "subject", "body", "email_from", "reply_to"]


class MailMessage(models.Model):
    _inherit = "mail.message"

    @aitool(
        input_schema={
            "terms": {"type": "array", "items": {"type": "string"}},
        },
        required_inputs=["terms"],
        output_schema={
            "results": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "model": {"type": "string"},
                            "id": {"type": "integer"},
                            "date": {"type": "string", "format": "date-time"},
                            "record_name": {"type": "string"},
                            "author": {"type": "string"},
                        },
                    },
                },
            },
        },
    )
    def _ai_search_messages(self, terms):
        results = {}
        for term in terms:
            words = term.split()
            if not words:
                results[term] = []
                continue
            word_domains = [
                expression.OR([[(field, "ilike", word)] for field in SEARCH_FIELDS])
                for word in words
            ]
            domain = expression.AND(word_domains)
            messages = self.search(domain, limit=DEFAULT_LIMIT, order="date desc")
            results[term] = [
                {
                    "content": html2plaintext(message.body or "")[:SNIPPET_LEN],
                    "model": message.model,
                    "id": message.res_id,
                    "date": message.date.isoformat() if message.date else "",
                    "record_name": message.record_name or "",
                    "author": message.author_id.name or message.email_from or "",
                }
                for message in messages
                if message.model and message.res_id
            ]
        return {"results": results}

    @aitool(
        input_schema={
            "records": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "model": {"type": "string"},
                        "id": {"type": "integer"},
                    },
                    "required": ["model", "id"],
                },
            },
        },
        required_inputs=["records"],
        output_schema={
            "records": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "model": {"type": "string"},
                        "id": {"type": "integer"},
                        "record_name": {"type": "string"},
                        "messages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "content": {"type": "string"},
                                    "date": {"type": "string", "format": "date-time"},
                                    "author": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
        },
    )
    def _ai_get_messages_for_records(self, records):
        result = []
        for ref in records:
            # Cap and keep only the most recent messages, then restore
            # chronological order (oldest first) for display.
            messages = self.search(
                [("model", "=", ref["model"]), ("res_id", "=", ref["id"])],
                order="date desc, id desc",
                limit=DEFAULT_LIMIT,
            )[::-1]
            result.append(
                {
                    "model": ref["model"],
                    "id": ref["id"],
                    "record_name": messages[-1].record_name if messages else "",
                    "messages": [
                        {
                            "content": html2plaintext(message.body or ""),
                            "date": message.date.isoformat() if message.date else "",
                            "author": message.author_id.name
                            or message.email_from
                            or "",
                        }
                        for message in messages
                    ],
                }
            )
        return {"records": result}
