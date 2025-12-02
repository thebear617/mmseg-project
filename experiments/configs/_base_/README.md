# 基础配置文件

本目录存放所有实验共享的基础配置文件。

## 目录结构

```
_base_/
├── datasets/        # 数据集配置
├── models/          # 模型基础配置
├── schedules/       # 训练策略配置
└── default_runtime.py  # 默认运行时配置
```

## 使用方式

在实验配置文件中通过 `_base_` 继承：

```python
_base_ = [
    '../_base_/models/fcn_r50-d8.py',
    '../_base_/datasets/cityscapes.py',
    '../_base_/schedules/schedule_40k.py',
    '../_base_/default_runtime.py'
]
```

## 配置说明

### datasets/

存放数据集相关配置，包括：
- 数据集路径
- 数据加载pipeline
- 数据增强策略

### models/

存放模型基础配置，包括：
- 骨干网络配置
- 解码头配置
- 损失函数配置

### schedules/

存放训练策略配置，包括：
- 优化器配置
- 学习率策略
- 训练轮数

### default_runtime.py

默认运行时配置，包括：
- 日志配置
- Hook配置
- 可视化配置

