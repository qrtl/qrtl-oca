This module exposes chatter (`mail.message`) search as `ai_tool` MCP tools,
allowing AI agents to look up conversation history across any record.

Two tools are provided:

- **search_messages**: searches chatter messages by one or more keywords
  (matching subject, body and record name), returning the matching messages'
  content plus the model/id of the record they are attached to, grouped per
  keyword.
- **get_messages_for_records**: given a list of `{model, id}` record
  references, returns the full chatter message history logged against each
  of those records.
