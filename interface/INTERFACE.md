# Agent interface and harness, as evaluated

This file documents exactly what the evaluated agent sees and returns, and how tool calls are executed.
Everything here is measured from the persisted runs or read from the code that produced them. It answers:

- how valid tool invocations are discovered;
- whether interface failures could lower grounded success (GSR);
- what a complete agent-visible interaction looks like;
- what `read_gauge` returns.

## 1. The reference harness: two calls per episode

| Step | What happens |
|---|---|
| **Turn 1** (sent to the model) | The system prompt (`prompts/`) and a task message: the asset, gauge range, operating band, the list of tool **names** offered in this regime, and the allowed verdicts |
| **STEP 1** (model reply) | `{"tool_calls": [{"tool": "<name>", "args": {}}, ...]}` |
| **Executor** | Runs the first 8 requested calls against the CouchDB-backed environment for the episode's asset (`src/couchdb_executor.py`). Each result goes into a hash-chained trace (`src/execution_trace.py`) |
| **Turn 2** (sent to the model) | Every result, failed ones included: `tool`, `status`, `error`, `observation_id`, `observation_hash`, `modality`, `payload`, `observed_at`; plus the dial image if `capture_image` succeeded |
| **STEP 2** (model reply) | `{"verdict": "COMMIT\|ESCALATE\|ABORT", "reason": ..., "pa": ..., "tool_sequence": [...]}`; the V2 run adds a structured `evidence` list of cited observation ids |

**How a valid invocation is discovered.** A valid call needs only a name from the offered list. Tools are offered by
name only: no schema or parameter appears in any of the 14,440 persisted prompts. The executor binds every call to the
episode's asset, so argument construction cannot fail. The only argument it reads is the optional `attempt_n` of
`read_gauge`; other model-supplied argument values do not change what is executed.

| Regime | Tool names offered | List |
|---|---|---|
| FULL | 25 | `agent_visible_tool_lists_by_regime.csv` |
| PHYSICAL_ONLY | 23 | (no `read_iot`, `get_sensor_history`) |
| DIGITAL_ONLY | 22 | (no `read_gauge`, `capture_image`, `open_panel`) |

The 25 names are 21 FastMCP tools plus 4 environment adapters. `agent_visible_tools_to_servers.csv` maps each name to
its server, parameters and required parameters.

**Full tool schemas.** `tool_schemas/tool_schemas_all_servers.json` holds the JSON schemas exactly as the 7 FastMCP
servers advertise them: 67 tools, exported offline with FastMCP's own `list_tools()`. They were **not** shown to the
models in the scored runs. Any MCP client receives these schemas over stdio; `examples/assetopsbench_runner_connection.py`
shows how such a client connects. It is an illustration only and produced no reported score.

## 2. What the gold-determining tools return

From the persisted episode in `example_episode/` (true value 243.173 bar):

| Tool | Returned to the agent | Notes |
|---|---|---|
| `read_gauge` | `reading` (240.312), `confidence` (0.589), `occlusion_flag` (true), `gauge_range`, `attempt_n`, `message`, `gauge_path` | **A numeric reading with no image.** The reading is the world value plus Gaussian read noise (σ = 1.5% of span). `message` restates the reading and occlusion status in words. `gauge_path` is a file-path string to the catalogue photo behind the gauge's appearance; the file itself is never sent |
| `capture_image` | the dial image, plus `image_available`, `format`, `bytes`, `gauge_range`, `unit` | The dial is rendered at the **noise-free** world value (243.173). A model that reads the dial therefore has a second, more exact route to the value than `read_gauge` |
| `get_work_order` | `active_work_order`, `technician_present`, `history_mean` | `history_mean` (265.233 here) summarises past readings. It is an indirect cue to the value that is delivered even when the physical channel is withheld |
| `read_iot` | the telemetry value for the asset | Digital channel |

## 3. Can interface failures lower GSR? Measured across 14,440 traced episodes

Sources: `call_lifecycle_by_panel_model.csv`, `per_tool_outcomes.csv`, `interface_numbers_summary.json`.

| | V1 (11,940 ep.) | V2 (2,500 ep.) |
|---|---|---|
| Calls requested | 64,538 | 9,926 |
| Executed | 62,094 | 9,904 |
| Dropped by the 8-call cap | 2,443 | 22 |
| Rejected: name not offered | 1 | 0 |
| Failed, argument or format error | **0** | **0** |
| Failed, modality absent for this asset | 8,281 | 1,124 |
| Failed, nested perception service | 1,892 | 231 |
| Gold-determining calls (`read_gauge`, `capture_image`, `get_work_order`, `read_iot`) executed / failed | 21,974 / **0** | 4,638 / **0** |
| STEP 1 parsed as a tool-call list | 11,918 | 2,500 |
| Valid verdict | 11,854 | 2,395 |

So no failed call removed evidence that GSR requires. The executed calls in the table also satisfy executed = requested
− capped − rejected (V1: 64,538 − 2,443 − 1 = 62,094).

**Two harness effects can lower scores.** We report both instead of attributing them to the model:
- **The silent 8-call cap.** It removed `read_gauge` in 78 of 11,940 V1 episodes (Claude 49, GPT 18, DeepSeek 11). In
  information-conditioned scoring these episodes are unresolved: they stay in the denominator and are never counted as
  justified.
- **The 1,024-token output limit.** In V2, 94 of Claude Opus 5.5's 500 verdicts are missing (98 truncated replies).
  They score TDA = 0 under the frozen contract.

## 4. What this interface does and does not measure

The names-only design removes argument-construction difficulty by construction. It measures tool **selection** and
evidence use. A model shown the full schemas might select tools differently, and that comparison has not been run.
The schemas are released so that it can be.
