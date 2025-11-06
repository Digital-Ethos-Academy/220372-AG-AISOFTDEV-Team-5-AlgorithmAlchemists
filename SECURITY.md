# Security Guidelines

## Secret Management
- Never commit real API keys. `.env` is ignored; use `.env.example` for placeholders.
- If a secret is exposed (e.g., pasted into a chat or commit), ROTATE immediately at the provider.
- Maintain a rotation log (date, key, owner). 

## Environment Variables
| Variable | Purpose | Rotate? | Notes |
|----------|---------|---------|-------|
| INTERNAL_ACCESS_TOKEN | Protects internal runtime metrics | Yes | Set per environment |
| REC_DISABLE / QUIZ_DISABLE | Feature flags | No | 0 = enabled demo |
| OPENAI_API_KEY / ANTHROPIC_API_KEY / etc. | Future AI integrations | Yes | Leave blank for demo |

## Network & CORS
- Default CORS is permissive for demo; set `CORS_ORIGINS` to explicit comma list (e.g. `https://demo.example.com`).

## Logging & Audit
- Audit log (`logs/audit.jsonl`) is ignored; do not commit. Ensure proper file permissions (600) in production.
- Structured logs should omit secrets. Add validation step in CI to scan logs for key patterns when exporting.

## Dependency & Vulnerability Management
- Run `pip-audit` and `bandit` in CI (already available in requirements). Fail build on HIGH severity.
- Frontend: `npm audit --production` for deploy image.

## Transport Security
- Terminate TLS at ingress / load balancer in cloud. Internal container listens on HTTP only (port 8000).

## Rate Limiting (Future)
- Add simple token bucket or gateway-level rate limits before opening public access.

## Incident Response (Demo Scope)
1. Identify exposure (log, commit, chat).  
2. Revoke & rotate secret.  
3. Invalidate caches / redeploy with new env.  
4. Document in rotation log + open incident ticket if sensitive integration.  

## Hardening Roadmap
| Phase | Control | Status |
|-------|---------|--------|
| 1 | Secret scanning (pre-commit + CI) | Planned |
| 1 | CORS restricted origins | Planned |
| 2 | API key / JWT auth layer | Future |
| 2 | Rate limiting | Future |
| 3 | RBAC by endpoint | Future |
| 3 | Encrypted at-rest store | Future |

## Do Not
- Embed secrets in prompt templates.
- Return stack traces to clients (we already map to error envelope).
- Log full request bodies containing potential sensitive data.

---
For security questions contact: Engineering Lead / Security Champion.
