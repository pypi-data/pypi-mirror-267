import numpy as np
import matplotlib.pyplot as plt

def draw(o1,o2,f):
  plt.figure(figsize=(20, 12))
  plt.subplot(3, 7, 1)
  plt.imshow(o1.image, cmap='gray', vmin=0, vmax=1)
  plt.title('Original 1')
  plt.axis('off')

  plt.subplot(3, 7, 8)
  plt.imshow(o2.image, cmap='gray', vmin=0, vmax=1)
  plt.title('Original 2')
  plt.axis('off')

  for i in range(5):
    plt.subplot(3, 7, i + 2)
    if i!=0:plt.imshow(o1.pyramid[i], cmap='gray')
    else:plt.imshow(o1.pyramid[i], cmap='gray', vmin=0, vmax=1)
    plt.title(o1.name+f' L{i+1}')
    plt.axis('off')
    plt.subplot(3, 7, i + 9)
    if i!=0:plt.imshow(o2.pyramid[i], cmap='gray')
    else:plt.imshow(o2.pyramid[i], cmap='gray', vmin=0, vmax=1)
    plt.title(o2.name+f' L{i+1}')
    plt.axis('off')
    plt.subplot(3, 7, i + 16)
    if i!=0:plt.imshow(f.pyramid[i], cmap='gray')
    else:plt.imshow(f.pyramid[i], cmap='gray', vmin=0, vmax=1)
    plt.title(f'Fusion L{i+1}')
    plt.axis('off')

  plt.subplot(3, 7, 7)
  plt.imshow(o1.recon, cmap='gray', vmin=0, vmax=1)
  plt.title('Reconstructed 1')
  plt.axis('off')

  plt.subplot(3, 7, 14)
  plt.imshow(o2.recon, cmap='gray', vmin=0, vmax=1)
  plt.title('Reconstructed 2')
  plt.axis('off')

  plt.subplot(3, 7, 21)
  plt.imshow(f.recon, cmap='gray', vmin=0, vmax=1)
  plt.title('Fusion')
  plt.axis('off')

  plt.tight_layout()
  plt.show()
  
def compare(images,titles):
  for i in range(len(images)):
    plt.subplot(1, len(images), i+1)
    plt.imshow(images[i], cmap='gray', vmin=0, vmax=1)
    plt.title(titles[i])
    plt.axis('off')
  plt.tight_layout()
  plt.show()
