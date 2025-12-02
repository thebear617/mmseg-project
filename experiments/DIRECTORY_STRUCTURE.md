# 实验目录结构

```
experiments/
├── README.md                          # 主说明文档
├── DIRECTORY_STRUCTURE.md             # 本文件：目录结构说明
├── .gitignore                         # Git忽略文件配置
│
├── configs/                           # 配置文件目录
│   ├── _base_/                        # 基础配置（所有实验共享）
│   │   ├── README.md                  # 基础配置说明
│   │   ├── default_runtime.py         # 默认运行时配置
│   │   ├── datasets/                  # 数据集基础配置
│   │   │   └── (数据集配置文件)
│   │   ├── models/                    # 模型基础配置
│   │   │   └── (模型配置文件)
│   │   └── schedules/                 # 训练策略配置
│   │       └── (策略配置文件)
│   │
│   └── exp_XXX/                       # 具体实验配置（按实验编号）
│       ├── README.md                  # 实验说明
│       ├── example_config.py          # 示例配置文件
│       └── (其他实验配置文件)
│
├── custom/                            # 自定义代码模块
│   ├── README.md                      # 自定义模块说明
│   ├── __init__.py                    # 包初始化文件
│   │
│   ├── datasets/                      # 自定义数据集
│   │   ├── __init__.py
│   │   └── my_dataset.py              # 示例：自定义数据集
│   │
│   ├── models/                        # 自定义模型组件
│   │   ├── __init__.py
│   │   ├── backbones/                 # 自定义骨干网络
│   │   │   ├── __init__.py
│   │   │   └── my_backbone.py
│   │   ├── decode_heads/              # 自定义解码头
│   │   │   ├── __init__.py
│   │   │   └── my_head.py
│   │   └── losses/                   # 自定义损失函数
│   │       ├── __init__.py
│   │       └── my_loss.py
│   │
│   └── utils/                         # 自定义工具函数
│       ├── __init__.py
│       └── my_utils.py
│
├── data/                              # 数据集存放目录
│   ├── cityscapes/                   # 示例：Cityscapes数据集
│   ├── ade20k/                       # 示例：ADE20K数据集
│   └── custom_dataset/               # 自定义数据集
│
├── checkpoints/                       # 预训练模型权重
│   ├── pretrained/                   # 官方预训练权重
│   │   └── (预训练模型文件)
│   └── custom/                       # 自定义预训练权重
│       └── (自定义模型文件)
│
├── work_dirs/                         # 实验结果输出目录
│   └── exp_XXX/                      # 每个实验的输出
│       ├── exp_XXX_YYYYMMDD_HHMMSS/  # 带时间戳的训练运行
│       │   ├── config.py             # 实际使用的完整配置
│       │   ├── log.json              # 训练日志
│       │   ├── vis_data/             # 可视化结果
│       │   ├── epoch_*.pth           # 按epoch保存的checkpoint
│       │   └── iter_*.pth            # 按iteration保存的checkpoint
│       └── latest.pth                # 最新checkpoint的软链接
│
├── scripts/                           # 训练和测试脚本
│   ├── README.md                     # 脚本说明
│   │
│   ├── train/                        # 训练脚本
│   │   ├── train_exp_001.sh          # 实验001训练脚本
│   │   └── (其他训练脚本)
│   │
│   ├── test/                         # 测试脚本
│   │   ├── test_exp_001.sh           # 实验001测试脚本
│   │   └── (其他测试脚本)
│   │
│   └── analysis/                     # 结果分析脚本
│       ├── analyze_results.py
│       └── (其他分析脚本)
│
└── logs/                             # 额外的日志文件（可选）
    └── (日志文件)
```

## 目录说明

### configs/
存放所有配置文件，分为：
- **`_base_/`**: 基础配置，所有实验共享
- **`exp_XXX/`**: 具体实验配置，每个实验一个目录

### custom/
存放自定义代码，包括：
- 自定义数据集
- 自定义模型组件（backbone、head、loss等）
- 自定义工具函数

### data/
存放数据集文件。建议：
- 大型数据集使用软链接
- 小型数据集可以直接存放

### checkpoints/
存放预训练模型权重：
- `pretrained/`: 官方预训练权重
- `custom/`: 自己训练的模型权重

### work_dirs/
训练和测试的输出目录：
- 每个实验一个子目录
- 每次训练运行创建带时间戳的子目录
- 包含配置、日志、checkpoints、可视化结果等

### scripts/
存放可执行的训练和测试脚本：
- `train/`: 训练脚本
- `test/`: 测试脚本
- `analysis/`: 结果分析脚本

## 快速开始

1. **创建新实验**:
   ```bash
   mkdir -p experiments/configs/exp_002
   cp experiments/configs/exp_001/example_config.py experiments/configs/exp_002/my_config.py
   ```

2. **修改配置文件**:
   编辑 `experiments/configs/exp_002/my_config.py`，设置实验特定参数

3. **创建训练脚本**:
   ```bash
   cp experiments/scripts/train/train_exp_001.sh experiments/scripts/train/train_exp_002.sh
   # 修改脚本中的实验编号
   ```

4. **运行训练**:
   ```bash
   bash experiments/scripts/train/train_exp_002.sh
   ```

## 注意事项

1. **版本控制**: 
   - ✅ 纳入版本控制: `configs/`, `custom/`, `scripts/`
   - ❌ 不纳入版本控制: `work_dirs/`, `data/`, `checkpoints/`

2. **路径设置**: 
   - 确保设置 `PYTHONPATH` 环境变量
   - 配置文件中的路径使用相对路径或环境变量

3. **实验编号**: 
   - 使用有意义的编号，如 `exp_001`, `exp_002`
   - 或使用描述性名称，如 `exp_baseline`, `exp_ablation_001`

