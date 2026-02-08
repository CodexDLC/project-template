# 🌿 Git Flow & Branching Strategy

[⬅️ Back](./README.md) | [🏠 Docs Root](../../../README.md)

We use a **3 main branches** strategy to ensure code stability and quality.

## 🌳 Branch Structure

### 1. `develop` 🛠️ (Development)

*   **Purpose:** Main branch for integrating new features. Contains "fresh" but potentially unstable code.
*   **Rules:**
    *   All new features (`feature/*`) are merged here via Pull Request (PR).
    *   **CI Checks:** Linters run (`Ruff`, `Mypy`). Database tests are **not** run for speed.
*   **Protection:** Requires passing linters.

### 2. `main` 🧪 (Staging / Pre-Release)

*   **Purpose:** Stable branch ready for release. Acts as Staging environment.
*   **Rules:**
    *   Code enters here only from `develop` via PR.
    *   **CI Checks:** **Full test suite** runs (`Pytest` with DB) and Docker image build check.
*   **Protection:** Strict. Merge only if all tests pass. Direct push forbidden.

### 3. `release` 🚀 (Production)

*   **Purpose:** Code running on the production server.
*   **Rules:**
    *   Code enters here **only from `main`** via PR.
    *   **CD Action:** Pushing to this branch triggers automatic deployment to VPS.
*   **Protection:** Maximum. Merge allowed **only** from `main` branch (controlled by GitHub Actions).

---

## 🔄 Workflow

1.  **New Task:**
    *   Create branch from `develop`: `git checkout -b feature/my-cool-feature develop`.
    *   Write code, commit.
    *   Run local check before push: `.\check_local.ps1` (Windows) or `pwsh` (Linux/Mac).

2.  **Integration (Develop):**
    *   Push and open PR to `develop`.
    *   GitHub Actions checks style and types.
    *   Merge PR.

3.  **Stabilization (Main):**
    *   When features are ready, open PR `develop` -> `main`.
    *   GitHub Actions runs heavy tests.
    *   If all OK — merge.

4.  **Release (Release):**
    *   Open PR `main` -> `release`.
    *   GitHub Actions verifies source is `main`.
    *   After merge, magic begins: Docker build -> Push to GHCR -> VPS Update.
