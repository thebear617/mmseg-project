# 实验 001

> **实验模板说明**: 本文档是实验记录模板，请根据实际实验情况填写各部分内容。完成后可作为后续实验的参考。

---

## 实验基本信息

| 项目 | 内容 |
|------|------|
| **实验编号** | exp_001 |
| **实验名称** | （填写实验的简短描述性名称） |
| **创建日期** | YYYY-MM-DD |
| **完成日期** | YYYY-MM-DD |
| **实验者** | （填写你的名字） |
| **状态** | 🟢 进行中 / 🟡 暂停 / ✅ 已完成 / ❌ 失败 |

---

## 实验描述

### 实验目的
（清晰描述本次实验的目标，例如：测试新的损失函数对模型性能的影响）

### 实验假设
（描述你的假设，例如：使用 Focal Loss 可以提升小目标分割效果）

### 实验方法
（简要描述实验方法，例如：在 FCN 模型基础上替换损失函数为 Focal Loss，其他配置保持不变）

### 预期结果
（描述预期的实验结果，例如：mIoU 提升 2-3%，小目标分割精度提升 5%）

---

## 配置说明

### 模型配置
- **模型架构**: （例如：FCN with ResNet-50 backbone）
- **骨干网络**: （例如：ResNet-50, depth=50）
- **解码头**: （例如：FCNHead with 512 channels）
- **其他组件**: （例如：使用 ASPP 模块）

### 数据集配置
- **数据集名称**: （例如：Cityscapes）
- **数据集路径**: `experiments/data/cityscapes`
- **训练集大小**: （例如：2975 张）
- **验证集大小**: （例如：500 张）
- **测试集大小**: （例如：1525 张）
- **类别数**: （例如：19 类）
- **图像尺寸**: （例如：512x1024）

### 训练策略
- **优化器**: （例如：SGD）
  - 学习率: （例如：0.01）
  - Momentum: （例如：0.9）
  - Weight Decay: （例如：0.0005）
- **学习率策略**: （例如：PolyLR）
  - 初始学习率: （例如：0.01）
  - 最小学习率: （例如：1e-4）
  - Power: （例如：0.9）
- **训练轮数**: （例如：40k iterations）
- **Batch Size**: （例如：4 per GPU）
- **GPU 数量**: （例如：4）
- **混合精度训练**: （是/否）

### 数据增强
- **训练时**: （例如：RandomFlip, RandomResize, ColorJitter）
- **验证时**: （例如：无 / Resize）

### 其他设置
- **预训练模型**: （例如：使用 ImageNet 预训练的 ResNet-50）
- **预训练路径**: `experiments/checkpoints/pretrained/resnet50.pth`
- **特殊配置**: （例如：使用 OHEM, 使用多尺度训练等）

---

## 配置文件

### 主配置文件
- **路径**: `experiments/configs/exp_001/my_config.py`
- **继承配置**: 
  ```python
  _base_ = [
      '../_base_/models/fcn_r50-d8.py',
      '../_base_/datasets/cityscapes.py',
      '../_base_/schedules/schedule_40k.py',
      '../_base_/default_runtime.py'
  ]
  ```
- **自定义模块**: （如果有）
  ```python
  custom_imports = dict(
      imports=['custom.models.backbones.my_backbone'],
      allow_failed_imports=False
  )
  ```

### 关键配置修改
（列出与基础配置不同的关键修改）
- 修改项1: （例如：损失函数从 CrossEntropyLoss 改为 FocalLoss）
- 修改项2: （例如：学习率从 0.01 调整为 0.005）

---

## 运行命令

### 环境准备
```bash
# 设置环境变量（如果未永久设置）
export PYTHONPATH=$PWD:$PYTHONPATH

# 激活虚拟环境（如果使用）
conda activate mmseg  # 或 source venv/bin/activate
```

### 训练命令

#### 单 GPU 训练
```bash
python mmsegmentation/tools/train.py \
    experiments/configs/exp_001/my_config.py \
    --work-dir experiments/work_dirs/exp_001
```

#### 多 GPU 训练（实际使用）
```bash
# 使用训练脚本
bash experiments/scripts/train/train_exp_001.sh

# 或直接使用命令
bash mmsegmentation/tools/dist_train.sh \
    experiments/configs/exp_001/my_config.py \
    4 \
    --work-dir experiments/work_dirs/exp_001
```

#### SLURM 集群训练
```bash
bash mmsegmentation/tools/slurm_train.sh \
    partition_name \
    exp_001 \
    experiments/configs/exp_001/my_config.py \
    experiments/work_dirs/exp_001
```

### 测试命令
```bash
# 使用测试脚本
bash experiments/scripts/test/test_exp_001.sh

# 或直接使用命令
python mmsegmentation/tools/test.py \
    experiments/configs/exp_001/my_config.py \
    experiments/work_dirs/exp_001/latest.pth \
    --work-dir experiments/work_dirs/exp_001
```

### 推理命令
```bash
# 单张图像推理
python mmsegmentation/demo/image_demo.py \
    experiments/configs/exp_001/my_config.py \
    experiments/work_dirs/exp_001/latest.pth \
    path/to/image.jpg \
    --out-dir experiments/work_dirs/exp_001/inference_results
```

---

## 实验结果

### 验证集性能

| 指标 | 数值 | 备注 |
|------|------|------|
| **mIoU** | - | Mean Intersection over Union |
| **mAcc** | - | Mean Accuracy |
| **aAcc** | - | Average Accuracy |
| **其他指标** | - | （如有其他评估指标） |

### 测试集性能（如有）

| 指标 | 数值 | 备注 |
|------|------|------|
| **mIoU** | - | - |
| **mAcc** | - | - |
| **aAcc** | - | - |

### 训练过程记录

- **训练时间**: （例如：约 8 小时，使用 4 GPUs）
- **最佳 checkpoint**: （例如：iter_40000.pth）
- **收敛情况**: （例如：在 35k iteration 后收敛，loss 稳定在 0.05）
- **内存使用**: （例如：峰值约 12GB per GPU）
- **训练曲线**: （可附上训练曲线截图或链接）

### 可视化结果

- **可视化结果路径**: `experiments/work_dirs/exp_001/vis_data/`
- **主要观察**:
  - （例如：小目标分割效果良好）
  - （例如：边界分割不够清晰）
  - （例如：某些类别存在混淆）

### 与基线对比（如有）

| 实验 | mIoU | mAcc | aAcc | 备注 |
|------|------|------|------|------|
| **基线 (exp_000)** | - | - | - | - |
| **本实验 (exp_001)** | - | - | - | - |
| **提升** | - | - | - | - |

---

## 实验笔记

### 重要发现
1. （记录实验过程中的重要发现，例如：Focal Loss 确实提升了小目标的分割效果）
2. （例如：但整体 mIoU 提升不明显，可能是因为类别不平衡问题）
3. （例如：训练初期 loss 震荡较大，调整学习率后改善）

### 遇到的问题及解决方案

#### 问题 1: （问题描述）
- **现象**: （描述问题现象）
- **原因**: （分析问题原因）
- **解决方案**: （描述解决方案）
- **参考**: （如有参考链接或文档）

#### 问题 2: （问题描述）
- **现象**: （描述问题现象）
- **原因**: （分析问题原因）
- **解决方案**: （描述解决方案）

### 实验改进方向
1. （例如：尝试不同的 focal loss 参数 alpha 和 gamma）
2. （例如：结合其他损失函数，如 Dice Loss）
3. （例如：调整数据增强策略，增加更多小目标样本）
4. （例如：尝试不同的学习率策略）

### 后续实验计划
- **exp_002**: （例如：测试 Focal Loss + Dice Loss 的组合）
- **exp_003**: （例如：调整 Focal Loss 的 alpha 和 gamma 参数）

---

## 资源链接

### 相关文档
- [实验目录说明](../../README.md)
- [快速开始指南](../../QUICKSTART.md)
- [开发基础笔记](../../notes/development_basics.md)

### 参考论文/资料
- （如有参考的论文或资料，列出链接或引用）

### 相关实验
- **exp_000**: （基线实验）
- **exp_002**: （相关实验）

---

## 检查清单

在完成实验后，请确认：

- [ ] 实验结果已记录完整
- [ ] 配置文件已保存并提交到版本控制
- [ ] 训练日志和 checkpoint 已备份（如需要）
- [ ] 可视化结果已保存
- [ ] 实验笔记已更新
- [ ] 相关代码已提交到版本控制
- [ ] 实验总结已完成

---

## 附录

### 完整配置文件
（可选：粘贴完整的配置文件内容，或提供文件路径）

### 训练日志摘要
（可选：粘贴关键的训练日志片段）

### 错误日志
（如有错误，记录错误信息）

---

**最后更新**: YYYY-MM-DD  
**下次更新**: （计划更新时间）
