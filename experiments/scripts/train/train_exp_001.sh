#!/bin/bash
# 实验 001 训练脚本

# 配置路径
CONFIG=experiments/configs/exp_001/my_config.py
WORK_DIR=experiments/work_dirs/exp_001
GPUS=4

# 设置环境变量
export PYTHONPATH=$PWD:$PYTHONPATH

# 创建输出目录
mkdir -p $WORK_DIR

# 单GPU训练
# python mmsegmentation/tools/train.py $CONFIG --work-dir $WORK_DIR

# 多GPU训练
bash mmsegmentation/tools/dist_train.sh $CONFIG $GPUS --work-dir $WORK_DIR

# SLURM训练（取消注释以使用）
# bash mmsegmentation/tools/slurm_train.sh \
#     partition_name \
#     exp_001 \
#     $CONFIG \
#     $WORK_DIR

echo "训练完成！结果保存在: $WORK_DIR"

