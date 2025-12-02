# Agent 上下文文档

> **重要**: 本文档是新 Agent 启动时的必读文档，用于快速了解项目状态、组织方式、风格规范和重要决策。
> 
> **更新原则**: 当项目发生重要变更时，Agent 应该更新本文档（参考 `experiments/notes/01_how_to_maintain_context.md`）。

---

## 📋 快速导航

- [项目概述](#项目概述)
- [目录组织规范](#目录组织规范)
- [重要决策记录](#重要决策记录)
- [风格指南](#风格指南)
- [用户偏好](#用户偏好)
- [变更历史](#变更历史)
- [快速参考](#快速参考)

---

## 项目概述

### 项目目的

本项目是基于 mmsegmentation 官方框架的语义分割研究项目，主要用于：
- 进行语义分割相关的实验研究
- 测试和开发新的模型架构
- 管理实验配置和结果

### 项目结构

```
mmseg-project/
├── AGENT_CONTEXT.md          # 本文件：Agent上下文文档
├── README.md                 # 项目说明
├── mmsegmentation/          # 官方mmsegmentation框架源码
│   ├── configs/             # 官方配置文件
│   ├── mmseg/               # 框架核心代码
│   └── tools/               # 训练/测试工具
└── experiments/             # 实验工作目录（主要工作区域）
    ├── configs/             # 实验配置文件
    ├── custom/              # 自定义代码模块
    ├── data/                # 数据集（软链接）
    ├── checkpoints/         # 预训练模型权重
    ├── work_dirs/           # 实验结果输出
    ├── scripts/             # 训练/测试脚本
    └── notes/               # 开发笔记
```

### 核心原则

1. **主要工作区域**: `experiments/` 目录
   - 所有实验配置、自定义代码、脚本都在这里
   - 这是版本控制的主要内容

2. **框架代码**: `mmsegmentation/` 目录
   - 官方框架，通常不需要修改
   - 如果从官方更新，可以单独提交

3. **版本控制**: 主要管理 `experiments/` 目录，忽略 `work_dirs/`、`data/`、`checkpoints/`

---

## 目录组织规范

### experiments/ 目录结构

```
experiments/
├── configs/                  # 配置文件
│   ├── _base_/              # 基础配置（共享）
│   └── exp_XXX/             # 具体实验配置
├── custom/                   # 自定义代码
│   ├── datasets/            # 自定义数据集
│   ├── models/              # 自定义模型组件
│   └── utils/               # 自定义工具
├── data/                     # 数据集（使用软链接）
├── checkpoints/              # 预训练模型权重
├── work_dirs/               # 实验结果（不提交到Git）
├── scripts/                  # 训练/测试脚本
└── notes/                    # 开发笔记
```

### 文件命名规范

- **实验配置**: `exp_XXX/`（XXX为实验编号，如001、002）
- **笔记文件**: `NN_主题名.md`（NN为两位数字，从00开始）
- **脚本文件**: `操作_实验编号.sh`（如 `train_exp_001.sh`）

### 实验编号规范

- `exp_001`, `exp_002`: 常规实验
- `exp_baseline`: 基线实验
- `exp_ablation_001`: 消融实验

---

## 重要决策记录

### 决策1: 实验目录独立组织

**时间**: 2024-12-02  
**决策**: 创建独立的 `experiments/` 目录，与官方框架 `mmsegmentation/` 分离

**原因**:
- 保持官方框架代码的纯净性
- 便于实验管理和版本控制
- 符合研究项目的组织习惯

**影响**: 所有实验相关的工作都在 `experiments/` 目录下进行

### 决策2: 笔记文件主题分类

**时间**: 2024-12-02  
**决策**: 将笔记按主题拆分为多个文件（01-05），而非单一文件

**原因**:
- 便于查找和维护
- 文件大小合理（300-400行）
- 符合使用频率（日常使用 vs 按需查阅）

**文件组织**:
- `00_how_to_add_notes.md`: AI参考文档
- `01_how_to_maintain_context.md`: Agent上下文维护指南
- `02_environment_setup.md`: 环境设置
- `03_git_basics.md`: Git基础（日常使用）
- `04_git_advanced.md`: Git高级（按需查阅）
- `05_troubleshooting.md`: 故障排查

### 决策3: Git版本控制策略

**时间**: 2024-12-02  
**决策**: 主要管理 `experiments/` 目录，忽略 `mmsegmentation/` 的更改

**原因**:
- 用户的所有工作都在 `experiments/` 目录
- `mmsegmentation/` 是官方框架，通常不需要修改
- 避免提交不必要的大文件

**实践**:
- ✅ 提交: `experiments/configs/`, `experiments/custom/`, `experiments/scripts/`
- ❌ 不提交: `experiments/work_dirs/`, `experiments/data/`, `experiments/checkpoints/`

### 决策4: Agent上下文传递机制

**时间**: 2024-12-02  
**决策**: 创建 `AGENT_CONTEXT.md` 和 `notes/01_how_to_maintain_context.md`

**原因**:
- 实现Agent间的无痛接力
- 新Agent能快速了解项目状态和风格
- 保持项目记忆的连续性

**机制**:
- 新Agent启动时读取 `AGENT_CONTEXT.md`
- Agent完成重要修改后更新 `AGENT_CONTEXT.md`（追加模式）
- 定期整理，删除过时内容

---

## 风格指南

### 代码风格

- **Python**: 遵循 PEP 8，使用4空格缩进
- **配置文件**: 使用 mmsegmentation 的配置格式
- **注释**: 中文注释，关键部分添加详细说明

### 文档风格

- **Markdown格式**: 使用标准Markdown语法
- **标题层级**: 使用 `##` 作为一级标题，`###` 作为二级标题
- **代码块**: 使用三个反引号，标注语言类型
- **表格**: 使用Markdown表格格式
- **目录**: 每个长文档开头包含目录（使用Markdown链接）

### 命名规范

- **文件**: 小写字母，下划线分隔（`exp_001_config.py`）
- **目录**: 小写字母，下划线分隔（`exp_001/`）
- **变量**: 小写字母，下划线分隔（`data_root`）
- **类名**: 驼峰命名（`MyBackbone`）

### 提交信息规范

**格式**: `操作类型: 简短描述`

**示例**:
- `Add exp_002: test focal loss`
- `Fix: correct learning rate in exp_001 config`
- `Update: add custom backbone for exp_003`

**操作类型**:
- `Add`: 新增内容
- `Fix`: 修复问题
- `Update`: 更新内容
- `Refactor`: 重构代码
- `Docs`: 文档更新

---

## 用户偏好

### 工作习惯

1. **主要关注**: `experiments/` 目录下的工作
2. **版本控制**: 主要提交 `experiments/` 目录的更改
3. **实验管理**: 使用编号管理实验（exp_001, exp_002...）
4. **笔记组织**: 按主题分类，便于查找

### 沟通偏好

1. **语言**: 使用中文简体
2. **详细程度**: 需要详细解释和示例
3. **文档**: 偏好结构清晰、有目录的文档
4. **反馈**: 希望了解操作原理，不只是命令

### 技术偏好

1. **环境变量**: 使用永久设置（~/.zshrc）
2. **数据集管理**: 使用软链接而非复制
3. **路径管理**: 使用相对路径，便于分享
4. **Git操作**: 主要使用基础命令，高级功能按需学习

---

## 变更历史

### 2024-12-02: 项目初始化

**主要变更**:
- 创建 `experiments/` 目录结构
- 建立实验配置和自定义代码组织方式
- 创建开发笔记系统（notes/）
- 建立Git版本控制策略

**重要文件**:
- `experiments/README.md`: 实验目录说明
- `experiments/QUICKSTART.md`: 快速开始指南
- `experiments/.gitignore`: 忽略规则配置

### 2024-12-02: 笔记系统优化

**主要变更**:
- 将单一笔记文件拆分为主题分类（01-05）
- 创建AI参考文档（`00_how_to_add_notes.md`）
- 建立笔记添加和维护规范

**文件变更**:
- 创建: `00_how_to_add_notes.md`, `01_how_to_maintain_context.md`
- 拆分: `development_basics.md` → `02_environment_setup.md`, `03_git_basics.md`, `04_git_advanced.md`, `05_troubleshooting.md`

### 2024-12-02: Agent上下文机制建立

**主要变更**:
- 创建 `AGENT_CONTEXT.md`（本文件）
- 建立Agent上下文传递机制
- 制定上下文维护规范

**目的**: 实现Agent间的无痛接力，保持项目记忆连续性

---

## 快速参考

### 关键文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| **Agent上下文** | `AGENT_CONTEXT.md` | 新Agent必读 |
| **实验说明** | `experiments/README.md` | 实验目录说明 |
| **快速开始** | `experiments/QUICKSTART.md` | 快速上手指南 |
| **笔记索引** | `experiments/notes/README.md` | 笔记目录索引 |
| **笔记添加规则** | `experiments/notes/00_how_to_add_notes.md` | AI参考文档 |
| **上下文维护** | `experiments/notes/01_how_to_maintain_context.md` | 上下文维护指南 |

### 常用操作

**添加笔记**:
```
添加笔记到 experiments/notes/：
标题：[标题]
内容：[内容]
分类：[环境/Git基础/Git高级/故障排查/其他]
要求：参考 experiments/notes/00_how_to_add_notes.md 中的规则
```

**提交代码**:
```bash
git add experiments/configs/
git add experiments/custom/
git commit -m "Add exp_XXX: description"
git push origin main
```

**创建新实验**:
```bash
mkdir -p experiments/configs/exp_XXX
# 创建配置文件...
git add experiments/configs/exp_XXX/
git commit -m "Add exp_XXX: description"
```

### 重要约定

1. **工作区域**: `experiments/` 目录
2. **版本控制**: 主要管理 `experiments/`，忽略 `work_dirs/`、`data/`、`checkpoints/`
3. **文件大小**: 笔记文件不超过500行
4. **文档格式**: Markdown，包含目录
5. **提交信息**: 使用规范格式 `操作类型: 描述`

---

## 🔄 更新说明

本文档采用**追加模式**更新：

- **追加新内容**: 在"变更历史"部分追加新的变更记录
- **更新现有内容**: 直接修改对应章节
- **定期整理**: 当文件过大时（>1000行），整理并删除过时内容

**更新时机**:
- 项目结构发生重大变化时
- 重要决策或约定改变时
- 用户偏好发生变化时
- Agent完成重要修改后

**更新方法**: 参考 `experiments/notes/01_how_to_maintain_context.md`

---

**最后更新**: 2024-12-02  
**维护者**: Agent团队  
**版本**: 1.0

