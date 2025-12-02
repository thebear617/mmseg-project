# Git 基础工作流程

> 本文档记录 Git 版本控制的基础知识和日常使用流程，适合日常开发参考。

---

## 目录

- [1. 基本原则](#1-基本原则)
  - [1.1 项目结构说明](#11-项目结构说明)
  - [1.2 应该提交的内容](#12-应该提交的内容)
  - [1.3 不应该提交的内容](#13-不应该提交的内容)
- [2. 工作流程详解](#2-工作流程详解)
  - [2.1 Git 的三个区域](#21-git-的三个区域)
  - [2.2 步骤详解](#22-步骤详解)
  - [2.3 可视化流程](#23-可视化流程)
  - [2.4 补充说明](#24-补充说明)
- [3. 具体操作方法](#3-具体操作方法)
  - [3.1 检查 .gitignore 配置](#31-检查-gitignore-配置)
  - [3.2 标准提交流程](#32-标准提交流程)
  - [3.3 验证哪些文件会被提交](#33-验证哪些文件会被提交)
- [4. 项目版本控制管理策略](#4-项目版本控制管理策略)
  - [4.1 核心原则](#41-核心原则)
  - [4.2 日常版本控制工作流程](#42-日常版本控制工作流程)
  - [4.3 需要管理的更改类型](#43-需要管理的更改类型)
  - [4.4 检查清单](#44-检查清单)
  - [4.5 常见场景](#45-常见场景)

---

## 1. 基本原则

### 1.1 项目结构说明

**重要理解**: 在本项目中，你的所有实验工作都在 `experiments/` 目录下进行，因此：

1. **主要关注 `experiments/` 目录**: 
   - 你的所有实验配置、自定义代码、脚本都在这里
   - 这是你需要版本控制的主要内容
   - `mmsegmentation/` 是官方框架，通常不需要修改

2. **`mmsegmentation/` 目录**:
   - 这是官方 mmsegmentation 框架的源码
   - 除非需要修改框架本身，否则不需要关注其更改
   - 如果从官方仓库更新，直接拉取更新即可

3. **版本控制范围**:
   - ✅ **主要管理**: `experiments/` 目录下的所有更改
   - ⚠️ **次要关注**: `mmsegmentation/` 的更改（通常只是更新官方代码）
   - ❌ **不需要提交**: 实验结果、数据集、模型权重等大文件

### 1.2 应该提交的内容（experiments/ 目录下）

- ✅ 配置文件（`experiments/configs/`）
- ✅ 自定义代码（`experiments/custom/`）
- ✅ 训练/测试脚本（`experiments/scripts/`）
- ✅ 文档（`experiments/*.md`）
- ✅ `.gitignore` 文件（`experiments/.gitignore`）

### 1.3 不应该提交的内容

- ❌ 训练结果（`experiments/work_dirs/`）
- ❌ 数据集（`experiments/data/`）
- ❌ 模型权重（`experiments/checkpoints/`）
- ❌ 大文件（`*.pth`, `*.pkl`, `*.log`）

---

## 2. 工作流程详解

### 2.1 Git 的三个区域

Git 工作流程涉及三个主要区域：

```
工作区 (Working Directory)  →  暂存区 (Staging Area)  →  本地仓库 (Local Repository)  →  远程仓库 (Remote Repository)
     ↓                              ↓                           ↓                            ↓
   你编辑文件                    git add                    git commit                  git push
```

- **工作区**: 你实际编辑文件的地方
- **暂存区**: 准备提交的文件临时存放区
- **本地仓库**: 提交历史记录保存在本地
- **远程仓库**: GitHub/GitLab 等在线仓库

### 2.2 步骤详解

**步骤 1: 检查状态**
```bash
git status
```
- **作用**: 查看工作区有哪些文件被修改、新增或删除
- **输出**: 显示"未跟踪的文件"和"已修改但未暂存的文件"

**步骤 2-6: 添加到暂存区**
```bash
git add experiments/configs/      # 将 configs/ 目录的更改添加到暂存区
git add experiments/custom/       # 将 custom/ 目录的更改添加到暂存区
git add experiments/scripts/       # 将 scripts/ 目录的更改添加到暂存区
git add experiments/*.md           # 将 .md 文件的更改添加到暂存区
git add experiments/.gitignore     # 将 .gitignore 的更改添加到暂存区
```
- **作用**: 将工作区的更改"暂存"起来，准备提交
- **注意**: 
  - 这些步骤是**顺序执行**的（不是并行）
  - 可以多次执行，逐步添加文件
  - 也可以一次性添加：`git add experiments/`

**步骤 7: 创建提交**
```bash
git commit -m "Add experiment 001: test focal loss"
```
- **作用**:
  1. 将暂存区的所有更改打包成一个提交
  2. 记录提交信息（-m 后面的内容）
  3. 保存到本地仓库的历史记录中
  4. 清空暂存区（准备下一次提交）
- **注意**: 此时更改还在本地，还没有上传到远程

**步骤 8: 推送到远程仓库**
```bash
git push origin main
```
- **作用**:
  1. 将本地仓库的提交上传到远程仓库（如 GitHub）
  2. `origin` 是远程仓库的默认名称
  3. `main` 是分支名称
- **注意**: 只有执行这一步，远程仓库才会更新

### 2.3 可视化流程

```
┌─────────────────┐
│   工作区         │  你在这里编辑文件
│ (Working Dir)   │
└────────┬────────┘
         │ git add (步骤 2-6)
         ↓
┌─────────────────┐
│   暂存区         │  准备提交的文件
│ (Staging Area)  │
└────────┬────────┘
         │ git commit (步骤 7)
         ↓
┌─────────────────┐
│   本地仓库       │  提交历史记录
│ (Local Repo)    │
└────────┬────────┘
         │ git push (步骤 8)
         ↓
┌─────────────────┐
│   远程仓库       │  GitHub/GitLab 等
│ (Remote Repo)   │
└─────────────────┘
```

### 2.4 补充说明

**可以一次性添加所有文件**:
```bash
# 方法 1: 添加整个 experiments/ 目录（推荐）
git add experiments/

# 方法 2: 添加所有更改（包括其他目录，需谨慎）
git add .

# 方法 3: 交互式添加（可以选择性添加）
git add -p experiments/
```

**提交前可以检查**:
```bash
# 查看暂存区有哪些文件
git status

# 查看暂存区的具体更改内容
git diff --cached
```

**如果提交后发现错误**:
```bash
# 修改最后一次提交信息
git commit --amend -m "新的提交信息"

# 如果已经推送，需要强制推送（谨慎使用）
git push --force origin main
```

---

## 3. 具体操作方法

### 3.1 检查 .gitignore 配置

项目中的 `.gitignore` 文件应该包含：

```gitignore
# 忽略工作目录（包含训练结果、checkpoints等）
work_dirs/
*.pth
*.pkl
*.log
*.json

# 忽略数据集（通常很大，不应纳入版本控制）
data/
*.zip
*.tar
*.tar.gz

# 忽略预训练模型权重
checkpoints/pretrained/
checkpoints/custom/
```

### 3.2 标准提交流程

**标准工作流程**（主要针对 `experiments/` 目录）：

```bash
# 1. 检查 Git 状态（查看 experiments/ 目录的更改）
git status

# 2. 添加配置文件
git add experiments/configs/

# 3. 添加自定义代码
git add experiments/custom/

# 4. 添加训练/测试脚本
git add experiments/scripts/

# 5. 添加文档
git add experiments/*.md
git add experiments/*/README.md

# 6. 添加 .gitignore（如果修改了）
git add experiments/.gitignore

# 7. 提交（专注于 experiments/ 的更改）
git commit -m "Add experiment 001: test focal loss"

# 8. 推送到远程（如果需要）
git push origin main
```

**关于 `mmsegmentation/` 目录**:
- 如果只是从官方仓库更新代码，可以单独提交：
  ```bash
  git add mmsegmentation/
  git commit -m "Update mmsegmentation to latest version"
  ```
- 如果修改了框架代码（不常见），需要明确记录修改内容
- 大多数情况下，只需要关注 `experiments/` 目录的更改

### 3.3 验证哪些文件会被提交

```bash
# 查看暂存区的文件
git status

# 查看会被提交的文件列表
git diff --cached --name-only

# 查看哪些文件被忽略
git status --ignored

# 检查特定文件是否被忽略
git check-ignore -v experiments/work_dirs/exp_001/latest.pth
```

---

## 4. 项目版本控制管理策略

### 4.1 核心原则

**你的理解是正确的！** 在本项目中：

1. **主要工作区域**: `experiments/` 目录
   - 所有实验配置、自定义代码、脚本都在这里
   - 这是你需要版本控制的主要内容

2. **框架代码**: `mmsegmentation/` 目录
   - 这是官方框架，通常不需要修改
   - 如果从官方更新，可以单独提交
   - 大多数情况下不需要关注其更改

### 4.2 日常版本控制工作流程

**标准提交流程（推荐）**:

```bash
# 1. 查看 experiments/ 目录的更改
git status

# 2. 添加 experiments/ 下的更改
git add experiments/configs/      # 配置文件
git add experiments/custom/       # 自定义代码
git add experiments/scripts/      # 脚本
git add experiments/*.md           # 文档
git add experiments/.gitignore    # 忽略规则

# 3. 提交（专注于实验相关更改）
git commit -m "Add exp_002: test new loss function"

# 4. 推送到远程
git push origin main
```

**快速提交脚本**:

可以创建一个便捷脚本：

```bash
# 提交 experiments/ 目录的所有更改（排除被忽略的文件）
git add experiments/ && git commit -m "Update experiments"
```

### 4.3 需要管理的更改类型

**✅ 主要管理（experiments/ 目录）**

| 类型 | 路径 | 说明 |
|------|------|------|
| **配置文件** | `experiments/configs/` | 实验配置文件，必须提交 |
| **自定义代码** | `experiments/custom/` | 自定义模型、数据集等，必须提交 |
| **脚本** | `experiments/scripts/` | 训练/测试脚本，必须提交 |
| **文档** | `experiments/*.md` | 说明文档，建议提交 |
| **忽略规则** | `experiments/.gitignore` | 忽略规则，必须提交 |

**⚠️ 次要关注（mmsegmentation/ 目录）**

| 情况 | 操作 |
|------|------|
| **官方更新** | 可以单独提交：`git add mmsegmentation/ && git commit -m "Update mmsegmentation"` |
| **修改框架** | 需要明确记录修改内容和原因（不常见） |
| **日常开发** | 通常不需要关注，专注于 experiments/ |

**❌ 不需要提交**

- `experiments/work_dirs/` - 训练结果
- `experiments/data/` - 数据集
- `experiments/checkpoints/` - 模型权重
- 所有大文件（`.pth`, `.pkl`, `.log` 等）

### 4.4 检查清单

在每次提交前，确认：

- [ ] 只提交了 `experiments/` 目录下的相关文件
- [ ] 没有误提交大文件（`*.pth`, `*.pkl` 等）
- [ ] 没有提交训练结果（`work_dirs/`）
- [ ] 没有提交数据集（`data/`）
- [ ] 提交信息清晰描述了更改内容

### 4.5 常见场景

**场景 1: 创建新实验**

```bash
# 1. 创建实验配置
mkdir -p experiments/configs/exp_002
# ... 创建配置文件 ...

# 2. 提交
git add experiments/configs/exp_002/
git commit -m "Add exp_002: baseline experiment"
```

**场景 2: 添加自定义模块**

```bash
# 1. 创建自定义代码
# ... 在 experiments/custom/ 下添加代码 ...

# 2. 提交
git add experiments/custom/
git commit -m "Add custom backbone for exp_002"
```

**场景 3: 更新官方框架**

```bash
# 1. 从官方仓库更新（如果需要）
cd mmsegmentation
git pull origin main
cd ..

# 2. 提交更新（可选，通常不需要）
git add mmsegmentation/
git commit -m "Update mmsegmentation to latest version"
```

---

**相关文档**:
- [Git 高级用法](../notes/04_git_advanced.md) - 版本回溯、特殊情况处理等
- [故障排查指南](../notes/05_troubleshooting.md) - 常见问题解决方案

**最后更新**: 2024-12-02

