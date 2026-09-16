# 06 - Deployment Plan: Churn Prediction with Explainability & Retention Strategy

## Environments
- **Local/dev**: development machine, `.env` for any secrets/API keys
- **Production**: Streamlit Community Cloud (free tier)

## Deployment Steps
1. Push final code to a public GitHub repository.
2. Connect the repository to Streamlit Community Cloud.
3. Configure build/start commands and environment variables.
4. Deploy and verify the public URL loads correctly.
5. Add the live link + repo link to the portfolio site (project 10).

## CI/CD (minimum viable)
- GitHub Actions workflow: run lint + tests on every push to `main`.
- (Project 08 goes further with a full CI/CD + model registry setup — reuse that pattern here if time allows.)

## Rollback Plan
- Keep deployments tied to tagged GitHub releases (`v1.0`, `v1.1`, ...) so you can redeploy a previous tag if a release breaks.

## Known Free-Tier Limitations
- Free-tier services may "sleep" after ~30 minutes of inactivity, causing a slow first load (cold start). Mention this proactively if demoing live to a recruiter.
