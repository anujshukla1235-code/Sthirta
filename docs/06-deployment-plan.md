# 06 - Deployment Plan: Project Sthirta (स्थिरता) — Churn Prediction with Explainability & Retention Strategy

## Target Environment
- **Platform:** Streamlit Community Cloud (Platform-as-a-Service)
- **Compute Constraints:** Max 1GB RAM, 1 CPU (Free Tier limitations).
- **Source Control:** GitHub (`main` branch triggers automatic deployments).

## Secrets Management
- All sensitive configurations (Cost Matrix financial variables, dummy DB passwords for feedback loop, API keys if applicable) are stored in the Streamlit Cloud interface under `Settings > Secrets`.
- Locally, these are mirrored in a `.streamlit/secrets.toml` file, which is strictly added to `.gitignore`.

## Deployment Steps
1. **Prepare Release:** Merge all passing feature branches into `main`. Ensure version bump in `pyproject.toml` or `requirements.txt`.
2. **Pre-compute Cache:** Run the `batch_inference_and_shap.py` script locally or via GitHub Actions to generate the updated SQLite/Parquet cache database. Commit the updated cache (if small enough for Git LFS) or upload it to a cloud bucket (S3/GCS) that the app pulls from on startup.
3. **Trigger Build:** Push to `main`. Streamlit Community Cloud webhook automatically detects the push and begins the container rebuild.
4. **Health Check:** Monitor the build logs in the Streamlit console. Verify that dependencies resolve cleanly.
5. **Validation:** Navigate to the public URL. Execute TC-10 and TC-11 (search customer, verify SHAP plot loads).

## CI/CD Pipeline
- **GitHub Actions Workflow:**
  - **Linting:** Ruff and Black run on all Pull Requests.
  - **Testing:** Pytest executes TC-01 through TC-08.
  - **Build Gate:** Deployment is blocked if code coverage drops below 80% or if any tests fail.

## Rollback Strategy
- **Version Control:** Deployments are tied to specific GitHub commits.
- **Rollback Execution:** If a critical bug is discovered in production, execute a `git revert` of the offending merge commit, or force Streamlit to deploy from a previous stable git tag (e.g., `v1.2.0`). The web app will automatically rebuild to the stable state within 2 minutes.

## Free-Tier Limitations & Mitigations
- **Cold Starts:** Streamlit Cloud will put the app to sleep after a period of inactivity. The first user to visit will experience a 30-60 second "waking up" delay.
- **Mitigation:** A scheduled ping (e.g., cron job or uptime monitoring tool) can be configured to keep the instance warm during peak business hours.
