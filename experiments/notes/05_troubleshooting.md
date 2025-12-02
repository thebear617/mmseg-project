# 故障排查指南

> 本文档汇总开发过程中遇到的常见问题和解决方案，便于快速查找和解决问题。

---

## 目录

- [1. 环境相关问题](#1-环境相关问题)
  - [1.1 PYTHONPATH 相关问题](#11-pythonpath-相关问题)
  - [1.2 软链接相关问题](#12-软链接相关问题)
- [2. Git 相关问题](#2-git-相关问题)
  - [2.1 提交相关问题](#21-提交相关问题)
  - [2.2 版本回溯相关问题](#22-版本回溯相关问题)
  - [2.3 文件管理相关问题](#23-文件管理相关问题)
- [3. 项目配置相关问题](#3-项目配置相关问题)
  - [3.1 路径问题](#31-路径问题)
  - [3.2 模块导入问题](#32-模块导入问题)

---

## 1. 环境相关问题

### 1.1 PYTHONPATH 相关问题

#### 问题: 设置后仍然找不到模块

**现象**: 
```
ModuleNotFoundError: No module named 'custom'
```

**可能原因**:
1. 路径不正确
2. 未重新加载配置
3. 在错误的终端/环境中执行

**解决步骤**:
```bash
# 1. 检查路径是否正确
ls /path/to/mmseg-project/custom

# 2. 检查环境变量
echo $PYTHONPATH

# 3. 重新加载配置
source ~/.zshrc  # 或 source ~/.bashrc

# 4. 在新终端中测试
python -c "from custom.models import *; print('导入成功！')"
```

#### 问题: 多个项目需要不同的 PYTHONPATH

**解决**: 使用相对路径或在不同终端中临时设置
```bash
# 在项目根目录下临时设置
export PYTHONPATH=$PWD:$PYTHONPATH
```

#### 问题: conda 环境中设置不生效

**解决**: 确保在激活环境后设置，或使用 conda env config vars
```bash
# 方法 1: 在激活环境后设置
conda activate mmseg
export PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH

# 方法 2: 使用 conda env config vars（永久）
conda env config vars set PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH
conda deactivate
conda activate mmseg
```

### 1.2 软链接相关问题

#### 问题: 软链接指向不存在的位置

**现象**: 
```bash
ls -l experiments/data/cityscapes
# 输出: cityscapes -> /path/to/cityscapes (红色或显示 broken)
```

**解决**: 
```bash
# 1. 检查源路径是否存在
ls /path/to/cityscapes

# 2. 如果不存在，重新创建链接到正确位置
rm experiments/data/cityscapes
ln -s /correct/path/to/cityscapes experiments/data/cityscapes
```

#### 问题: 相对路径软链接失效

**现象**: 移动项目目录后，软链接失效

**解决**: 使用绝对路径创建软链接
```bash
# ❌ 不推荐：相对路径
ln -s ../datasets/cityscapes experiments/data/cityscapes

# ✅ 推荐：绝对路径
ln -s /absolute/path/to/cityscapes experiments/data/cityscapes
```

---

## 2. Git 相关问题

### 2.1 提交相关问题

#### 问题: 误提交了大文件

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
```

#### 问题: 不知道提交什么

**答案**: 主要关注 `experiments/` 目录，忽略 `mmsegmentation/` 的更改

**应该提交**:
- ✅ `experiments/configs/` - 配置文件
- ✅ `experiments/custom/` - 自定义代码
- ✅ `experiments/scripts/` - 脚本
- ✅ `experiments/*.md` - 文档

**不应该提交**:
- ❌ `experiments/work_dirs/` - 训练结果
- ❌ `experiments/data/` - 数据集
- ❌ `experiments/checkpoints/` - 模型权重

### 2.2 版本回溯相关问题

#### 问题: 需要回退版本

**解决**: 使用 `git log` 查看历史，`git reset` 回退
```bash
# 1. 查看提交历史
git log --oneline

# 2. 回退到目标提交
git reset --hard <commit-hash>

# 3. 如果已推送，强制推送（谨慎）
git push --force-with-lease origin main
```

#### 问题: 误删文件

**解决**: 使用 `git checkout <commit>^ -- <file>` 恢复
```bash
# 1. 查看文件删除的提交
git log --diff-filter=D --summary

# 2. 从历史中恢复文件
git checkout <commit-hash>^ -- <file-path>
# 例如: git checkout abc1234^ -- experiments/configs/exp_001/config.py
```

#### 问题: 撤销最后一次提交但保留更改

**解决**:
```bash
git reset --soft HEAD~1
# 修改文件后重新提交
git add .
git commit -m "修正后的提交信息"
```

### 2.3 文件管理相关问题

#### 问题: 配置文件路径问题

**现象**: 配置文件包含绝对路径，不便于分享

**解决**: 使用相对路径或环境变量
```python
# ❌ 不推荐：绝对路径
work_dir = '/Users/mkc/.../experiments/work_dirs/exp_001'

# ✅ 推荐：相对路径
work_dir = 'experiments/work_dirs/exp_001'

# ✅ 推荐：环境变量
import os
data_root = os.getenv('DATASET_ROOT', 'experiments/data/cityscapes')
```

---

## 3. 项目配置相关问题

### 3.1 路径问题

#### 问题: 配置文件中的路径在不同机器上不工作

**解决**: 
1. 使用相对路径（推荐）
2. 使用环境变量
3. 使用软链接统一管理数据集路径

### 3.2 模块导入问题

#### 问题: 找不到自定义模块

**可能原因**:
1. PYTHONPATH 未设置
2. 模块未正确注册
3. 路径不正确

**解决步骤**:
```bash
# 1. 检查 PYTHONPATH
echo $PYTHONPATH

# 2. 检查模块文件是否存在
ls experiments/custom/models/backbones/

# 3. 检查 __init__.py 是否存在
ls experiments/custom/__init__.py

# 4. 测试导入
python -c "from custom.models import *; print('导入成功！')"
```

---

## 快速参考

### 常用命令速查

| 问题 | 命令 |
|------|------|
| **找不到自定义模块** | 检查 PYTHONPATH: `echo $PYTHONPATH` |
| **软链接失效** | 检查源路径: `readlink -f experiments/data/cityscapes` |
| **误提交大文件** | 移除: `git rm --cached file` |
| **需要回退版本** | 查看历史: `git log --oneline`，回退: `git reset HEAD~1` |
| **误删文件** | 恢复: `git checkout <commit>^ -- <file>` |

### 问题分类索引

- **环境问题** → 查看 [环境相关问题](#1-环境相关问题)
- **Git 提交问题** → 查看 [提交相关问题](#21-提交相关问题)
- **版本回溯问题** → 查看 [版本回溯相关问题](#22-版本回溯相关问题)
- **路径问题** → 查看 [路径问题](#31-路径问题)
- **模块导入问题** → 查看 [模块导入问题](#32-模块导入问题)

---

**相关文档**:
- [环境设置指南](../notes/02_environment_setup.md)
- [Git 基础工作流程](../notes/03_git_basics.md)
- [Git 高级用法](../notes/04_git_advanced.md)

**最后更新**: 2024-12-02

