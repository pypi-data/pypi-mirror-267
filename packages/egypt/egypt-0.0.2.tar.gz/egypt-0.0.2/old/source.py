import numpy as np
import cv2

# 图像参数
image_size = (1024, 1024)
stripe_width = 200

# 创建横向黑色条纹灰度图像
def black_stripe_gray_background(size=image_size, stripe_width=stripe_width):
    width, height = size
    image = np.ones((height, width)) * 0.5  # 灰色背景

    # 计算粗条纹的起始和结束位置，使其位于图像中间
    start_y = (height - stripe_width) // 2
    end_y = start_y + stripe_width

    # 绘制横向的黑色条纹
    image[start_y:end_y, :] = 0.01

    return image

# 创建纵向白色条纹灰度图像
def white_vertical_stripe_gray_background(size=image_size, stripe_width=stripe_width):
    width, height = size
    image = np.ones((height, width)) * 0.5  # 灰色背景

    # 计算粗条纹的起始和结束位置，使其位于图像中间
    start_x = (width - stripe_width) // 2
    end_x = start_x + stripe_width

    # 绘制纵向的白色条纹
    image[:, start_x:end_x] = 1.0

    return image

def from_src(src,grey=True,image_size=image_size):
    if grey==True:
        image = cv2.resize(cv2.imread(src, cv2.IMREAD_GRAYSCALE), image_size)
    else:
        image = cv2.resize(cv2.imread(src, cv2.COLOR_BGR2RGB), image_size)
    return image.astype(float) / 255.0

def add_gaussian_noise(image, mean=0, std=0.25):
    """
    向图像中添加高斯噪声。

    Parameters:
    - image: 输入图像
    - mean: 噪声的均值，默认为0
    - std: 噪声的标准差，默认为0.1

    Returns:
    - 添加噪声后的图像
    """
    if len(image.shape) == 2:  # 如果是单通道（黑白）图像
        row, col = image.shape
        gauss = np.random.normal(mean, std, (row, col))
        noisy = np.clip(image + gauss, 0, 1)
        return noisy.astype(float)
    elif len(image.shape) == 3:  # 如果是三通道（彩色）图像
        row, col, ch = image.shape
        gauss = np.random.normal(mean, std, (row, col, ch))
        noisy = np.clip(image + gauss, 0, 1)
        return noisy.astype(float)
    else:
        raise ValueError("Unsupported image format")

def laplacian_sharpening(gray, alpha=1.5):
    gray = (gray * 255).round().astype(np.uint8)
    # 应用Laplacian滤波器
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # 计算锐化后的图像
    sharpened = gray - alpha * laplacian

    # 将像素值限制在0到255之间
    sharpened = np.clip(sharpened, 0, 255)

    # 转换为8位图像
    sharpened = np.uint8(sharpened)

    # 将锐化后的图像叠加到原始图像上
    result = cv2.addWeighted(gray, 1, sharpened, alpha, 0)

    return result.astype(float) / 255.0




