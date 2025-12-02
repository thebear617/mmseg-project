#!/bin/bash
# 实验 001 测试脚本

# 配置路径
CONFIG=experiments/configs/exp_001/my_config.py
CHECKPOINT=experiments/work_dirs/exp_001/latest.pth
WORK_DIR=experiments/work_dirs/exp_001

# 设置环境变量
export PYTHONPATH=$PWD:$PYTHONPATH

# 检查checkpoint是否存在
if [ ! -f "$CHECKPOINT" ]; then
    echo "错误: 找不到checkpoint文件: $CHECKPOINT"
    exit 1
fi

# 运行测试
python mmsegmentation/tools/test.py \
    $CONFIG \
    $CHECKPOINT \
    --work-dir $WORK_DIR

echo "测试完成！结果保存在: $WORK_DIR"

