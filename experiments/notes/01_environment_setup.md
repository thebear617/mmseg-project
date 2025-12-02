# 环境设置指南

> 本文档记录项目环境设置相关的基础知识，包括环境变量配置和软链接使用。

---

## 目录

- [1. 环境变量 PYTHONPATH](#1-环境变量-pythonpath)
  - [1.1 什么是 PYTHONPATH](#11-什么是-pythonpath)
  - [1.2 为什么需要设置 PYTHONPATH](#12-为什么需要设置-pythonpath)
  - [1.3 永久设置方法](#13-永久设置方法)
  - [1.4 验证和故障排查](#14-验证和故障排查)
- [2. 软链接（Symbolic Link）](#2-软链接symbolic-link)
  - [2.1 什么是软链接](#21-什么是软链接)
  - [2.2 为什么使用软链接](#22-为什么使用软链接)
  - [2.3 基本操作](#23-基本操作)
  - [2.4 常见问题](#24-常见问题)

---

## 1. 环境变量 PYTHONPATH

### 1.1 什么是 PYTHONPATH

`PYTHONPATH` 是一个环境变量，用于指定 Python 解释器搜索模块的路径。当 Python 导入模块时，会按照以下顺序搜索：

1. 当前目录
2. `PYTHONPATH` 中指定的目录
3. Python 标准库目录
4. site-packages 目录（第三方包安装位置）

### 1.2 为什么需要设置 PYTHONPATH

在 mmsegmentation 项目中，我们经常需要导入自定义模块：

```python
# 在配置文件中
custom_imports = dict(
    imports=['custom.models.backbones.my_backbone'],
    allow_failed_imports=False
)
```

如果不设置 `PYTHONPATH`，Python 无法找到 `custom` 包，会报错：
```
ModuleNotFoundError: No module named 'custom'
```

### 1.3 永久设置方法

#### 方法 1: 编辑 ~/.zshrc（推荐，macOS/Linux）

1. **打开配置文件**:
   ```bash
   # 使用 nano 编辑器（简单易用）
   nano ~/.zshrc
   
   # 或使用 vim 编辑器
   vim ~/.zshrc
   
   # 或使用 VS Code
   code ~/.zshrc
   ```

2. **添加环境变量**:
   在文件末尾添加以下内容（使用你的实际项目路径）：
   ```bash
   # mmsegmentation 项目路径
   export PYTHONPATH=/Users/mkc/Documents/研一上/Research/mmseg-project:$PYTHONPATH
   ```
   
   **注意**: 
   - 使用绝对路径更可靠
   - 多个路径用冒号 `:` 分隔
   - `$PYTHONPATH` 保留原有路径，避免覆盖

3. **保存并重新加载**:
   ```bash
   # 如果使用 nano: Ctrl+O 保存, Ctrl+X 退出
   # 如果使用 vim: 按 Esc, 输入 :wq 保存退出
   
   # 重新加载配置
   source ~/.zshrc
   ```

#### 方法 2: 编辑 ~/.bashrc（Linux，如果使用 bash）

```bash
# 打开文件
nano ~/.bashrc

# 添加内容（同上）
export PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH

# 重新加载
source ~/.bashrc
```

#### 方法 3: 编辑 ~/.bash_profile（macOS，如果使用 bash）

```bash
# 打开文件
nano ~/.bash_profile

# 添加内容
export PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH

# 重新加载
source ~/.bash_profile
```

#### 方法 4: 使用 conda 环境（推荐用于 conda 用户）

如果使用 conda 管理环境，可以在激活环境时自动设置：

```bash
# 激活环境
conda activate mmseg

# 设置环境变量（仅当前环境）
conda env config vars set PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH

# 重新激活环境使设置生效
conda deactivate
conda activate mmseg
```

### 1.4 验证和故障排查

#### 验证设置是否生效

```bash
# 方法 1: 检查环境变量
echo $PYTHONPATH
# 应该输出: /path/to/mmseg-project:...

# 方法 2: 在 Python 中检查
python -c "import sys; print('\n'.join(sys.path))"
# 应该能看到你的项目路径

# 方法 3: 测试导入自定义模块
python -c "from custom.models import *; print('导入成功！')"
```

#### 常见问题

**问题 1: 设置后仍然找不到模块**

- **原因**: 可能路径不正确，或未重新加载配置
- **解决**: 
  ```bash
  # 检查路径是否正确
  ls /path/to/mmseg-project/custom
  
  # 重新加载配置
  source ~/.zshrc
  
  # 在新终端中测试
  ```

**问题 2: 多个项目需要不同的 PYTHONPATH**

- **解决**: 使用相对路径或在不同终端中临时设置
  ```bash
  # 在项目根目录下临时设置
  export PYTHONPATH=$PWD:$PYTHONPATH
  ```

**问题 3: conda 环境中设置不生效**

- **解决**: 确保在激活环境后设置，或使用 conda env config vars

---

## 2. 软链接（Symbolic Link）

### 2.1 什么是软链接

软链接（Symbolic Link，也叫符号链接）是一个特殊的文件，它指向另一个文件或目录的路径。类似于 Windows 中的快捷方式。

### 2.2 为什么使用软链接

在深度学习项目中，使用软链接管理数据集有以下优势：

1. **节省空间**: 避免在项目目录中复制大型数据集
2. **统一管理**: 多个项目可以指向同一个数据集
3. **版本控制友好**: 软链接本身很小，不会影响 Git 仓库
4. **灵活性**: 可以随时切换数据集位置，无需修改代码

### 2.3 基本操作

#### 创建软链接

```bash
# 基本语法
ln -s <源路径> <目标路径>

# 示例：将 Cityscapes 数据集链接到 experiments/data/
ln -s /path/to/cityscapes experiments/data/cityscapes

# 示例：使用绝对路径（推荐）
ln -s /Users/mkc/Documents/datasets/cityscapes \
     /Users/mkc/Documents/研一上/Research/mmseg-project/experiments/data/cityscapes

# 示例：链接文件（不仅仅是目录）
ln -s /path/to/model.pth experiments/checkpoints/pretrained/model.pth
```

#### 查看软链接

```bash
# 查看详细信息（可以看到指向）
ls -l experiments/data/

# 输出示例：
# lrwxr-xr-x  1 user  staff  45 Dec  2 14:00 cityscapes -> /path/to/cityscapes
# 第一个字符 'l' 表示这是一个链接
# '->' 后面是实际指向的路径

# 查看链接指向的实际路径
readlink experiments/data/cityscapes
# 或
readlink -f experiments/data/cityscapes  # 显示完整路径
```

#### 删除软链接

```bash
# 注意：不要用 rm -rf，直接用 rm 即可
rm experiments/data/cityscapes

# 删除后，源文件/目录不受影响
```

#### 修改软链接

```bash
# 先删除旧链接
rm experiments/data/cityscapes

# 创建新链接
ln -s /new/path/to/cityscapes experiments/data/cityscapes
```

### 2.4 常见问题

#### 问题 1: 软链接指向不存在的位置

**现象**: 
```bash
ls -l experiments/data/cityscapes
# 输出: cityscapes -> /path/to/cityscapes (红色或显示 broken)
```

**原因**: 源路径不存在或被删除

**解决**: 
```bash
# 检查源路径是否存在
ls /path/to/cityscapes

# 如果不存在，重新创建链接到正确位置
rm experiments/data/cityscapes
ln -s /correct/path/to/cityscapes experiments/data/cityscapes
```

#### 问题 2: 相对路径软链接失效

**现象**: 移动项目目录后，软链接失效

**原因**: 使用了相对路径

**解决**: 使用绝对路径创建软链接
```bash
# ❌ 不推荐：相对路径
ln -s ../datasets/cityscapes experiments/data/cityscapes

# ✅ 推荐：绝对路径
ln -s /absolute/path/to/cityscapes experiments/data/cityscapes
```

#### 问题 3: 软链接 vs 硬链接

**软链接（Symbolic Link）**:
- 可以链接目录
- 可以跨文件系统
- 源文件删除后链接失效
- 使用 `ln -s` 创建

**硬链接（Hard Link）**:
- 只能链接文件，不能链接目录
- 不能跨文件系统
- 源文件删除后仍然有效（直到所有硬链接删除）
- 使用 `ln`（不加 -s）创建

**推荐**: 在项目中使用软链接

#### 问题 4: 在配置文件中使用软链接

软链接创建后，在配置文件中正常使用路径即可：

```python
# experiments/configs/exp_001/my_config.py
data_root = 'experiments/data/cityscapes'  # 使用链接路径

train_dataloader = dict(
    dataset=dict(
        data_root=data_root,  # Python 会自动解析软链接
        # ...
    )
)
```

---

**相关文档**:
- [Git 基础工作流程](../notes/02_git_basics.md)
- [故障排查指南](../notes/04_troubleshooting.md)

**最后更新**: 2024-12-02

