# Git 高级用法

> 本文档记录 Git 的高级功能和特殊场景处理，包括版本回溯、特殊情况处理、最佳实践等。

---

## 目录

- [1. 特殊情况处理](#1-特殊情况处理)
  - [1.1 误提交了大文件](#11-误提交了大文件)
  - [1.2 需要分享小文件结果](#12-需要分享小文件结果)
  - [1.3 使用 Git LFS 管理大文件](#13-使用-git-lfs-管理大文件)
  - [1.4 配置文件中的路径问题](#14-配置文件中的路径问题)
- [2. 版本回溯](#2-版本回溯)
  - [2.1 核心概念](#21-核心概念)
  - [2.2 本地版本回溯](#22-本地版本回溯)
  - [2.3 远程版本回溯](#23-远程版本回溯)
  - [2.4 常用回溯场景](#24-常用回溯场景)
  - [2.5 版本回溯最佳实践](#25-版本回溯最佳实践)
- [3. 最佳实践](#3-最佳实践)
  - [3.1 提交前检查清单](#31-提交前检查清单)
  - [3.2 提交信息规范](#32-提交信息规范)
  - [3.3 分支管理建议](#33-分支管理建议)
  - [3.4 定期备份](#34-定期备份)
  - [3.5 分享实验结果](#35-分享实验结果)

---

## 1. 特殊情况处理

### 1.1 误提交了大文件

**问题**: 不小心将大文件添加到了 Git

**解决步骤**:

```bash
# 1. 从暂存区移除（但保留本地文件）
git rm --cached experiments/work_dirs/exp_001/latest.pth

# 2. 确保 .gitignore 包含该文件模式
# 检查 .gitignore 中是否有 *.pth

# 3. 提交删除操作
git commit -m "Remove large files from tracking"

# 4. 如果已经推送到远程，需要强制推送（谨慎使用）
git push origin main
# 注意：如果其他人已经拉取了，需要通知他们
```

**从 Git 历史中完全删除大文件**（如果已经提交到历史）:

```bash
# 使用 git filter-branch（不推荐，复杂）
# 或使用 git filter-repo（推荐，需要安装）

# 安装 git-filter-repo
pip install git-filter-repo

# 删除历史中的大文件
git filter-repo --path experiments/work_dirs/exp_001/latest.pth --invert-paths

# 强制推送（会重写历史，谨慎使用）
git push origin main --force
```

### 1.2 需要分享小文件结果

**场景**: 需要分享配置文件副本或结果摘要

**方法 1: 复制到配置目录**（推荐）
```bash
# 复制配置文件到配置目录
cp experiments/work_dirs/exp_001/config.py \
   experiments/configs/exp_001/used_config.py

# 提交
git add experiments/configs/exp_001/used_config.py
git commit -m "Add used config for exp_001"
```

**方法 2: 创建结果摘要**
```bash
# 创建结果摘要文件
cat > experiments/configs/exp_001/results_summary.txt << EOF
实验 001 结果摘要
mIoU: 72.5%
训练时间: 8小时
最佳 checkpoint: iter_40000.pth
EOF

# 提交
git add experiments/configs/exp_001/results_summary.txt
git commit -m "Add results summary for exp_001"
```

### 1.3 使用 Git LFS 管理大文件

**场景**: 如果确实需要版本控制某些大文件（如预训练模型）

**步骤**:

```bash
# 1. 安装 Git LFS
# macOS
brew install git-lfs

# Linux
# 参考: https://git-lfs.github.com/

# 2. 初始化 Git LFS
git lfs install

# 3. 跟踪大文件类型
git lfs track "*.pth"
git lfs track "*.pkl"
git lfs track "*.h5"

# 4. 提交 .gitattributes 文件
git add .gitattributes
git commit -m "Add Git LFS tracking for large files"

# 5. 正常添加和提交大文件
git add experiments/checkpoints/pretrained/model.pth
git commit -m "Add pretrained model"
git push origin main
```

**注意**: Git LFS 需要额外的存储空间和配置，通常不推荐用于实验项目。

### 1.4 配置文件中的路径问题

**问题**: 配置文件包含绝对路径，不便于分享

**解决**: 使用相对路径或环境变量

```python
# ❌ 不推荐：绝对路径
work_dir = '/Users/mkc/Documents/研一上/Research/mmseg-project/experiments/work_dirs/exp_001'
data_root = '/Users/mkc/Documents/datasets/cityscapes'

# ✅ 推荐：相对路径
work_dir = 'experiments/work_dirs/exp_001'
data_root = 'experiments/data/cityscapes'

# ✅ 推荐：环境变量
import os
data_root = os.getenv('DATASET_ROOT', 'experiments/data/cityscapes')
```

---

## 2. 版本回溯

### 2.1 核心概念

**是的，你可以在本地仓库提交历史记录后实现版本回溯！**

当你执行 `git commit` 后，所有更改都保存在本地仓库的历史记录中。你可以随时回溯到任何历史版本，无论是否推送到远程。

### 2.2 本地版本回溯

**查看提交历史**:
```bash
# 查看提交历史（简洁版）
git log --oneline

# 查看提交历史（详细版）
git log

# 查看最近 5 次提交
git log -5

# 查看图形化历史
git log --graph --oneline --all
```

**回溯到特定提交**:
```bash
# 方法 1: 查看特定提交（不修改工作区）
git show <commit-hash>
# 例如: git show abc1234

# 方法 2: 临时切换到某个提交（查看历史版本）
git checkout <commit-hash>
# 注意：这会使你处于"分离头指针"状态，查看完后记得切换回来
git checkout main  # 切换回主分支

# 方法 3: 创建新分支从某个提交开始（推荐）
git checkout -b new-branch <commit-hash>
```

**撤销更改**:

```bash
# 撤销工作区的更改（未 add 的）
git restore <file>
# 或
git checkout -- <file>

# 撤销暂存区的更改（已 add 但未 commit 的）
git restore --staged <file>
# 或
git reset HEAD <file>

# 撤销最后一次提交（保留更改在暂存区）
git reset --soft HEAD~1

# 撤销最后一次提交（保留更改在工作区）
git reset --mixed HEAD~1
# 或
git reset HEAD~1

# 撤销最后一次提交（完全删除更改，谨慎使用）
git reset --hard HEAD~1
```

**回退到特定提交**:
```bash
# 回退到指定提交（保留更改在工作区）
git reset <commit-hash>

# 回退到指定提交（完全删除更改，谨慎使用）
git reset --hard <commit-hash>

# 回退到上一个提交
git reset HEAD~1

# 回退到上 N 个提交
git reset HEAD~N
```

### 2.3 远程版本回溯

**如果已经推送到远程，需要额外操作**:

```bash
# 1. 本地回退（如上所述）
git reset --hard <commit-hash>

# 2. 强制推送到远程（会覆盖远程历史，谨慎使用）
git push --force origin main
# 或使用更安全的选项
git push --force-with-lease origin main
```

**警告**: 
- `--force` 会覆盖远程历史，如果其他人也在使用这个仓库，可能会造成问题
- 建议使用 `--force-with-lease`，更安全
- 如果多人协作，最好先沟通

**恢复远程的特定版本**:
```bash
# 1. 查看远程提交历史
git log origin/main --oneline

# 2. 创建新分支指向远程的某个提交
git checkout -b restore-branch origin/main~5

# 3. 如果需要，可以合并回主分支
git checkout main
git merge restore-branch
```

### 2.4 常用回溯场景

**场景 1: 撤销最后一次提交但保留更改**
```bash
git reset --soft HEAD~1
# 修改文件后重新提交
git add .
git commit -m "修正后的提交信息"
```

**场景 2: 完全回退到某个提交**
```bash
# 查看历史找到目标提交
git log --oneline

# 回退到目标提交（例如: abc1234）
git reset --hard abc1234

# 如果已推送，强制推送（谨慎）
git push --force-with-lease origin main
```

**场景 3: 查看历史版本但不修改当前版本**
```bash
# 查看特定提交的内容
git show <commit-hash>

# 查看特定文件的历史版本
git show <commit-hash>:<file-path>

# 临时切换到历史版本查看
git checkout <commit-hash>
# 查看完后切换回来
git checkout main
```

**场景 4: 恢复被删除的文件**
```bash
# 查看文件删除的提交
git log --diff-filter=D --summary

# 从历史中恢复文件
git checkout <commit-hash>^ -- <file-path>
# 例如: git checkout abc1234^ -- experiments/configs/exp_001/config.py
```

### 2.5 版本回溯最佳实践

1. **提交前检查**: 使用 `git status` 和 `git diff` 确认更改
2. **重要提交前备份**: 对重要更改创建分支备份
3. **谨慎使用 --hard**: `git reset --hard` 会永久删除更改
4. **协作时沟通**: 如果已推送，回退前先与团队沟通
5. **使用分支**: 在分支上实验，确认无误后再合并到主分支

---

## 3. 最佳实践

### 3.1 提交前检查清单

```bash
# ✅ 检查暂存区文件大小
git diff --cached --stat

# ✅ 检查是否有大文件
git diff --cached --name-only | xargs ls -lh

# ✅ 检查 .gitignore 是否生效
git status --ignored

# ✅ 查看提交内容
git diff --cached
```

### 3.2 提交信息规范

```bash
# ✅ 好的提交信息
git commit -m "Add exp_001: test focal loss on Cityscapes"
git commit -m "Fix: correct learning rate in exp_002 config"
git commit -m "Update: add custom backbone for exp_003"

# ❌ 不好的提交信息
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### 3.3 分支管理建议

```bash
# 创建功能分支
git checkout -b feature/exp_001

# 在分支上开发
# ... 进行修改和提交 ...

# 合并到主分支
git checkout main
git merge feature/exp_001

# 删除功能分支
git branch -d feature/exp_001
```

### 3.4 定期备份

虽然不提交到 Git，但重要结果应该备份：

```bash
# 备份到外部存储
tar -czf exp_001_backup.tar.gz experiments/work_dirs/exp_001/

# 或使用 rsync 同步到服务器
rsync -av experiments/work_dirs/exp_001/ user@server:/backup/exp_001/
```

### 3.5 分享实验结果

**方法 1: 云存储**
- 上传到 Google Drive / 百度网盘
- 在 README 中提供下载链接

**方法 2: 实验管理平台**
- Weights & Biases (wandb)
- TensorBoard
- MLflow

**方法 3: 结果摘要**
- 在实验 README 中记录关键指标
- 创建结果对比表格

---

**相关文档**:
- [Git 基础工作流程](../notes/02_git_basics.md) - 日常使用流程
- [故障排查指南](../notes/04_troubleshooting.md) - 常见问题解决方案

**最后更新**: 2024-12-02

