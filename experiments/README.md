# 实验目录组织说明

本文档说明如何在本项目中组织和管理实验。

## 目录结构

```
experiments/
├── README.md                 # 本说明文档
├── configs/                  # 实验配置文件
│   ├── _base_/              # 基础配置文件（数据集、模型、训练策略等）
│   │   ├── datasets/        # 数据集配置
│   │   ├── models/          # 模型基础配置
│   │   └── schedules/       # 训练策略配置
│   └── exp_XXX/             # 具体实验的配置文件（按实验编号组织）
│       ├── exp_XXX_config.py
│       └── ...
├── custom/                   # 自定义代码模块
│   ├── datasets/            # 自定义数据集
│   │   ├── __init__.py
│   │   └── my_dataset.py
│   ├── models/              # 自定义模型组件
│   │   ├── __init__.py
│   │   ├── backbones/       # 自定义骨干网络
│   │   ├── decode_heads/    # 自定义解码头
│   │   └── losses/          # 自定义损失函数
│   └── utils/               # 自定义工具函数
│       ├── __init__.py
│       └── ...
├── data/                     # 数据集存放目录（软链接或实际数据）
│   ├── cityscapes/          # 示例：Cityscapes数据集
│   ├── ade20k/              # 示例：ADE20K数据集
│   └── custom_dataset/      # 自定义数据集
├── checkpoints/              # 预训练模型权重存放目录
│   ├── pretrained/          # 官方预训练权重
│   └── custom/              # 自定义预训练权重
├── work_dirs/                # 实验结果输出目录
│   └── exp_XXX/             # 每个实验的输出
│       ├── exp_XXX_timestamp/
│       │   ├── config.py    # 实际使用的配置（带时间戳）
│       │   ├── log.json     # 训练日志
│       │   ├── vis_data/    # 可视化结果
│       │   └── ...
│       └── latest.pth       # 最新checkpoint的软链接
├── scripts/                  # 训练和测试脚本
│   ├── train/               # 训练脚本
│   │   ├── train_exp_001.sh
│   │   └── ...
│   ├── test/                # 测试脚本
│   │   ├── test_exp_001.sh
│   │   └── ...
│   └── analysis/            # 结果分析脚本
│       ├── analyze_results.py
│       └── ...
└── logs/                     # 额外的日志文件（可选）
    └── ...
```

## 使用指南

### 1. 创建新实验

创建一个新实验的步骤：

```bash
# 1. 创建实验配置目录
mkdir -p experiments/configs/exp_002

# 2. 创建实验配置文件
# 在 experiments/configs/exp_002/ 下创建配置文件

# 3. 创建对应的 work_dir 目录（可选，会自动创建）
mkdir -p experiments/work_dirs/exp_002
```

### 2. 配置文件组织

#### 基础配置（_base_/）

将常用的配置放在 `configs/_base_/` 下，包括：
- `datasets/`: 数据集配置（数据路径、pipeline等）
- `models/`: 模型基础配置
- `schedules/`: 学习率策略、优化器配置等

#### 实验配置（exp_XXX/）

每个实验的配置文件应该：
- 继承自 `_base_/` 中的配置
- 使用 `custom_imports` 导入自定义模块
- 明确指定 `work_dir`

示例配置文件：
```python
# experiments/configs/exp_002/my_model_config.py
_base_ = [
    '../_base_/models/my_model.py',
    '../_base_/datasets/my_dataset.py',
    '../_base_/schedules/schedule_40k.py',
    '../_base_/default_runtime.py'
]

custom_imports = dict(imports=['custom.models.backbones.my_backbone'], allow_failed_imports=False)

# 实验特定配置
model = dict(
    backbone=dict(type='MyBackbone'),
    # ...
)

work_dir = 'experiments/work_dirs/exp_002'
```

### 3. 自定义代码

#### 添加自定义数据集

1. 在 `custom/datasets/` 下创建数据集类
2. 在配置文件中使用 `custom_imports` 导入
3. 在配置中注册数据集

示例：
```python
# custom/datasets/my_dataset.py
from mmseg.datasets import BaseSegDataset

class MyDataset(BaseSegDataset):
    METAINFO = dict(
        classes=('class1', 'class2', ...),
        palette=[[120, 120, 120], [180, 120, 120], ...]
    )
    
    def __init__(self, ...):
        super().__init__(...)
```

#### 添加自定义模型组件

在 `custom/models/` 下按类型组织：
- `backbones/`: 骨干网络
- `decode_heads/`: 解码头
- `losses/`: 损失函数

记得在 `__init__.py` 中注册：
```python
# custom/models/__init__.py
from .backbones.my_backbone import MyBackbone
from .decode_heads.my_head import MyHead

__all__ = ['MyBackbone', 'MyHead']
```

### 4. 训练和测试

#### 训练

```bash
# 单GPU训练
python mmsegmentation/tools/train.py \
    experiments/configs/exp_002/my_config.py \
    --work-dir experiments/work_dirs/exp_002

# 多GPU训练（4 GPUs）
bash mmsegmentation/tools/dist_train.sh \
    experiments/configs/exp_002/my_config.py \
    4 \
    --work-dir experiments/work_dirs/exp_002

# 使用SLURM
bash mmsegmentation/tools/slurm_train.sh \
    partition_name \
    job_name \
    experiments/configs/exp_002/my_config.py \
    experiments/work_dirs/exp_002
```

#### 测试

```bash
# 测试
python mmsegmentation/tools/test.py \
    experiments/configs/exp_002/my_config.py \
    experiments/work_dirs/exp_002/latest.pth \
    --work-dir experiments/work_dirs/exp_002
```

### 5. 数据集管理

建议将数据集放在 `data/` 目录下，可以：
- 直接存放数据集文件
- 创建软链接到实际数据集位置

```bash
# 创建软链接示例
ln -s /path/to/actual/dataset experiments/data/cityscapes
```

### 6. 预训练模型

将预训练模型放在 `checkpoints/` 目录：
- `checkpoints/pretrained/`: 官方预训练权重
- `checkpoints/custom/`: 自己训练的模型权重

在配置文件中引用：
```python
load_from = 'experiments/checkpoints/pretrained/resnet50.pth'
```

### 7. 实验结果

所有实验结果（checkpoints、日志、可视化等）会自动保存在 `work_dirs/exp_XXX/` 下。

每个训练运行会创建一个带时间戳的子目录，包含：
- `config.py`: 实际使用的完整配置
- `log.json`: 训练日志
- `vis_data/`: 可视化结果
- `*.pth`: 模型checkpoints

## 最佳实践

1. **实验编号规范**: 使用有意义的编号，如 `exp_001`, `exp_002`，或使用描述性名称如 `exp_baseline`, `exp_ablation_001`

2. **配置文件命名**: 使用描述性名称，如 `fcn_r50_40k_cityscapes.py`

3. **版本控制**: 
   - 将 `configs/` 和 `custom/` 纳入版本控制
   - 将 `work_dirs/` 和 `data/` 添加到 `.gitignore`

4. **实验记录**: 为每个实验创建 README 或在实验配置目录下记录实验说明

5. **代码复用**: 尽量将通用代码放在 `_base_/` 中，避免重复

6. **路径管理**: 使用相对路径或环境变量，便于在不同机器上运行

## 环境变量设置

在运行实验前，确保设置正确的 PYTHONPATH：

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
```

或者添加到 `~/.bashrc` 或 `~/.zshrc`：
```bash
export PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH
```

## 注意事项

1. 确保 `custom/` 目录下的模块正确注册到 mmseg 的 registry 中
2. 配置文件中的路径使用相对于项目根目录的路径
3. `work_dir` 建议使用绝对路径或相对于项目根目录的路径
4. 大型数据集和模型权重建议使用软链接或符号链接

