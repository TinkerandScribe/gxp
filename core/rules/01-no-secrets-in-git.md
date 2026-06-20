# No secrets in version control

Do not commit live API keys, passwords, tokens, or production connection strings.

Use `.env.example` with placeholders only. Keep `.env` and local credential files
gitignored. If a task requires reading secrets for debugging, the operator must
explicitly authorize it in the task brief.
