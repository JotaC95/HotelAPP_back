# Security remediation checklist

## Confirmed exposure

A Django `SECRET_KEY` was previously committed to this public repository. The current configuration reads `DJANGO_SECRET_KEY` from the environment, but the old key remains recoverable from Git history.

## Required operator actions

1. Generate and deploy a new, unique Django signing key. Never reuse the previously committed key.
2. Review whether the old key was used in a deployed environment; assess signed sessions/tokens and invalidate as appropriate.
3. Inspect the committed `db.sqlite3` offline for real user data, tokens, credentials or other sensitive information before deciding how to remove it. Do not upload the database to third-party scanners.
4. Inventory clones, forks, open PRs, deployments and branch protections before any history rewrite.
5. Back up the repository and coordinate a `git filter-repo` history rewrite only after confirming exact paths and impact. Force-pushing rewritten history requires a separate explicit decision; removing files from current HEAD alone does not erase past exposure.
6. Revoke and rotate exposed credentials independently of history cleanup. Contact GitHub support if cached sensitive content needs follow-up.

## Prevent recurrence

Use GitHub secret scanning and push protection when available, keep local `.env` files ignored, and review dependency alerts. Do not place real secrets in `.env.example`.

**Status:** documentation only. No history rewrite, database deletion, or credential rotation has been performed by this change.
