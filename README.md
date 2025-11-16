# Google AI Tinkerers Hackathon — Demo App: Bridging Gaps in VLM with Agentic Systems

*Agent-powered app scaffolded from the GoogleCloudPlatform **agent-starter-pack** (v0.15.2), with a local Streamlit playground, a deployable Agent Engine backend, and Terraform IaC for Google Cloud.*

---

## ✨ What is this?

This repository is a batteries‑included template for building and shipping a Generative AI agent during a hackathon (or beyond):

* **Bring‑your‑own agent**: focus on your agent’s logic; the template handles UI, packaging, and deployment.
* **Local Playground**: iterate quickly with a Streamlit chat UI that hot‑reloads your agent code.
* **Agent Engine backend**: production‑ready service wrapper for your agent.
* **Cloud‑native deployment**: Terraform modules + CI/CD hooks for Google Cloud.
* **Observability**: OpenTelemetry ➜ Cloud Logging/Trace; BigQuery sink + Looker Studio template.

> The project layout follows the starter pack conventions and keeps your agent code in `sam_agent/` alongside a small Streamlit front‑end in `frontend/` and infra in `deployment/`.

---

## 🗂️ Project structure

```
demo3/
├── sam_agent/                 # Core application code
│   ├── agent.py               # Your agent logic (edit me!)
│   ├── agent_engine_app.py    # Agent Engine entrypoint
│   └── utils/                 # Helpers
├── frontend/                  # Streamlit playground UI
├── deployment/                # Terraform + deployment scripts
├── notebooks/                 # Prototyping & evaluation notebooks
├── tests/                     # Unit/integration/load tests
├── Makefile                   # Dev shortcuts
├── GEMINI.md                  # Prompting/AI tool context for the repo
└── pyproject.toml             # Python deps & tool config
```

---

## ✅ Prerequisites

Make sure you have these installed:

* **Python** 3.11+ (recommended)
* **[uv](https://docs.astral.sh/uv/)** (Python package manager)
  *Tip:* install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
* **[Google Cloud SDK](https://cloud.google.com/sdk/docs/install)** (`gcloud`)
* **[Terraform](https://developer.hashicorp.com/terraform/install)**
* **make** (usually preinstalled on Linux/macOS)

> Optional: **Nix** users can `nix develop` using `flake.nix`/`shell.nix`.

---

## 🚀 Quick start (local)

Clone and spin up the playground:

```bash
# 1) Get the code
git clone https://github.com/hadilq/google-aitinker-hackathon-demo.git
cd google-aitinker-hackathon-demo

# 2) Install deps & launch the Streamlit playground
make install && make playground
```

Now open the URL printed by Streamlit and chat with your agent. Edit `sam_agent/agent.py` and save — the playground auto‑reloads.

---

## 🧠 Develop your agent

1. **Prototype** in `notebooks/` (e.g., quick LLM/tooling experiments, evaluation with Vertex AI Evaluation).
2. **Implement** the production path in `sam_agent/agent.py` (inputs ➜ tool calls ➜ outputs).
3. **Run locally** via `make playground` and iterate.

---

## 🧪 Quality: tests & linting

```bash
make test      # unit/integration tests
make lint      # ruff, mypy, codespell, etc.
```

### Evaluate on a public multi-object image set

You can quickly exercise the agent against the sample dataset at
`https://github.com/inbarhub/single_image_dataset/tree/main/images` by running:

```bash
uv run python -m sam_agent.utils.dataset_evaluator \
  --prompt "Describe the picture: what kind of objects can you see on it, and how many of them?" \
  --output data/eval-results.json
```

The script downloads the dataset, sends each image to the configured Gemini
vision model, and writes responses to `data/eval-results.json`.

---

## ☁️ Deploy to Google Cloud

There are two common paths:

### 1) One‑command CI/CD bootstrap (recommended)

This sets up a GitHub‑based pipeline and GCP infra with Terraform.

```bash
# From the repo root (after authenticating gcloud)
uvx agent-starter-pack setup-cicd
```

Follow the prompts to provision:

* GCP projects (dev/prod)
* Artifact/Secret storage
* Cloud Build or GitHub Actions CI/CD
* Terraform state and service accounts

### 2) Manual dev deploy

```bash
# Pick your dev project
gcloud config set project <your-dev-project-id>

# Deploy the Agent Engine backend (Cloud Run or equivalent)
make backend
```

For full infra details see `deployment/` (Terraform modules, variables, environments).

---

## 🔧 Configuration

Environment values vary by setup; common ones include:

* `GCP_PROJECT_ID` – your Google Cloud project
* `GCP_REGION` – e.g., `us-central1`
* `BIGQUERY_DATASET` – for logs/metrics sink
* `OTEL_EXPORTER_OTLP_ENDPOINT` – custom OTLP exporter if not using default GCP
* `MODEL_*` / provider keys – if your agent calls external models/tools

> The repo may include an `.envrc` for [direnv](https://direnv.net/). If present, adjust values and `direnv allow`.

---

## 🔭 Monitoring & analytics

* **OpenTelemetry** emits traces/logs ➜ **Cloud Trace** & **Cloud Logging**.
* **BigQuery** stores long‑term events; use the included **Looker Studio** dashboard template to visualize them.

---

## 🧰 Make targets

| Command              | What it does                            |
| -------------------- | --------------------------------------- |
| `make install`       | Install dependencies with **uv**        |
| `make playground`    | Launch local Streamlit UI (auto‑reload) |
| `make backend`       | Build & deploy the Agent Engine service |
| `make test`          | Run tests                               |
| `make lint`          | Run linters/type checks/spell checks    |
| `make setup-dev-env` | Bootstrap dev resources with Terraform  |
| `uv run jupyter lab` | Start Jupyter Lab for notebooks         |

---

## 🗺️ Roadmap ideas (hackathon‑friendly)

* Tool abstractions (search/db/calendar) with simple stubs
* Thin evaluation harness (prompt/response datasets + metrics)
* Minimal auth session state for the playground

---

## 🤝 Contributing

PRs welcome! Please:

* Keep code in `sam_agent/` small & composable
* Add/adjust tests in `tests/`
* Run `make lint && make test` before pushing

---

## 📄 License

Choose a license (e.g., Apache‑2.0, MIT) and add `LICENSE`.

---

## 🙏 Acknowledgements

* Based on **googleCloudPlatform/agent-starter-pack** (v0.15.2).
* Thanks to the Google AI Tinkerers community for examples and feedback.
# demo3


Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.15.2`

## Project Structure

This project is organized as follows:

```
demo3/
├── sam_agent/                 # Core application code
│   ├── agent.py         # Main agent logic
│   ├── agent_engine_app.py # Agent Engine application logic
│   └── utils/           # Utility functions and helpers
├── .cloudbuild/         # CI/CD pipeline configurations for Google Cloud Build
├── deployment/          # Infrastructure and deployment scripts
├── notebooks/           # Jupyter notebooks for prototyping and evaluation
├── tests/               # Unit, integration, and load tests
├── Makefile             # Makefile for common commands
├── GEMINI.md            # AI-assisted development guide
└── pyproject.toml       # Project dependencies and configuration
```

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)
- **Terraform**: For infrastructure deployment - [Install](https://developer.hashicorp.com/terraform/downloads)
- **make**: Build automation tool - [Install](https://www.gnu.org/software/make/) (pre-installed on most Unix-based systems)


## Quick Start (Local Testing)

Install required packages and launch the local development environment:

```bash
make install && make playground
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Install all required dependencies using uv                                                  |
| `make playground`    | Launch Streamlit interface for testing agent locally and remotely |
| `make backend`       | Deploy agent to Agent Engine |
| `make test`          | Run unit and integration tests                                                              |
| `make lint`          | Run code quality checks (codespell, ruff, mypy)                                             |
| `make setup-dev-env` | Set up development environment resources using Terraform                         |
| `uv run jupyter lab` | Launch Jupyter notebook                                                                     |

For full command options and usage, refer to the [Makefile](Makefile).


## Usage

This template follows a "bring your own agent" approach - you focus on your business logic, and the template handles everything else (UI, infrastructure, deployment, monitoring).

1. **Prototype:** Build your Generative AI Agent using the intro notebooks in `notebooks/` for guidance. Use Vertex AI Evaluation to assess performance.
2. **Integrate:** Import your agent into the app by editing `sam_agent/agent.py`.
3. **Test:** Explore your agent functionality using the Streamlit playground with `make playground`. The playground offers features like chat history, user feedback, and various input types, and automatically reloads your agent on code changes.
4. **Deploy:** Set up and initiate the CI/CD pipelines, customizing tests as necessary. Refer to the [deployment section](#deployment) for comprehensive instructions. For streamlined infrastructure deployment, simply run `uvx agent-starter-pack setup-cicd`. Check out the [`agent-starter-pack setup-cicd` CLI command](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Currently supports GitHub with both Google Cloud Build and GitHub Actions as CI/CD runners.
5. **Monitor:** Track performance and gather insights using Cloud Logging, Tracing, and the Looker Studio dashboard to iterate on your application.

The project includes a `GEMINI.md` file that provides context for AI tools like Gemini CLI when asking questions about your template.


## Deployment

> **Note:** For a streamlined one-command deployment of the entire CI/CD pipeline and infrastructure using Terraform, you can use the [`agent-starter-pack setup-cicd` CLI command](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Currently supports GitHub with both Google Cloud Build and GitHub Actions as CI/CD runners.

### Dev Environment

You can test deployment towards a Dev Environment using the following command:

```bash
gcloud config set project <your-dev-project-id>
make backend
```


The repository includes a Terraform configuration for the setup of the Dev Google Cloud project.
See [deployment/README.md](deployment/README.md) for instructions.

### Production Deployment

The repository includes a Terraform configuration for the setup of a production Google Cloud project. Refer to [deployment/README.md](deployment/README.md) for detailed instructions on how to deploy the infrastructure and application.


## Monitoring and Observability
> You can use [this Looker Studio dashboard](https://lookerstudio.google.com/reporting/46b35167-b38b-4e44-bd37-701ef4307418/page/tEnnC
) template for visualizing events being logged in BigQuery. See the "Setup Instructions" tab to getting started.

The application uses OpenTelemetry for comprehensive observability with all events being sent to Google Cloud Trace and Logging for monitoring and to BigQuery for long term storage.
