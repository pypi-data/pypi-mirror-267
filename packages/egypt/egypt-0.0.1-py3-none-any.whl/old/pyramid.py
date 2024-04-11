import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Pyramid(object):
    def __init__(self,name,**kwargs):
        # Images Params Init
        self.name = name           # Name of Pyramid, eg.`Laplacian`
        self.image = None          # Input image
        self.pyramid = []          # Pyramids
        self.layer = 5             # Number of Layers of Pyramids
        self.recon = None          # Output image
        self.auto = True           # Auto Construct and Reconstruct
        self.con_way = 'ordinary'  # Construct Pyramid Method
        self.recon_way = 'ordinary'# Reconstruct Pyramid Method
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Default Operations
        if type(self.image) != type(None):
            # Build Gaussian Pyramid from Imput Image
            self.build_gaussian_pyramid()
            # Auto Construct Pyramid and Reconstruct Output Image
            if self.auto:
                self.construct()
                self.reconstruct()
        elif self.pyramid != []:
            # Auto Reconstruct Output Image
            if self.auto: self.reconstruct()

    def build_gaussian_pyramid(self):
        image = self.image
        self.gaussian = [image]
        for _ in range(self.layer-1):
            image = cv2.pyrDown(image)
            self.gaussian.append(image)

    def construct(self):
        pass

    def reconstruct(self):
        pass

    def show(self,vmin=0,vmax=1):
        plt.figure(figsize=(20, 12))
        if type(self.image) != type(None):
            plt.subplot(2, self.layer, 1)
            plt.imshow(self.image, cmap='gray', vmin=vmin, vmax=vmax)
            plt.title('Original')
            plt.axis('off')
        plt.subplot(2, self.layer, self.layer)
        if type(self.recon) != type(None):
            plt.subplot(2, self.layer, self.layer)
            plt.imshow(self.recon, cmap='gray', vmin=vmin, vmax=vmax)
            plt.title('Reconstructed')
            plt.axis('off')
        if self.pyramid != []:
            for i in range(self.layer):
                plt.subplot(2, self.layer, self.layer+i+1)
                if i!=self.layer-1:plt.imshow(self.pyramid[i], cmap='gray')
                else:plt.imshow(self.pyramid[i], cmap='gray', vmin=vmin, vmax=vmax)
                plt.title(self.name+f' L{i+1}')
                plt.axis('off')
        plt.tight_layout()
        plt.show()

class Laplacian(Pyramid):
    def __init__(self,**kwargs):
        super().__init__("Laplacian",**kwargs)

    def construct(self,method=None):
        if type(method) == type(None): method = self.con_way
        else: self.con_way = method

        if method == 'ordinary':
            laplacian_pyramid = []
            for i in range(self.layer-1):
                expanded = cv2.pyrUp(self.gaussian[i+1])
                laplacian = self.gaussian[i] - expanded
                laplacian_pyramid.append(laplacian)
            laplacian_pyramid.append(self.gaussian[-1])

            self.pyramid = laplacian_pyramid
        else:
            raise ValueError("Wrong construct method:",method)

    def reconstruct(self,method=None):
        if type(method) == type(None): method = self.recon_way
        else: self.recon_way = method

        if method == 'ordinary':
            image_reconstructed = self.pyramid[-1]
            for i in reversed(range(self.layer-1)):
                expanded = cv2.pyrUp(image_reconstructed)
                image_reconstructed = self.pyramid[i] + expanded

            self.recon = image_reconstructed
        elif method == 'orthogonal':
            image_reconstructed = self.pyramid[-1]
            for i in reversed(range(self.layer-1)):
                print(image_reconstructed.shape)
                print(cv2.pyrDown(self.pyramid[i]).shape)
                expanded = cv2.pyrUp(image_reconstructed - cv2.pyrDown(self.pyramid[i]))
                image_reconstructed = self.pyramid[i] + expanded

            self.recon = image_reconstructed
        else:
            raise ValueError("Wrong reconstruct method:",method)

class Contrust(Pyramid):
    def __init__(self,**kwargs):
        super().__init__("Contrust",**kwargs)

    def construct(self,method=None):
        if type(method) == type(None): method = self.con_way
        else: self.con_way = method

        if method == 'ordinary':
            construct_pyramid = []
            for i in range(self.layer-1):
                expanded = cv2.pyrUp(self.gaussian[i+1])
                laplacian = self.gaussian[i] / expanded - 1
                laplacian[np.isnan(laplacian)] = 0
                construct_pyramid.append(laplacian)
            construct_pyramid.append(self.gaussian[-1])

            self.pyramid = construct_pyramid
        else:
            raise ValueError("Wrong construct method:",method)

    def reconstruct(self,method=None):
        if type(method) == type(None): method = self.recon_way
        else: self.recon_way = method

        if method == 'ordinary':
            image_reconstructed = self.pyramid[-1]
            for i in reversed(range(self.layer-1)):
                expanded = cv2.pyrUp(image_reconstructed)
                image_reconstructed = (self.pyramid[i] + 1) * expanded
                image_reconstructed[np.isnan(image_reconstructed)] = 0

            self.recon = image_reconstructed
        else:
            raise ValueError("Wrong reconstruct method:",method)

class Graident(Pyramid):
    def __init__(self,**kwargs):
        super().__init__("Graident",**kwargs)

    def construct(self,method=None):
        if type(method) == type(None): method = self.con_way
        else: self.con_way = method

        if method == 'ordinary':
            h1 = np.array([[ 1,-1]])
            h2 = np.array([[ 0,-1],[ 1, 0]]) / math.sqrt(2)
            h3 = np.array([[-1],[1]])
            h4 = np.array([[-1, 0],[ 0, 1]]) / math.sqrt(2)
            w = np.array([[1,2,1],[2,4,2],[1,2,1]])/16

            graident_pyramid = []
            for i in range(self.layer-1):
                pyramids = []
                temp = cv2.filter2D(self.gaussian[i], -1, w) + self.gaussian[i]
                pyramids.append(cv2.filter2D(temp, -1, h1))
                pyramids.append(cv2.filter2D(temp, -1, h2))
                pyramids.append(cv2.filter2D(temp, -1, h3))
                pyramids.append(cv2.filter2D(temp, -1, h4))
                graident_pyramid.append(pyramids)
            graident_pyramid.append([self.gaussian[-1]]*4)

            self.pyramid = graident_pyramid
        else:
            raise ValueError("Wrong construct method:",method)

    def reconstruct(self,method=None):
        if type(method) == type(None): method = self.recon_way
        else: self.recon_way = method

        if method == 'ordinary':
            w = np.array([[1,2,1],[2,4,2],[1,2,1]])/16
            h1 = np.array([[ 1,-1]])
            h2 = np.array([[ 0,-1],[ 1, 0]]) / math.sqrt(2)
            h3 = np.array([[-1],[1]])
            h4 = np.array([[-1, 0],[ 0, 1]]) / math.sqrt(2)
            h = [h1,h2,h3,h4]
            lp = Laplacian(auto=False,layer=self.layer)

            for i in range(self.layer-1):
                temp = 0
                for j in range(4):
                    temp = temp + cv2.filter2D(self.pyramid[i][j], -1, h[j])
                temp = -temp / 8
                pyramid = cv2.filter2D(temp, -1, 1+w)

                lp.pyramid.append(pyramid)
            lp.pyramid.append(self.gaussian[-1])
            for i in range(len(lp.pyramid)):
                print(lp.pyramid[i].shape)
            lp.reconstruct(method='orthogonal')

            self.recon = lp.recon

        else:
            raise("Wrong reconstruct method:",method)

    def show(self,vmin=0,vmax=1):
        plt.figure(figsize=(20, 12))
        if type(self.image) != type(None):
            plt.subplot(5, self.layer, 1)
            plt.imshow(self.image, cmap='gray', vmin=vmin, vmax=vmax)
            plt.title('Original')
            plt.axis('off')
        if type(self.recon) != type(None):
            plt.subplot(5, self.layer, self.layer)
            plt.imshow(self.recon, cmap='gray', vmin=vmin, vmax=vmax)
            plt.title('Reconstructed')
            plt.axis('off')
        if self.pyramid != []:
            for i in range(self.layer):
                for j in range(4):
                    plt.subplot(5, self.layer, i+1+(j+1)*self.layer)
                    if i!=self.layer-1:plt.imshow(self.pyramid[i][j], cmap='gray')
                    else:plt.imshow(self.pyramid[i][j], cmap='gray', vmin=vmin, vmax=vmax)
                    plt.title(self.name+f' k{j+1} L{i+1}')
                    plt.axis('off')
        plt.tight_layout()
        plt.show()

class Morphological(Pyramid):
    def __init__(self,**kwargs):
        super().__init__("Morphological",**kwargs)

    def construct(self,method=None):
        if type(method) == type(None): method = self.con_way
        else: self.con_way = method

        if method == 'ordinary':
            image = self.image
            morph_pyramid = [image]
            kernel_size = 5
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            for i in range(self.layer-1):
                image  = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
                image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
                image = image[::2, ::2]
                morph_pyramid.append(image)
            self.pyramid = morph_pyramid
        else:
            raise("Wrong construct method:",method)

    def reconstruct(self,method=None):
        if type(method) == type(None): method = self.recon_way
        else: self.recon_way = method

        if method == 'ordinary':
            image_reconstructed = self.pyramid[-1]
            kernel_size = 5
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            for i in reversed(range(self.layer-1)):
                print(image_reconstructed.shape,self.pyramid[i].shape)
                expanded = np.zeros(np.array(image_reconstructed.shape[0:2])*2,\
                    dtype=image_reconstructed.dtype)
                expanded[1::2, 1::2] = image_reconstructed
                expanded = cv2.dilate(expanded, kernel, iterations=1)
                image_reconstructed = self.pyramid[i] + expanded

            self.recon = image_reconstructed
        else:
            raise("Wrong reconstruct method:",method)
