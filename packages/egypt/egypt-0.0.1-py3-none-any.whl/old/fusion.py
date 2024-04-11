import numpy as np
import pyramid
import cv2

def laplacian_max(l1,l2,**kwargs):
    image_fusion = []
    image_fusion.append((l1.pyramid[0]+l2.pyramid[0])/2)
    for i in range(len(l1.pyramid)-1):
        image_fusion.append(
          np.maximum(l1.pyramid[i+1],l2.pyramid[i+1]))
    return pyramid.Laplacian(pyramid=image_fusion,**kwargs)

def laplacian_info_and_energy(l1,l2,region=9,**kwargs):
  J = K = region
  border = int((J-1)/2)
  def D_and_E(image):
    image = (image * 255).round().astype(np.uint8)
    # 获得图像的均值
    X_mean = np.mean(image)
    # 初始化D
    d = np.zeros((image.shape[0],image.shape[1]))
    # 对边缘进行扩充
    image = cv2.copyMakeBorder(image, 
      border, border, border, border, cv2.BORDER_WRAP)
    # 填充d
    for i in range(d.shape[0]):
      for j in range(d.shape[1]):
        temp = (image[0:J, 0:K] - X_mean)**2
        d[i][j] = np.sum(temp)/J/K
    # 初始化E
    e = np.zeros((image.shape[0],image.shape[1]))
    # 计算灰度直方图
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    # 将直方图归一化为概率
    hist_probability = hist / np.sum(hist)
    # 填充d
    for i in range(e.shape[0]):
      for j in range(e.shape[1]):
        e[i][j] = hist_probability[image[i][j]]
    return (d,e)

  def RE(image):
    image = (image * 255).round().astype(np.uint8)
    # 初始化RE
    re = np.zeros((image.shape[0],image.shape[1]))
    # 对边缘进行扩充
    image = cv2.copyMakeBorder(image, 2, 2, 2, 2, cv2.BORDER_WRAP)
    # w
    w = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])/256
    # 填充RE
    for i in range(re.shape[0]):
      for j in range(re.shape[1]):
        patch = image[i:i+5, j:j+5]
        re[i][j] = np.sum(w*(patch**2))/5/5
    return re

  image_fusion = []
  (D1,E1) = D_and_E(l1.pyramid[0])
  (D2,E2) = D_and_E(l2.pyramid[0])
  F0 = np.zeros(D1.shape)
  for i in range(D1.shape[0]):
    for j in range(D1.shape[1]):
      if D1[i][j]>D2[i][j] and E1[i][j]>E2[i][j]:
        F0[i][j] = l1.pyramid[0][i][j]
      elif D1[i][j]<D2[i][j] and E1[i][j]<E2[i][j]:
        F0[i][j] = l2.pyramid[0][i][j]
      else:
        F0[i][j] = (l1.pyramid[0][i][j]+l2.pyramid[0][i][j])/2

  image_fusion.append((l1.pyramid[0]+l2.pyramid[0])/2)
  for i in range(len(l1.pyramid)-1):
    print(i+1,'of',len(l1.pyramid))
    RE1 = RE(l1.pyramid[i+1])
    RE2 = RE(l2.pyramid[i+1])
    f = np.zeros(RE1.shape)
    for j in range(f.shape[0]):
      for k in range(f.shape[1]):
        if RE1[j][k]>RE2[j][k]: f[j][k] = l1.pyramid[i+1][j][k]
        else: f[j][k] = l2.pyramid[i+1][j][k]
    image_fusion.append(f)
  p = pyramid.Laplacian(pyramid=image_fusion,**kwargs)
  return p