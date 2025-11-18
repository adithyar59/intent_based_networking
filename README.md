# Intent-Based Networking for Campus LAN

**Academic Project** | YANG, NETCONF, and Prometheus Automation

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [What is Intent-Based Networking?](#what-is-intent-based-networking)
- [Project Goal](#project-goal)
- [Architecture & Workflow](#architecture--workflow)
- [Technologies & Tools](#technologies--tools)
- [Project Structure](#project-structure)
- [What Has Been Implemented](#what-has-been-implemented)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Expected Outputs](#expected-outputs)
- [NETCONF Troubleshooting & Demo](#netconf-troubleshooting--demo)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

This project demonstrates a complete **Intent-Based Networking (IBN)** automation workflow for campus LAN management. The system accepts high-level network intents (declarative policies), translates them into standardized YANG-based configurations, deploys them via NETCONF to network devices, and verifies successful deployment using Prometheus monitoring metrics.

The implementation provides a production-ready foundation with:
- **Intent translation** from JSON to YANG-compliant XML
- **Automated NETCONF deployment** with intelligent fallback simulation
- **Prometheus integration** for verification and monitoring
- **Demo-friendly** mock tools and auto-simulation for reproducible results

---

## What is Intent-Based Networking?

**Intent-Based Networking (IBN)** is an approach to network management that allows administrators to define desired network behavior in high-level, declarative terms rather than writing low-level configuration commands.

### Traditional Approach
```
Network Admin → Write CLI commands → Configure device A → Configure device B → ...
```

### Intent-Based Approach
```
Network Admin → Declare intent: "Allow CS VLAN to access internet" 
             → System translates → Auto-deploys to devices → Verifies success
```

### Key Benefits
- **Simplified management**: Express "what" you want, not "how" to do it
- **Reduced errors**: Automated translation eliminates manual configuration mistakes
- **Faster deployment**: One intent can configure multiple devices simultaneously
- **Consistency**: Standardized models (YANG) ensure uniform configurations across vendors
- **Self-verification**: Automated monitoring confirms intent fulfillment

### IBN Lifecycle (This Project)
1. **Intent Declaration**: High-level JSON policy file
2. **Intent Translation**: Convert to YANG-compliant XML configuration
3. **Intent Deployment**: Push via NETCONF to network devices
4. **Intent Verification**: Monitor via Prometheus metrics

---

## Project Goal

**Automate the configuration of a campus LAN by accepting a high-level intent, translating it into YANG-based network configurations, applying them via NETCONF, and verifying successful deployment using Prometheus metrics.**

### Scope
- ✅ Intent parsing and YANG translation
- ✅ NETCONF configuration push (with auto-fallback simulation)
- ✅ Prometheus metric verification
- ✅ Mock tools for testing without real devices
- ✅ Complete automation pipeline

---

## Architecture & Workflow

```
┌─────────────────┐
│  Intent (JSON)  │  campus_policy.json
│  "CS VLAN →     │
│   Internet OK"  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Intent Parser   │  intent_parser.py
│ (JSON → YANG)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ YANG XML Config │  generated_config.xml
│ <campus-network>│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  NETCONF Push   │  netconf_push.py
│  (Real or Sim)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Prometheus    │  verify_prometheus.py
│   Verification  │
└─────────────────┘
```

### Detailed Workflow

1. **Intent Input**: User defines network policy in `intents/campus_policy.json`
   ```json
   {
     "intent": "Allow CS and ECE VLANs to access internet...",
     "vlans": {"CS": 10, "ECE": 20, "ADMIN": 30},
     "policies": {"CS": "internet_access", ...}
   }
   ```

2. **Translation**: `intent_parser.py` reads JSON and generates YANG-compliant XML
   - Validates against `models/campus_lan.yang` schema
   - Produces `generated_config.xml`

3. **Deployment**: `netconf_push.py` attempts real NETCONF push
   - If device unavailable → automatic simulation fallback
   - Logs clear success/failure status

4. **Verification**: `verify_prometheus.py` queries metrics
   - Checks `up` and `node_network_up` metrics
   - Confirms network device health

---

## Technologies & Tools

### Core Technologies

| Technology | Purpose | Version/Details |
|------------|---------|-----------------|
| **YANG** | Data modeling language for network configuration | RFC 6020, 7950 |
| **NETCONF** | Network configuration protocol (over SSH) | RFC 6241 |
| **Prometheus** | Time-series monitoring and alerting | Latest stable |
| **Python 3** | Implementation language | 3.9+ |

### Python Libraries

| Library | Purpose |
|---------|---------|
| `ncclient` | NETCONF client library for Python |
| `prometheus-api-client` | Query Prometheus metrics programmatically |
| `lxml` | XML parsing and generation |
| `paramiko` | SSH transport (dependency of ncclient) |

### Standards & Protocols

- **NETCONF** (RFC 6241): Network configuration protocol
- **YANG** (RFC 6020/7950): Data modeling language
- **SSH** (RFC 4253): Secure transport for NETCONF
- **Prometheus Query API**: RESTful API for metric queries

---

## Project Structure

```
intent_based_networking/
│
├── intents/                          # High-level intent declarations
│   └── campus_policy.json            # Sample intent: VLAN policies
│
├── models/                           # YANG data models
│   └── campus_lan.yang               # Campus LAN YANG schema definition
│
├── scripts/                          # Automation scripts
│   ├── intent_parser.py              # Translate JSON intent → YANG XML
│   ├── netconf_push.py               # Push config via NETCONF (auto-fallback)
│   ├── verify_prometheus.py          # Verify deployment via Prometheus
│   ├── test_netconf_conn.py          # Test NETCONF connectivity & capabilities
│   └── mock_netconf_server.py        # TCP-only mock server (for testing)
│
├── prometheus/                       # Prometheus configuration
│   ├── prometheus.yml                # Scrape configs and targets
│   └── rules.yml                     # Alert rules for network health
│
├── generated_config.xml              # Generated YANG XML (runtime output)
│
├── setup_environment.sh              # Automated environment setup script
│
├── .venv/                            # Python virtual environment (created by setup)
│
└── README.md                         # This file
```

### File Descriptions

#### `intents/campus_policy.json`
High-level intent declaration in JSON format. Defines VLANs and their access policies (e.g., "CS VLAN can access internet, ADMIN VLAN is restricted").

**Example:**
```json
{
  "intent": "Allow CS and ECE VLANs to access the internet, but block ADMIN VLAN...",
  "vlans": {"CS": 10, "ECE": 20, "ADMIN": 30},
  "policies": {"CS": "internet_access", "ECE": "internet_access", "ADMIN": "restricted"}
}
```

#### `models/campus_lan.yang`
YANG data model defining the schema for campus LAN configuration. Includes:
- `container campus-network`
- `list vlan` with keys: `id`, `name`, `policy`
- `typedef` definitions for VLAN IDs and access policies

#### `scripts/intent_parser.py`
**Purpose**: Translate high-level JSON intent into YANG-compliant XML configuration.

**Features**:
- Reads `intents/campus_policy.json`
- Validates structure against YANG model
- Generates `generated_config.xml` with proper namespaces
- Prints confirmation messages

**Output**: `generated_config.xml` (YANG XML configuration)

#### `scripts/netconf_push.py`
**Purpose**: Deploy generated XML configuration to network devices via NETCONF.

**Features**:
- Attempts **real** NETCONF push using `ncclient`
- **Automatic fallback** to deterministic simulation on failure
- Supports environment variable overrides (`NETCONF_HOST`, `NETCONF_PORT`, etc.)
- Clear logging with emoji indicators (✅ success, ❌ error, ⚠️ warning)
- Extracts and displays VLAN information during simulation

**Behavior**:
1. Try real NETCONF connection
2. On failure → automatically switch to simulation mode
3. Simulation parses XML and shows VLAN apply/commit steps
4. Always returns success (for demo reproducibility)

#### `scripts/verify_prometheus.py`
**Purpose**: Verify network device health using Prometheus metrics.

**Features**:
- Connects to Prometheus at `http://localhost:9090`
- Queries `up` (target availability) and `node_network_up` (interface status)
- Prints metric results in readable format
- Handles connection errors gracefully

#### `scripts/test_netconf_conn.py`
**Purpose**: Test NETCONF connectivity and display server capabilities.

**Features**:
- Attempts connection to NETCONF device
- On success: prints server capabilities
- On failure: prints exact error with troubleshooting tips
- Uses same environment variables as `netconf_push.py`

#### `scripts/mock_netconf_server.py`
**Purpose**: Lightweight TCP-only mock server for basic connectivity testing.

**Features**:
- Listens on configurable host/port (default: 127.0.0.1:1830)
- Sends minimal NETCONF `<hello>` XML banner
- Logs incoming connections and data
- Useful for `nc -vz`, `telnet`, or basic port tests

**Limitations**:
- **Not a full SSH/NETCONF server** (no SSH handshake)
- `ncclient` expects SSH and will fail against this mock
- Use for connectivity demo only; real tests require SSH/NETCONF server

#### `prometheus/prometheus.yml`
Prometheus scrape configuration defining:
- Global scrape interval (15s)
- Alert rule file (`rules.yml`)
- Scrape jobs:
  - `prometheus` (self-monitoring)
  - `nodes` (node exporter targets)
  - `network_devices` (campus network device targets: 192.168.1.10:9100, 192.168.1.11:9100)

#### `prometheus/rules.yml`
Alert rules for network health monitoring:
- **Alert**: `NetworkInterfaceDown`
- **Condition**: `node_network_up == 0` for 1 minute
- **Labels**: `severity: warning`

#### `setup_environment.sh`
Automated setup script that:
- Updates apt package lists
- Installs Python 3, python3-venv (if needed)
- Creates `.venv` virtual environment
- Installs Python dependencies (`ncclient`, `prometheus-api-client`, `lxml`)
- Makes scripts executable
- Prints next steps

**Idempotent**: Safe to run multiple times.

---

## What Has Been Implemented

### ✅ Core Features

1. **Intent Parsing Engine**
   - JSON to YANG XML translation
   - Schema validation against YANG model
   - XML generation with proper namespaces
   - Error handling and confirmation messages

2. **NETCONF Deployment**
   - Real NETCONF push via `ncclient` library
   - SSH transport support
   - Environment variable configuration
   - **Intelligent auto-fallback** to simulation mode
   - Deterministic simulation that parses VLAN configs from XML
   - Clear logging with status indicators

3. **Prometheus Verification**
   - Automated metric queries (`up`, `node_network_up`)
   - Connection handling
   - Result formatting and display

4. **Mock & Testing Tools**
   - TCP-only mock NETCONF server for connectivity tests
   - NETCONF connectivity test script
   - Support for testing without real devices

5. **Automated Setup**
   - One-command environment setup
   - Virtual environment management
   - Dependency installation
   - Idempotent operations

### ✅ Advanced Features

- **Auto-Fallback Simulation**: Ensures demos always succeed even without real devices
- **Environment Variable Overrides**: Flexible configuration without code changes
- **Comprehensive Logging**: Clear, emoji-enhanced status messages
- **Error Handling**: Graceful degradation and helpful error messages
- **Modular Design**: Each script is independent and reusable

### ✅ YANG Model Implementation

- Complete YANG schema with:
  - Container structure (`campus-network`)
  - List definitions (`vlan` list with keys)
  - Typedef constraints (VLAN ID range 1-4094)
  - Enumeration types (access policies)
  - Proper namespace and prefix definitions

---

## Setup Instructions

### Prerequisites

- **Ubuntu Linux** (tested on Ubuntu 20.04+)
- **Internet connection** (for package installation)
- **Sudo access** (for system package installation)

### Automated Setup (Recommended)

From the project root directory:

```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

This script will:
1. Update package lists
2. Install Python 3 and venv support
3. Create `.venv` virtual environment
4. Install required Python packages
5. Make all scripts executable

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install ncclient prometheus-api-client lxml

# Make scripts executable
chmod +x scripts/*.py setup_environment.sh
```

### Optional: Prometheus Setup

#### Option 1: System Installation
```bash
sudo apt-get install prometheus prometheus-node-exporter
sudo prometheus --config.file="$(pwd)/prometheus/prometheus.yml"
```

#### Option 2: Docker (Recommended)
```bash
docker run --rm -d \
  -p 9090:9090 \
  -v "$(pwd)/prometheus:/etc/prometheus" \
  --name prometheus \
  prom/prometheus
```

Access Prometheus UI: http://localhost:9090

---

## How to Run

### Complete Workflow (Step-by-Step)

#### Step 1: Activate Virtual Environment

```bash
source .venv/bin/activate
```

Or use venv Python directly:
```bash
.venv/bin/python scripts/intent_parser.py
```

#### Step 2: Generate Configuration from Intent

```bash
python3 scripts/intent_parser.py
```

**Expected Output:**
```
[intent_parser] Starting intent parsing and translation...
[intent_parser] Intent loaded successfully.
[intent_parser] YANG-based XML configuration generated.
[intent_parser] XML saved to: /home/adithya/intent_based_networking/generated_config.xml
Intent successfully translated to YANG config.
```

**Generated File**: `generated_config.xml`

#### Step 3: Push Configuration via NETCONF

**Using default settings** (192.168.1.10:830):
```bash
python3 scripts/netconf_push.py
```

**Using custom device** (override environment variables):
```bash
NETCONF_HOST=127.0.0.1 \
NETCONF_PORT=1830 \
NETCONF_USER=admin \
NETCONF_PASS=admin \
python3 scripts/netconf_push.py
```

**Behavior**:
- Attempts real NETCONF push first
- If connection fails → automatically falls back to simulation
- Prints clear status messages

#### Step 4: Verify via Prometheus

**Prerequisites**: Prometheus must be running on `http://localhost:9090`

```bash
python3 scripts/verify_prometheus.py
```

**Expected Output:**
```
[verify_prometheus] Connecting to Prometheus at http://localhost:9090 ...
[verify_prometheus] Connected to Prometheus.
[verify_prometheus] Querying: up ...
[verify_prometheus] Result for up: [...]
[verify_prometheus] Querying: node_network_up ...
[verify_prometheus] Result for node_network_up: [...]
[verify_prometheus] Verification complete.
```

### Optional: Testing Tools

#### Test NETCONF Connectivity

```bash
# Default device
.venv/bin/python scripts/test_netconf_conn.py

# Custom device
NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 \
.venv/bin/python scripts/test_netconf_conn.py
```

#### Start Mock Server (for connectivity demo)

In a **separate terminal**:
```bash
python3 scripts/mock_netconf_server.py --host 127.0.0.1 --port 1830
```

Then test against it:
```bash
NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 \
.venv/bin/python scripts/test_netconf_conn.py
```

---

## Expected Outputs

### 1. Intent Parser Output

**File Created**: `generated_config.xml`

**Content** (formatted):
```xml
<campus-network xmlns="urn:example:campus-lan">
  <vlan>
    <id>10</id>
    <name>CS</name>
    <policy>internet_access</policy>
  </vlan>
  <vlan>
    <id>20</id>
    <name>ECE</name>
    <policy>internet_access</policy>
  </vlan>
  <vlan>
    <id>30</id>
    <name>ADMIN</name>
    <policy>restricted</policy>
  </vlan>
</campus-network>
```

### 2. NETCONF Push Output (Real Device Success)

```
[netconf_push] Starting NETCONF push...
🔌 [netconf_push] Connecting to NETCONF device 192.168.1.10:830 (timeout 10s) ...
📨 [netconf_push] Connected. Pushing configuration via edit-config ...
✅ [netconf_push] edit-config RPC reply:
<rpc-reply>...</rpc-reply>
✅ [netconf_push] Configuration pushed successfully (REAL device).
```

### 3. NETCONF Push Output (Auto-Fallback Simulation)

```
[netconf_push] Starting NETCONF push...
🔌 [netconf_push] Connecting to NETCONF device 192.168.1.10:830 (timeout 10s) ...
❌ [netconf_push] Real push failed: Could not open socket to 192.168.1.10:830
⚠️  [netconf_push] Falling back to SIMULATION mode.
   Simulating NETCONF push...
   Applying VLAN config: VLAN 10 -> CS
   Applying VLAN config: VLAN 20 -> ECE
   Applying VLAN config: VLAN 30 -> ADMIN
   Commit simulated.
✅ [netconf_push] Configuration push completed successfully (SIMULATED).
```

### 4. Prometheus Verification Output

```
[verify_prometheus] Connecting to Prometheus at http://localhost:9090 ...
[verify_prometheus] Connected to Prometheus.
[verify_prometheus] Querying: up  (# General scrape target up/down status)
[verify_prometheus] Result for up:
[{'metric': {'__name__': 'up', 'instance': 'localhost:9090', 'job': 'prometheus'}, 'value': [1762262136.517, '1']}, ...]
[verify_prometheus] Querying: node_network_up  (# Network interface up/down status)
[verify_prometheus] Result for node_network_up:
[{'metric': {'__name__': 'node_network_up', 'device': 'ens33', ...}, 'value': [1762262136.519, '1']}, ...]
[verify_prometheus] Verification complete.
```

### 5. NETCONF Connection Test Output (Success)

```
🔌 [test_netconf_conn] Connecting to 192.168.1.10:830 (timeout 10s) ...
✅ [test_netconf_conn] Connected. Server capabilities:
   - urn:ietf:params:netconf:base:1.0
   - urn:ietf:params:netconf:capability:writable-running:1.0
   - ...
```

---

## NETCONF Troubleshooting & Demo

### How `netconf_push.py` Works

1. **First Attempt**: Real NETCONF push via `ncclient`
   - Connects over SSH to specified host:port
   - Sends `edit-config` RPC with generated XML
   - On success → prints confirmation

2. **Automatic Fallback**: If real push fails
   - Catches any exception (socket error, SSH error, timeout)
   - Prints friendly error message
   - **Automatically** switches to simulation mode
   - Simulation parses XML and shows VLAN apply/commit steps
   - Always returns success (exit code 0)

**Why Auto-Fallback?**
- Ensures demos always run successfully
- Provides reproducible results for academic presentations
- Shows "what would happen" even without real devices

### Environment Variables

All NETCONF scripts support these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `NETCONF_HOST` | `192.168.1.10` | NETCONF device IP address |
| `NETCONF_PORT` | `830` | NETCONF SSH port (typically 830) |
| `NETCONF_USER` | `admin` | SSH username |
| `NETCONF_PASS` | `admin` | SSH password |
| `TIMEOUT` | `10` | Connection timeout in seconds |

**Usage Example:**
```bash
export NETCONF_HOST=10.0.0.5
export NETCONF_PORT=830
export NETCONF_USER=netadmin
export NETCONF_PASS=secret
python3 scripts/netconf_push.py
```

### Mock Server Usage

**Start Mock Server:**
```bash
python3 scripts/mock_netconf_server.py --host 127.0.0.1 --port 1830
```

**What It Does**:
- Listens on specified host:port
- Sends minimal NETCONF `<hello>` XML when client connects
- Logs incoming connections and data
- Closes connection after banner

**Limitations**:
- **TCP-only** (no SSH handshake)
- `ncclient` expects SSH and will fail against this mock
- Useful for: `nc -vz`, `telnet`, basic port connectivity tests

**For Full Testing**: Use real NETCONF-over-SSH servers:
- Vendor sandboxes (Cisco DevNet, Juniper vLabs)
- EVE-NG network emulator
- Docker NETCONF server images

### One-Copy Demo Commands

Run everything in sequence (copy-paste friendly):

```bash
# 1. Generate config
source .venv/bin/activate
python3 scripts/intent_parser.py

# 2. (Optional) Start mock server in background
python3 scripts/mock_netconf_server.py --host 127.0.0.1 --port 1830 &

# 3. Test connection (may fail with mock - that's expected)
NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 \
.venv/bin/python scripts/test_netconf_conn.py || true

# 4. Attempt push (auto-fallback to simulation on failure)
NETCONF_HOST=127.0.0.1 NETCONF_PORT=1830 \
NETCONF_USER=admin NETCONF_PASS=admin \
.venv/bin/python scripts/netconf_push.py

# 5. Verify via Prometheus (requires Prometheus running)
python3 scripts/verify_prometheus.py
```

---

## Troubleshooting

### Common Issues

#### 1. `generated_config.xml` Not Found

**Error:**
```
❌ [netconf_push] ERROR: generated_config.xml not found at ...
```

**Solution:**
```bash
python3 scripts/intent_parser.py
```

#### 2. `ncclient` Not Available

**Error:**
```
⚠️  [netconf_push] ncclient not available: No module named 'ncclient'
```

**Solution:**
```bash
source .venv/bin/activate
pip install ncclient
```

#### 3. Connection Failed / Could Not Open Socket

**Error:**
```
❌ [netconf_push] Real push failed: Could not open socket to ...
```

**Causes & Solutions**:
- **Device not running**: Start your NETCONF device/mock server
- **Wrong host/port**: Check with `ss -tuln | grep 830`
- **Firewall blocking**: Ensure port is open
- **Wrong credentials**: Verify `NETCONF_USER` and `NETCONF_PASS`

**Note**: This is expected if no device is available. The script will automatically fall back to simulation.

#### 4. Prometheus Connection Failed

**Error:**
```
[verify_prometheus] ERROR connecting to Prometheus: ...
```

**Solution:**
- Ensure Prometheus is running: `sudo systemctl status prometheus`
- Or start via Docker: `docker run -p 9090:9090 prom/prometheus`
- Check URL: http://localhost:9090

#### 5. Virtual Environment Not Activated

**Error:**
```
python3: command not found
```

**Solution:**
```bash
source .venv/bin/activate
# OR use venv Python directly
.venv/bin/python scripts/intent_parser.py
```

### Error-Reduction Tips

- ✅ Always run scripts from project root directory
- ✅ Use `.venv/bin/python` or activate venv first
- ✅ Check port availability: `ss -tuln | grep <port>`
- ✅ Use environment variables for overrides (don't edit source files)
- ✅ For vendor devices, ensure SSH/NETCONF is enabled
- ✅ Verify firewall rules allow NETCONF port (typically 830)

### Getting Help

1. **Check logs**: All scripts print detailed error messages
2. **Test connectivity**: Use `test_netconf_conn.py` first
3. **Verify setup**: Re-run `./setup_environment.sh`
4. **Check dependencies**: `pip list | grep -E "ncclient|prometheus"`

---

## Project Summary

This project successfully implements a complete **Intent-Based Networking** automation pipeline for campus LAN management. It demonstrates:

- ✅ Intent declaration and translation (JSON → YANG XML)
- ✅ Automated NETCONF deployment with intelligent fallback
- ✅ Prometheus-based verification and monitoring
- ✅ Production-ready error handling and logging
- ✅ Demo-friendly tools for reproducible results

**Key Innovation**: The automatic fallback simulation ensures that demos and academic presentations always succeed, even without access to real network devices, while maintaining clear logging that distinguishes between real and simulated operations.

---

## License & Credits

**Academic Project** - Intent-Based Networking for Campus LAN  
**Technologies**: YANG, NETCONF, Prometheus, Python  
**Purpose**: Demonstrate IBN automation workflow

---

**Last Updated**: 2025  
**Status**: ✅ Complete & Tested
