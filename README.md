# Process Mining & Agentic Application (PMAA)

A research project that combines **process mining** with **agentic AI** to discover, model, and automate software development workflows from GitHub repository event logs.

## 📄 Paper Reference

This repository implements the approach described in:

**"Using Process Mining to Generate AI Agents from Software Engineering Process Records"**
Submitted to: **BPM 2026** (double-blind review)

## 🎯 Project Overview

This project demonstrates a complete pipeline from raw GitHub data to an operational multi-agent system:

1. **Extract** GitHub repository events into OCEL (Object-Centric Event Log) format
2. **Discover** process models, roles, and behavioral patterns using process mining
3. **Generate** role-specific BPMN models and DECLARE constraints
4. **Build** a LangGraph-based multi-agent application grounded in discovered patterns

## 🏗️ Architecture

```
GitHub Events → OCEL → Role Mining → Process Discovery → Agentic App
```

### Key Components

- **Event Logs**: OCEL 2.0 format capturing issues, commits, users, and tasks
- **Process Mining**: Role-based analysis using pm4py and custom algorithms
- **Discovered Artifacts**: BPMN models, DECLARE constraints, process descriptions
- **Agentic Application**: LangGraph-based multi-agent system for GitHub automation

## 📁 Repository Structure

```
pmaa/
├── 01-09_*.ipynb              # Sequential analysis notebooks
├── enrich_ocel_with_tasks.py  # Task extraction from commit messages
├── commitizen*.json            # OCEL event logs (raw, enriched, annotated)
├── role_logs/                  # Per-role OCEL splits + visualizations
├── bpmn_models/                # Discovered BPMN diagrams per role
├── declare_models/             # Mined DECLARE constraint models
└── langraph-agentic-app/       # Multi-agent application
    ├── src/                    # Python source code
    ├── docs/                   # Architecture documentation
    └── README.md               # App-specific documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Jupyter Notebook
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/liorlimonad/pmaa.git
   cd pmaa
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt  # If available
   ```

3. **Install Jupyter dependencies**
   ```bash
   pip install jupyter pm4py pandas numpy matplotlib
   ```

## 📊 Analysis Pipeline

Run the notebooks in sequence:

1. **01_enrich-ocel-event-log.ipynb** - Parse and enrich OCEL from GitHub data
2. **02_analyze-with-pm4py.ipynb** - Basic process mining analysis
3. **03_resource-role-annotation.ipynb** - Annotate resources with roles
4. **04_split-logs-by-role.ipynb** - Split event log by discovered roles
5. **05_role-process-mining.ipynb** - Per-role process discovery
6. **06_declarative-process-mining.ipynb** - DECLARE constraint mining
7. **07_process_markdowns.ipynb** - Generate process descriptions
8. **08_bpmn_discovery.ipynb** - Discover BPMN models
9. **09_role_declare_model_discovery.ipynb** - Role-specific DECLARE models

## 🤖 Agentic Application

The `langraph-agentic-app/` directory contains a production-ready multi-agent system:

### Features

- **Role-based agents**: Issue Reporter, Bot, Feature Developer, Quality Engineer, etc.
- **GitHub integration**: Real REST API calls with dry-run mode
- **Policy guards**: Risk scoring and DECLARE constraint checking
- **Human-in-the-loop**: Approval gates for high-risk operations
- **Structured state**: TypedDict-based state management

### Quick Start

```bash
cd langraph-agentic-app
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Configure environment
export GITHUB_TOKEN=your_token
export GITHUB_REPO=owner/repo
export GITHUB_ISSUE_ID=123
export GITHUB_DRY_RUN=true

# Run the app
python -m langraph_agentic_app.app
```

See [langraph-agentic-app/README.md](langraph-agentic-app/README.md) for detailed documentation.

## 🔍 Discovered Roles

The process mining analysis identified 8 distinct roles in software development:

1. **Issue Reporter** - Creates and clarifies issues
2. **Bot** - Automated workflow maintenance
3. **Feature Developer** - Implements new features
4. **Maintainer** - Reviews and merges contributions
5. **Quality Engineer** - Testing and validation
6. **Technical Writer** - Documentation
7. **DevOps Engineer** - CI/CD and infrastructure
8. **Contributor** - General contributions

Each role has:
- Dedicated OCEL event log
- OCDFG visualization
- Process description (markdown)
- BPMN model
- DECLARE constraints (where applicable)

## 📈 Key Insights

- **Object-centric approach**: Captures complex many-to-many relationships between issues, commits, users, and tasks
- **Role specialization**: Different roles exhibit distinct behavioral patterns
- **Conventional commits**: Task semantics extracted from commit message patterns
- **Declarative constraints**: Temporal and logical rules governing valid workflows

## 🛠️ Technologies

- **Process Mining**: pm4py, OCEL 2.0
- **Visualization**: matplotlib, graphviz
- **Agentic Framework**: LangGraph, LangChain
- **Data Processing**: pandas, numpy
- **API Integration**: requests (GitHub REST API)

## 📚 Documentation

- [LangGraph App Architecture](langraph-agentic-app/docs/architecture.md)
- [GitHub Setup Guide](langraph-agentic-app/docs/github_setup_and_usage.md)
- [Process Descriptions](role_logs/)
- [BPMN Models](bpmn_models/)

## 🤝 Contributing

This is a research project. For questions or collaboration:

1. Open an issue
2. Review the paper (BPM26_Agent_.pdf)
3. Check existing notebooks and documentation

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- Built on the Commitizen project event log
- Uses pm4py for process mining
- Powered by LangGraph for agent orchestration

## 📧 Contact

For questions about this research, please open an issue or contact the repository maintainer.

---

**Note**: This project demonstrates a research prototype. The agentic application runs in dry-run mode by default to prevent unintended GitHub operations.