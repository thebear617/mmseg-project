# 实验脚本

本目录存放训练、测试和分析脚本。

## 目录结构

```
scripts/
├── train/          # 训练脚本
├── test/           # 测试脚本
└── analysis/       # 结果分析脚本
```

## 使用方式

### 训练脚本

创建训练脚本示例：

```bash
#!/bin/bash
# scripts/train/train_exp_001.sh

CONFIG=experiments/configs/exp_001/my_config.py
WORK_DIR=experiments/work_dirs/exp_001
GPUS=4

# 设置环境变量
export PYTHONPATH=$PWD:$PYTHONPATH

# 单GPU训练
# python mmsegmentation/tools/train.py $CONFIG --work-dir $WORK_DIR

# 多GPU训练
bash mmsegmentation/tools/dist_train.sh $CONFIG $GPUS --work-dir $WORK_DIR

# SLURM训练
# bash mmsegmentation/tools/slurm_train.sh \
#     partition_name \
#     job_name \
#     $CONFIG \
#     $WORK_DIR
```

### 测试脚本

创建测试脚本示例：

```bash
#!/bin/bash
# scripts/test/test_exp_001.sh

CONFIG=experiments/configs/exp_001/my_config.py
CHECKPOINT=experiments/work_dirs/exp_001/latest.pth
WORK_DIR=experiments/work_dirs/exp_001

export PYTHONPATH=$PWD:$PYTHONPATH

python mmsegmentation/tools/test.py \
    $CONFIG \
    $CHECKPOINT \
    --work-dir $WORK_DIR
```

### 分析脚本

创建结果分析脚本，用于：
- 绘制训练曲线
- 分析模型性能
- 生成实验报告

## 最佳实践

1. **脚本命名**: 使用有意义的名称，如 `train_exp_001.sh`
2. **参数化**: 使用变量存储配置路径，便于修改
3. **日志记录**: 重定向输出到日志文件
4. **错误处理**: 添加错误检查和处理

