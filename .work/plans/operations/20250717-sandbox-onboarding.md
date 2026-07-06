# Sandbox onboarding runbook — RFP Platform

**Status:** Draft · **Updated:** 2025-07-17
**Cross-ref:** Foundation doc 02 (integration), ADR-005 (LiteLLM)

---

## 1. External integrations requiring sandbox

| Integration | Sandbox available | V1 need | Status |
|-------------|-------------------|---------|--------|
| LiteLLM → OpenAI | Yes (API key with $5 credit) | P0 | Sign up at platform.openai.com |
| LiteLLM → Anthropic | Yes (API key) | P0 (fallback) | Sign up at console.anthropic.com |
| Email — Microsoft 365 | Yes (Graph API sandbox) | P1 (deferred) | Not needed for V1 |
| Email — Google Workspace | Yes (Gmail API sandbox) | P1 (deferred) | Not needed for V1 |
| Email — IMAP/SMTP | N/A (generic protocol) | P1 (deferred) | Not needed for V1 |

## 2. V1 sandbox setup (LiteLLM)

### Prerequisites
- Docker Compose stack running (see compose proposal)
- `.env` file populated with API keys

### Steps

1. **Create OpenAI account** → [platform.openai.com](https://platform.openai.com)
   - Add billing → set a hard spending limit (e.g., $10)
   - Create API key → copy to `.env` as `LITELLM_API_KEY`

2. **(Optional) Create Anthropic account** → [console.anthropic.com](https://console.anthropic.com)
   - Create API key → add as fallback in LiteLLM config

3. **Test the integration:**
   ```bash
   curl -X POST http://localhost:8000/v1/rag/generate \
     -H "Authorization: Bearer $JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question_id": "...", "rfp_id": "...", "question_text": "Test question"}'
   ```

4. **Verify:**
   - Response contains `answer_text` with meaningful content
   - LiteLLM logs show provider used + token count
   - No `openai-organization:` header errors (verifies non-training opt-out)

### Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `401` from LiteLLM | Missing or invalid API key | Check `.env`; verify key at provider dashboard |
| `429` rate limited | No billing set up | Add payment method; check spending limit |
| Empty answer | Zero KB entries loaded | Upload at least one KB document first |
| Slow response (>10s) | Free tier rate limiting | Upgrade to paid tier for production |

## 3. Production onboarding (future)

When deploying for a real tenant:

1. Provision VPS (4 cores, 8GB RAM minimum)
2. Install Docker + Docker Compose
3. Clone repo → `docker compose build`
4. Set `.env` with real secrets
5. `docker compose up -d`
6. Configure DNS + optional TLS (Traefik Let's Encrypt)
7. Monitor logs: `docker compose logs -f api worker`

No cloud-specific onboarding needed — single-tenant self-hosted deployment.
