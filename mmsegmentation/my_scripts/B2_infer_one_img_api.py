import torch
import cv2
import matplotlib.pyplot as plt
from mmseg.apis import init_model, inference_model, show_result_pyplot



# 模型 config 配置文件
config_file = 'configs/segformer/segformer_mit-b5_8xb1-160k_cityscapes-1024x1024.py'
# 模型 checkpoint 权重文件
checkpoint_file = 'checkpoints/segformer_mit-b5.pth'


# 模型初始化
model = init_model(config_file, checkpoint_file, device='cuda:1')

img_path = 'data/street_uk.jpeg'
img_bgr = cv2.imread(img_path)
plt.imshow(img_bgr[:,:,::-1]) # bgr->rgb
plt.axis('off')
plt.savefig('outputs/input.png', dpi=200, bbox_inches='tight')
print("saved to outputs/input.png")


# 模型推理
result = inference_model(model, img_bgr)
pred_mask = result.pred_sem_seg.data[0].detach().cpu().numpy()


# 可视化方式一:overlay方式其实就是原图叠加掩码
plt.figure(figsize=(14, 8))
plt.imshow(img_bgr[:,:,::-1])
plt.imshow(pred_mask, alpha=0.55) # alpha 高亮区域透明度，越小越接近原图
plt.axis('off')
plt.savefig('outputs/B2-1.jpg')
print("saved to outputs/B2-1.jpg")


# 可视化方式二:原图➕overlay图
plt.figure(figsize=(14, 8))

plt.subplot(1,2,1)
plt.imshow(img_bgr[:,:,::-1])
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(img_bgr[:,:,::-1])
plt.imshow(pred_mask, alpha=0.6) # alpha 高亮区域透明度，越小越接近原图
plt.axis('off')
plt.savefig('outputs/B2-2.jpg')
print("saved to outputs/B2-2.jpg")

# 可视化方式三:用规定好的palette做overlay,调用了mmseg中的show_result_pyplot函数
img_rgb = img_bgr[:, :, ::-1]
img_viz = show_result_pyplot(
    model,                   # 必需:提供网络推理配置 + 可视化需要的 classes/palette 元信息
    img_rgb,                 # 必需:作为底图进行 overlay
    result,                  # 必需:提供要画的分割结果
    show=False,              # 必需:服务器不写就一直卡住
    opacity=0.8,             # 可选:overlay 透明度，默认0.5
    title='MMSeg',           # 可选:可视化的标题，默认空字符串
    draw_gt=False,           # 可选:绘制GT,默认画,推理时没有GT,所以设为不画
    draw_pred=True,          # 可选:绘制预测图,默认画
    wait_time=0,             # 可选:画图的等待时间,默认为0,一直等待的意思
    with_labels=False,       # 可选:图上是否写类别名字,默认写
    save_dir='outputs',      # 可选:与out_file配套就好,save_dir到文件夹名,out_file到文件名
    out_file='outputs/B2-3.jpg'
)
print("saved to outputs/B2-3.jpg")



# 可视化方式四:加图例,这个也是用规定好的palette,但没有调用api

from mmseg.datasets import cityscapes
import numpy as np
import mmcv 
from PIL import Image

# 获取类别名和调色板
classes = cityscapes.CityscapesDataset.METAINFO['classes']
palette = cityscapes.CityscapesDataset.METAINFO['palette']
opacity = 0.15 # 透明度，越大越接近原图

# 将分割图按调色板染色
# seg_map = result[0].astype('uint8')
seg_map = pred_mask.astype('uint8')
seg_img = Image.fromarray(seg_map).convert('P')
seg_img.putpalette(np.array(palette, dtype=np.uint8))

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
plt.figure(figsize=(14, 8))
im = plt.imshow(((np.array(seg_img.convert('RGB')))*(1-opacity) + mmcv.imread(img_path)*opacity) / 255)

# 为每一种颜色创建一个图例
patches = [mpatches.Patch(color=np.array(palette[i])/255., label=classes[i]) for i in range(len(classes))]
plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize='large')
plt.savefig('outputs/B2-4.jpg')
print("saved to outputs/B2-4.jpg")