# 示例配置文件
# 这是一个示例，展示如何组织实验配置文件

# 继承基础配置
_base_ = [
    # 模型配置
    '../_base_/models/fcn_r50-d8.py',  # 或使用自定义模型配置
    # 数据集配置
    '../_base_/datasets/cityscapes.py',  # 或使用自定义数据集配置
    # 训练策略配置
    '../_base_/schedules/schedule_40k.py',
    # 运行时配置
    '../_base_/default_runtime.py'
]

# 导入自定义模块（如果有）
custom_imports = dict(
    imports=[
        # 'custom.models.backbones.my_backbone',
        # 'custom.datasets.my_dataset',
    ],
    allow_failed_imports=False
)

# 实验特定配置
# 可以覆盖 _base_ 中的配置

# 工作目录
work_dir = 'experiments/work_dirs/exp_001'

# 模型配置（覆盖或扩展）
# model = dict(
#     backbone=dict(
#         type='ResNet',
#         depth=50,
#         # ...
#     ),
#     decode_head=dict(
#         num_classes=19,
#         # ...
#     ),
# )

# 数据集配置（覆盖或扩展）
# data_root = 'data/cityscapes'
# train_dataloader = dict(
#     dataset=dict(
#         data_root=data_root,
#         # ...
#     )
# )

# 训练配置（覆盖或扩展）
# train_cfg = dict(type='IterBasedTrainLoop', max_iters=40000, val_interval=4000)
# val_cfg = dict(type='ValLoop')
# test_cfg = dict(type='TestLoop')

# 优化器配置（覆盖或扩展）
# optim_wrapper = dict(
#     type='OptimWrapper',
#     optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0005),
# )

# 学习率策略（覆盖或扩展）
# param_scheduler = [
#     dict(
#         type='PolyLR',
#         eta_min=1e-4,
#         power=0.9,
#         begin=0,
#         end=40000,
#     )
# ]

# 预训练模型（可选）
# load_from = 'experiments/checkpoints/pretrained/resnet50.pth'

# 其他配置
# default_hooks = dict(
#     checkpoint=dict(
#         type='CheckpointHook',
#         by_epoch=False,
#         interval=4000,
#         save_best='mIoU'
#     )
# )

