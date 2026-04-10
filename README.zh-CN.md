<!-- language-switch:start -->
[English](./README.md) | [中文](./README.zh-CN.md)
<!-- language-switch:end -->

fdo 内核 mvk

最小确定性执行内核（原型）

fdo-kernel-mvk 是 Digital Biosphere Architecture 的 execution-integrity layer repository。它聚焦于 deterministic execution、replay validation 和 runtime truth surfaces。它是 layer repo，不是整个 stack。

## Role

`fdo-kernel-mvk` 是 Digital Biosphere Architecture 的 execution-integrity layer repository。

它聚焦于 deterministic execution、replay validation 和 runtime truth surfaces。

它是 layer repo，不是整个 stack。

## Not this repo

- not the governance runtime
- not the audit control plane
- not the architecture hub
- not the evidence packaging toolkit
- not the benchmark suite

## Start here

- [docs/walkthrough.md](docs/walkthrough.md)
- [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- [token-governor](https://github.com/joy7758/token-governor)
- [agent-evidence](https://github.com/joy7758/agent-evidence)
- [aro-audit](https://github.com/joy7758/aro-audit)

## Depends on / Architecture navigation

- Digital Biosphere Architecture provides the system context.
- Token Governor is the governance layer.
- Agent Evidence is the concrete evidence packaging entry.
- ARO-Audit is the post-execution review layer.
- Verifiable Agent Demo is the shortest walkthrough across adjacent layers.

## Commands

- `make run` -> `EXECUTION_OK`
- `make replay` -> `REPLAY_PASS`
- `make tamper` -> `CONFORMANCE_FAIL`

## 架构背景

该仓库是[数字生物圈架构](https://github.com/joy7758/digital-biosphere-architecture)生态系统的一部分。
它贡献执行完整性层，而不是试图成为整个堆栈。
它的重点是执行真相、验证表面和运行时完整性。

它证明了什么：
- 确定性状态演化
- 规范对象校验和验证
- 跟踪绑定重放验证

安全说明：
- 该原型当前使用 SHA-256 校验和进行篡改检测。
- 校验和提供完整性检查，而不是身份绑定的数字签名。

## AI 智能体堆栈架构

该仓库还探讨了执行完整性在更广泛的AI 智能体堆栈中的适用范围。

看：
- [AI 智能体架构图](docs/architecture/agent-architecture-map.md)
- [AI智能体运行时和安全堆栈](docs/architecture/agent-runtime-stack.md)
- [AI 智能体堆栈架构](docs/architecture/ai-agent-stack-architecture.md)
- [AI 智能体安全架构](docs/architecture/ai-agent-security-architecture.md)
- [AI 智能体运行时OSI模型](docs/architecture/agent-runtime-osi.md)

```mermaid
flowchart TB
    A["Application Layer<br>AI Apps / Copilots / Workflows"] --> B["Agent Framework Layer<br>LangGraph / CrewAI / AutoGen"]
    B --> C["Identity Layer<br>Persona Objects (POP)"]
    C --> D["Execution Integrity Layer<br>MVK Kernel<br>Deterministic Action Logs"]
    D --> E["Governance Layer<br>Policy / Verification / Audit"]
    E --> F["Object Layer<br>FDO / Digital Objects"]
    F --> G["Infrastructure<br>Models / Compute / Storage"]
```

核心层：
- 应用
- 代理框架
- 身份
- 执行完整性
- 治理
- 对象层
- 基础设施

主要区别：
- 治理决定应该允许什么。
- 执行完整性证明了实际发生的情况。

## 执照

麻省理工学院

## 架构注释

- [证据→推论→行动](docs/schema-notes/evidence-inference-action.md)

## 架构笔记

- [执行完整性与治理运行时](docs/architecture/execution-integrity-vs-governance-runtime.md)

## 路线图注释

- [成功端执行跟踪](docs/roadmap-notes/success-side-execution-traces.md)
