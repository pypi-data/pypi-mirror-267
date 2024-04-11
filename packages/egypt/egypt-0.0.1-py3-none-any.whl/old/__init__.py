import source
import fusion
import pyramid
import plot

def laplacian_pyramid_demo1():
  x = source.from_src("./images/1_IR.bmp")
  lx = pyramid.Laplacian(image=x)
  lx.show()

def laplacian_pyramid_demo2():
  y = source.from_src("./images/1_VIS.bmp")
  ly = pyramid.Laplacian(image=y,layer=3)
  ly.show()

def laplacian_pyramid_demo3():
  z = source.from_src("./images/1_IR.bmp")
  z = source.add_gaussian_noise(z)
  lz1 = pyramid.Laplacian(image=z)
  lz2 = pyramid.Laplacian(image=z,recon_way='orthogonal')
  lz2.show()
  plot.compare([lz1.recon,lz2.recon],titles=['ordinary','orthogonal'])

def laplacian_pyramid_max_demo1():
  # 得到两张生成的图片
  x = source.black_stripe_gray_background()
  y = source.white_vertical_stripe_gray_background()
  # 构建拉普拉斯金字塔
  l1 = pyramid.Laplacian(image=x)
  l2 = pyramid.Laplacian(image=y)
  # 采用最大值方案融合
  res = fusion.laplacian_max(l1,l2)
  # 画图
  plot.draw(l1,l2,res)

def laplacian_pyramid_max_demo2():
  # 读入两张图片
  x = source.from_src("./images/Kayak_Vis.png")
  y = source.from_src("./images/Kayak_IR.png")
  # 构建拉普拉斯金字塔
  l1 = pyramid.Laplacian(image=x)
  l2 = pyramid.Laplacian(image=y)
  # 采用最大值方案融合
  res = fusion.laplacian_max(l1,l2)
  # 画图
  plot.draw(l1,l2,res)

def laplacian_pyramid_orthogonal_demo():
  # 读入两张图片
  x = source.from_src("./images/1_VIS.bmp")
  y = source.from_src("./images/1_IR.bmp")
  # 构建拉普拉斯金字塔 - 采用正交的方法重构图片
  l1 = pyramid.Laplacian(image=x,recon_way='orthogonal')
  l2 = pyramid.Laplacian(image=y,recon_way='orthogonal')
  # 采用最大值方案融合 - 传统方案重构图片
  res = fusion.laplacian_max(l1,l2)
  pictures = [res.recon]
  # 采用正交的方法重构图片
  res.reconstruct(method='orthogonal')
  pictures.append(res.recon)
  # 画图
  plot.draw(l1,l2,res)
  plot.compare(pictures,titles=['ordinary','orthogonal'])

  # 添加高斯噪声
  x = source.add_gaussian_noise(x)
  y = source.add_gaussian_noise(y)
  # 构建拉普拉斯金字塔 - 采用正交的方法重构图片
  l1 = pyramid.Laplacian(image=x,recon_way='orthogonal')
  l2 = pyramid.Laplacian(image=y,recon_way='orthogonal')
  # 采用最大值方案融合 - 传统方案重构图片
  res = fusion.laplacian_max(l1,l2)
  pictures = [res.recon]
  # 采用正交的方法重构图片
  res.reconstruct(method='orthogonal')
  pictures.append(res.recon)
  # 画图
  plot.draw(l1,l2,res)
  plot.compare(pictures,titles=['ordinary','orthogonal'])

def laplacian_pyramid_info_and_energy_demo():
  # 读入两张图片
  x = source.from_src("./images/1_VIS.bmp")
  y = source.from_src("./images/1_IR.bmp")
  # 构建拉普拉斯金字塔
  l1 = pyramid.Laplacian(image=x)
  l2 = pyramid.Laplacian(image=y)
  # 采用最大值方案融合
  res1 = fusion.laplacian_max(l1,l2)
  # 采用信息与能量最大方案
  res2 = fusion.laplacian_info_and_energy(l1,l2,region=9)
  # 画图
  plot.draw(l1,l2,res2)
  pictures = [res1.recon,res2.recon]
  plot.compare(pictures,titles=['Max Value','Max Info and Energy'])

def laplacian_pyramid_info_and_energy_demo2():
  # 读入两张图片
  x = source.from_src("./images/1_VIS.bmp")
  y = source.from_src("./images/1_IR.bmp")
  # 构建拉普拉斯金字塔
  l1 = pyramid.Laplacian(image=source.laplacian_sharpening(x))
  l2 = pyramid.Laplacian(image=source.laplacian_sharpening(y))
  # 采用最大值方案融合
  res1 = fusion.laplacian_max(l1,l2)
  # 采用信息与能量最大方案
  res2 = fusion.laplacian_info_and_energy(l1,l2,region=9)
  # 画图
  plot.draw(l1,l2,res2)
  pictures = [res1.recon,res2.recon]
  plot.compare(pictures,titles=['Max Value','Max Info and Energy'])

def laplacian_sharpening_demo():
  img1 = source.from_src("./images/1_VIS.bmp")
  img2 = source.laplacian_sharpening(img1)
  plot.compare([img1,img2],titles=['Origin','After Sharpening'])

def contrust_pyramid_demo():
  x = source.from_src("./images/1_IR.bmp")
  lx = pyramid.Contrust(image=x)
  lx.show()

  y = source.from_src("./images/1_VIS.bmp")
  ly = pyramid.Contrust(image=y)
  ly.show()

  #z = source.from_src("./images/1_VIS.bmp")
  #lz = pyramid.Contrust(image=x,layer=3)
  #lz.show()

def graident_pyramid_demo():
  x = source.from_src("./images/1_IR.bmp")
  lx = pyramid.Graident(image=x)
  lx.show()

def morphological_pyramid_demo():
  x = source.from_src("./images/1_VIS.bmp")
  lx = pyramid.Morphological(image=x)
  lx.show()

def main():
  #laplacian_pyramid_demo1()
  #laplacian_pyramid_demo2()
  #laplacian_pyramid_demo3()
  #laplacian_pyramid_max_demo1()
  #laplacian_pyramid_max_demo2()
  #laplacian_pyramid_orthogonal_demo()
  #laplacian_pyramid_info_and_energy_demo()
  #laplacian_pyramid_info_and_energy_demo2()
  #laplacian_sharpening_demo()
  #contrust_pyramid_demo()
  graident_pyramid_demo()
  #morphological_pyramid_demo()

if __name__ == '__main__':
  main()
