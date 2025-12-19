#  用命令行推理：输出一张overlay图
python demo/image_demo.py \
  data/street_uk.jpeg \
  configs/segformer/segformer_mit-b5_8xb1-160k_cityscapes-1024x1024.py \
  /data/mkc/mmseg-project/mmsegmentation/checkpoints/segformer_mit-b5.pth \
  --out-file outputs/B1_uk_segformer.jpg \
  --device cuda:1 \
  --opacity 0.5