# 快速开始指南

本指南将帮助你快速开始使用实验目录进行实验。

## 前置准备

### 1. 设置环境变量

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
export PYTHONPATH=/path/to/mmseg-project:$PYTHONPATH
```

然后执行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

或者在每次运行前执行：
```bash
export PYTHONPATH=$PWD:$PYTHONPATH
```

### 2. 准备数据集

将数据集放在 `experiments/data/` 目录下，或创建软链接：

```bash
# 示例：创建软链接
ln -s /path/to/your/dataset experiments/data/cityscapes
```

## 创建第一个实验

### 步骤 1: 创建实验配置目录

```bash
mkdir -p experiments/configs/exp_002
```

### 步骤 2: 创建配置文件

复制示例配置文件并修改：

```bash
cp experiments/configs/exp_001/example_config.py \
   experiments/configs/exp_002/my_config.py
```

编辑 `experiments/configs/exp_002/my_config.py`：

```python
_base_ = [
    # 从 mmsegmentation 官方配置继承
    'mmseg::fcn/fcn_r50-d8_4xb2-40k_cityscapes-512x1024.py',
    # 或从 experiments/configs/_base_/ 继承
    # '../_base_/models/fcn_r50-d8.py',
    # '../_base_/datasets/cityscapes.py',
    # '../_base_/schedules/schedule_40k.py',
    # '../_base_/default_runtime.py'
]

# 设置工作目录
work_dir = 'experiments/work_dirs/exp_002'

# 修改数据集路径（如果需要）
# data_root = 'experiments/data/cityscapes'
# train_dataloader = dict(
#     dataset=dict(data_root=data_root)
# )
```

### 步骤 3: 创建训练脚本

```bash
cp experiments/scripts/train/train_exp_001.sh \
   experiments/scripts/train/train_exp_002.sh
```

编辑脚本，修改配置路径：

```bash
CONFIG=experiments/configs/exp_002/my_config.py
WORK_DIR=experiments/work_dirs/exp_002
```

### 步骤 4: 运行训练

```bash
bash experiments/scripts/train/train_exp_002.sh
```

## 添加自定义模块

### 添加自定义数据集

1. 创建数据集文件：

```python
# experiments/custom/datasets/my_dataset.py
from mmseg.datasets import BaseSegDataset

class MyDataset(BaseSegDataset):
    METAINFO = dict(
        classes=('background', 'class1', 'class2'),
        palette=[[0, 0, 0], [128, 0, 0], [0, 128, 0]]
    )
    
    def __init__(self, **kwargs):
        super().__init__(
            img_suffix='.jpg',
            seg_map_suffix='.png',
            **kwargs
        )
```

2. 在配置文件中使用：

```python
custom_imports = dict(
    imports=['custom.datasets.my_dataset'],
    allow_failed_imports=False
)

data_root = 'experiments/data/my_dataset'
train_dataloader = dict(
    dataset=dict(
        type='MyDataset',
        data_root=data_root,
        # ...
    )
)
```

### 添加自定义模型组件

1. 创建模型组件：

```python
# experiments/custom/models/backbones/my_backbone.py
from mmseg.registry import MODELS
from mmseg.models.backbones import ResNet

@MODELS.register_module()
class MyBackbone(ResNet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 添加自定义层或修改
```

2. 在配置文件中使用：

```python
custom_imports = dict(
    imports=['custom.models.backbones.my_backbone'],
    allow_failed_imports=False
)

model = dict(
    backbone=dict(type='MyBackbone', ...),
    # ...
)
```

## 常用命令

### 训练

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
```

### 测试

```bash
python mmsegmentation/tools/test.py \
    experiments/configs/exp_002/my_config.py \
    experiments/work_dirs/exp_002/latest.pth \
    --work-dir experiments/work_dirs/exp_002
```

### 推理

```python
from mmseg.apis import inference_model, init_model

# 初始化模型
model = init_model(
    'experiments/configs/exp_002/my_config.py',
    'experiments/work_dirs/exp_002/latest.pth',
    device='cuda:0'
)

# 推理
result = inference_model(model, 'path/to/image.jpg')
```

## 实验管理建议

1. **实验编号**: 使用有意义的编号，如：
   - `exp_001`: 基线实验
   - `exp_002`: 第一个改进
   - `exp_003`: 第二个改进
   - `exp_ablation_001`: 消融实验1

2. **记录实验**: 在 `experiments/configs/exp_XXX/README.md` 中记录：
   - 实验目的
   - 配置说明
   - 运行命令
   - 实验结果
   - 备注

3. **版本控制**: 
   - 提交配置文件: `git add experiments/configs/`
   - 提交自定义代码: `git add experiments/custom/`
   - 不提交结果: `work_dirs/` 已在 `.gitignore` 中

4. **结果对比**: 使用 `experiments/scripts/analysis/` 下的脚本分析多个实验的结果

## 故障排查

### 问题 1: 找不到自定义模块

**解决方案**: 确保设置了 `PYTHONPATH` 并在配置文件中正确导入：

```python
custom_imports = dict(
    imports=['custom.models.backbones.my_backbone'],
    allow_failed_imports=False
)
```

### 问题 2: 找不到数据集

**解决方案**: 检查数据集路径是否正确，确保在配置文件中设置了正确的 `data_root`。

### 问题 3: 找不到预训练模型

**解决方案**: 将预训练模型放在 `experiments/checkpoints/pretrained/` 下，或在配置文件中使用绝对路径。

## 下一步

- 阅读 [README.md](README.md) 了解详细说明
- 查看 [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) 了解目录结构
- 参考 `experiments/configs/exp_001/example_config.py` 了解配置示例

