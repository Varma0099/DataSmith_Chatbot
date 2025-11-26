LOG FILES DIRECTORY
===================

This directory contains all system logs.

Log files created automatically:
- system.log          : System initialization, startup events, configuration
- conversations.log   : Complete conversation history in JSON format
- agent_activity.log  : Agent actions, tool calls, RAG queries, decisions
- errors.log          : All errors with stack traces and context

Log files are created when the application starts and are appended to during operation.

Log Format:
All logs use timestamp format: YYYY-MM-DD HH:MM:SS,mmm

Conversation logs use JSON format for easy parsing:
{
  "timestamp": "ISO-8601 format",
  "user_id": "session identifier",
  "agent_type": "receptionist | clinical",
  "user_message": "user input",
  "agent_response": "agent output",
  "metadata": {}
}

Viewing Logs:
- Windows: type logs\system.log
- Linux/Mac: cat logs/system.log
- Or open with any text editor

Analyzing Logs:
- Use grep/findstr for searching
- Import JSON logs into analysis tools
- Monitor for errors and performance issues

Log Rotation:
Currently logs append indefinitely. For production:
- Implement log rotation (daily/weekly)
- Archive old logs
- Set up log monitoring alerts

Privacy Note:
- Logs contain conversation data
- Keep logs secure
- Do not share logs publicly
- In production, implement log anonymization

