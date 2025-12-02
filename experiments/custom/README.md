# 自定义代码模块

本目录存放所有自定义的代码模块，包括自定义数据集、模型组件、工具函数等。

## 目录结构

```
custom/
├── datasets/           # 自定义数据集
│   ├── __init__.py
│   └── my_dataset.py
├── models/             # 自定义模型组件
│   ├── __init__.py
│   ├── backbones/      # 自定义骨干网络
│   ├── decode_heads/   # 自定义解码头
│   └── losses/         # 自定义损失函数
└── utils/              # 自定义工具函数
    ├── __init__.py
    └── ...
```

## 使用方式

### 1. 在配置文件中导入

使用 `custom_imports` 导入自定义模块：

```python
custom_imports = dict(
    imports=['custom.models.backbones.my_backbone', 
             'custom.datasets.my_dataset'],
    allow_failed_imports=False
)
```

### 2. 注册到 Registry

自定义的模型组件需要注册到 mmseg 的 registry：

```python
# custom/models/backbones/my_backbone.py
from mmseg.registry import MODELS
from mmseg.models.backbones import ResNet

@MODELS.register_module()
class MyBackbone(ResNet):
    def __init__(self, ...):
        super().__init__(...)
```

### 3. 在配置中使用

注册后即可在配置文件中使用：

```python
model = dict(
    backbone=dict(type='MyBackbone', ...),
    ...
)
```

## 开发规范

1. **模块注册**: 所有自定义模块必须注册到对应的 registry
2. **文档字符串**: 为所有类和函数添加详细的文档字符串
3. **类型提示**: 使用类型提示提高代码可读性
4. **测试**: 为自定义模块编写单元测试（可选但推荐）

## Registry 说明

mmseg 使用以下 registry：
- `MODELS`: 模型组件（backbone, head, loss等）
- `DATASETS`: 数据集
- `HOOKS`: 训练钩子
- `OPTIMIZERS`: 优化器
- `SCHEDULERS`: 学习率调度器

