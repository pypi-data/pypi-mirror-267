import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.transforms.functional import to_tensor
from PIL import Image
import matplotlib.pyplot as plt

class Base(object):
    """
    Represents a pyramid constructed from an input image using Gaussian pyramid techniques.

    Attributes:
        name (str): Name of the pyramid.
        image (array): Input image.
        pyramid (list): List to store pyramid layers.
        layer (int): Number of layers in the pyramid.
        recon (array): Output image after reconstruction.
        auto (bool): Flag indicating whether to automatically construct and reconstruct the pyramid.
        con_way (str): Method used for constructing the pyramid.
        recon_way (str): Method used for reconstructing the pyramid.
    """
    def __init__(self, name, **kwargs):
        """
        Initializes a Pyramid object.

        Args:
            name (str): Name of the pyramid.
            **kwargs: Additional keyword arguments to customize object attributes.

        Attributes:
            name (str): Name of the pyramid.
            image (array): Input image.
            pyramid (list): List to store pyramid layers.
            layer (int): Number of layers in the pyramid.
            recon (array): Output image after reconstruction.
            auto (bool): Flag indicating whether to automatically construct and reconstruct the pyramid.
            con_way (str): Method used for constructing the pyramid.
            recon_way (str): Method used for reconstructing the pyramid.
        """
        self.name = name
        self.image = None
        self.pyramid = []
        self.layer = 5
        self.recon = None
        self.auto = True
        self.down_way = 'zero'     # 下采样方案
        self.up_way = 'zero'       # 上采样方案
        self.dec_way = 'ordinary'  # 分解方案
        self.rec_way = 'ordinary'  # 复原方案

        # Update attributes based on additional keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Default operations
        if isinstance(self.image, str):
            transform = transforms.Compose([transforms.ToTensor()])
            self.image = to_tensor(Image.open(self.image)).unsqueeze(0)
        elif isinstance(self.image, torch.Tensor):
            pass
        else:
            raise ValueError("Image should be `str` or `torch.Tensor`")

        if type(self.image) != type(None):
            # Build Base(Defaule Gaussian) Pyramid from input image
            self._build_base_pyramid()
            # Auto Decomposition to Pyramid and Reconstruction for Output Image
            if self.auto:
                self.decomposition()
                self.reconstruction()
        elif self.pyramid != []:
            # Auto Reconstruction for Output Image
            if self.auto:
                self.reconstruction()

    @staticmethod
    def gaussian_blur(image):
        # Define a Gaussian kernel
        kernel = torch.tensor([[1, 4, 6, 4, 1],
                               [4, 16, 24, 16, 4],
                               [6, 24, 36, 24, 6],
                               [4, 16, 24, 16, 4],
                               [1, 4, 6, 4, 1]], dtype=torch.float32) / 256
        # Expand dimensions of the kernel for convolution
        kernel = kernel.unsqueeze(0).unsqueeze(0)

        # Check the number of channels in the input image
        _, channels, _, _ = image.size()

        # If the input image has more than 1 channel, adjust the kernel accordingly
        if channels > 1:
            kernel = kernel.expand(channels, -1, -1, -1)

        # Apply 2D convolution with the Gaussian kernel
        blurred = F.conv2d(image, kernel, stride=1, padding=2, groups=image.size(1))
        return blurred

    @staticmethod
    def down_sample(image):
        # Subsample the image using 2x2 max pooling
        # downsampled = F.max_pool2d(blurred, kernel_size=2, stride=2)
        return image[:, :, ::2, ::2]

    @staticmethod
    def up_sample(image):
        # Perform zero-padding
        batch_size, channels, height, width = image.size()
        padded_img = torch.zeros(batch_size, channels, 2 * height, 2 * width)
        padded_img[:, :, ::2, ::2] = image
        return padded_img

    @staticmethod
    def pyr_down(image):
        """
        Downsamples the input image using a Gaussian kernel and max pooling.

        Args:
            image (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).

        Returns:
            torch.Tensor: Downsampled image tensor.
        """
        blurred = Base.gaussian_blur(image)
        downsampled = Base.down_sample(blurred)
        return downsampled

    @staticmethod
    def pyr_up(image):
        """
        Upsamples the input image using zero-padding and then applying Gaussian blur.

        Args:
            src_img (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).

        Returns:
            torch.Tensor: Upsampled image tensor.
        """
        padded_img = Base.up_sample(image)
        blurred_img = Base.gaussian_blur(padded_img)
        return blurred_img * 4

    def _build_gaussian_pyramid(self):
        """
        Constructs a Gaussian pyramid from the input image.
        """
        image = self.image
        self.gaussian = [image]
        for _ in range(self.layer):
            image = self.pyr_down(image)
            self.gaussian.append(image)

    def _build_base_pyramid(self):
        self._build_gaussian_pyramid()

    def decomposition(self, method=None):
        """
        Method to decompose the image based on the specified method.
        """
        if method is not None:
            self.dec_way = method
        if self.dec_way is not None:
            decomposition_method = getattr(self, f"decomposition_{self.dec_way}", None)
            if decomposition_method is not None and callable(decomposition_method):
                decomposition_method()
            else:
                raise ValueError(f"Invalid decomposition method (reconstruct_{self.dec_way}):", method)
        else:
            raise ValueError("No decomposition method specified")

    def reconstruction(self, method=None):
        """
        Method to reconstruct the image based on the specified method.
        """
        if method is not None:
            self.rec_way = method
        if self.rec_way is not None:
            reconstruct_method = getattr(self, f"reconstruction_{self.rec_way}", None)
            if reconstruct_method is not None and callable(reconstruct_method):
                reconstruct_method()
            else:
                raise ValueError(f"Invalid reconstruct method (reconstruct_{self.rec_way}):", method)
        else:
            raise ValueError("No reconstruct method specified")

    def __getitem__(self, index):
        return self.pyramid[index]

    def __len__(self):
        return len(self.pyramid)

    def append(self, item):
        self.pyramid.append(item)

class Demo(Base):
    def __init__(self,**kwargs):
        super().__init__("Demo",**kwargs)

    def decomposition_ordinary(self):
        pass

    def reconstruction_ordinary(self):
        pass

class Laplacian(Base):
    def __init__(self,**kwargs):
        super().__init__("Laplacian",**kwargs)

    def decomposition_ordinary(self):
        laplacian_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.gaussian[i].shape
            expanded = self.pyr_up(self.gaussian[i+1])[:,:,:m,:n]
            laplacian = self.gaussian[i] - expanded
            laplacian_pyramid.append(laplacian)

        self.pyramid = laplacian_pyramid

    def reconstruction_ordinary(self):
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed

    def reconstruction_orthogonal(self):
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            image_reconstructed -= self.pyr_down(self.pyramid[i])
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed

class Contrust(Base):
    def __init__(self,**kwargs):
        super().__init__("Contrust",**kwargs)

    def decomposition_ordinary(self):
        laplacian_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.gaussian[i].shape
            expanded = self.pyr_up(self.gaussian[i+1])[:,:,:m,:n]
            laplacian = torch.where(expanded == 0, torch.zeros_like(self.gaussian[i]),\
                self.gaussian[i] / expanded - 1)
            laplacian_pyramid.append(laplacian)

        self.pyramid = laplacian_pyramid

    def reconstruction_ordinary(self):
        image_reconstructed = self.gaussian[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.pyr_up(image_reconstructed)[:,:,:m,:n]
            image_reconstructed = (self.pyramid[i] + 1) * expanded

        self.recon = image_reconstructed

class FSD(Base):
    def __init__(self,**kwargs):
        super().__init__("FSD",**kwargs)

    def decomposition_ordinary(self):
        fsd_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.gaussian[i].shape
            fsd = self.gaussian[i] - self.gaussian_blur(self.gaussian[i])
            fsd_pyramid.append(fsd)

        self.pyramid = fsd_pyramid

    def reconstruction_ordinary(self):
        image_reconstructed = self.up_sample(self.gaussian[-1])*4
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            image_reconstructed = image_reconstructed[:,:,:m,:n]
            image_reconstructed += self.pyramid[i]
            image_reconstructed = self.gaussian_blur(image_reconstructed)
            image_reconstructed += self.pyramid[i]
            if i!=0:
                image_reconstructed = self.up_sample(image_reconstructed)*4

        self.recon = image_reconstructed

class Graident(Base):
    def __init__(self,**kwargs):
        super().__init__("Graident",**kwargs)

    @staticmethod
    def gaussian_blur(image,bias=0):
        # Define a Gaussian kernel
        kernel = torch.tensor([[1, 2, 1],
                               [2, 4, 2],
                               [1, 2, 1]], dtype=torch.float32) / 16 + bias
        # Expand dimensions of the kernel for convolution
        kernel = kernel.unsqueeze(0).unsqueeze(0)

        # Check the number of channels in the input image
        _, channels, _, _ = image.size()

        # If the input image has more than 1 channel, adjust the kernel accordingly
        if channels > 1:
            kernel = kernel.expand(channels, -1, -1, -1)

        # Apply 2D convolution with the Gaussian kernel
        blurred = F.conv2d(image, kernel, stride=1, padding=1, groups=image.size(1))
        return blurred

    @staticmethod
    def get_graident(image):
        if type(image) != list:
            image = [image]*4
        batch_size, channels, height, width = image[0].shape
        h1 = torch.tensor([[0,0,0],[0, 1,-1],[0,0,0]], dtype=torch.float32)
        h2 = torch.tensor([[0,0,0],[0, 0,-1],[0,1,0]], dtype=torch.float32) / torch.sqrt(torch.tensor(2))
        h3 = torch.tensor([[0,0,0],[0,-1, 0],[0,1,0]], dtype=torch.float32)
        h4 = torch.tensor([[0,0,0],[0,-1, 0],[0,0,1]], dtype=torch.float32) / torch.sqrt(torch.tensor(2))
        h = [k.unsqueeze(0).unsqueeze(0).repeat(channels, 1, 1, 1) for k in [h1,h2,h3,h4]]
        graidents = [F.conv2d(_i, _h, stride=1, padding=1, groups=_i.shape[1]) for _i,_h in zip(image,h)]
        return graidents

    def decomposition_ordinary(self):
        graident_pyramid = []
        for i in range(self.layer):
            temp = self.gaussian_blur(self.gaussian[i]) + self.gaussian[i]
            graident_pyramid.append(self.get_graident(temp))
        print(len(graident_pyramid[0]))
        self.pyramid = graident_pyramid

    def reconstruction_ordinary(self):
        lp = Laplacian(image=self.image,auto=False,layer=self.layer)
        for i in range(self.layer):
            temp = torch.stack(self.get_graident(self.pyramid[i]))
            temp = -torch.sum(temp, dim=0) / 8
            pyramid = self.gaussian_blur(temp,bias=0)+temp # change FSD to Laplacian
            lp.append(pyramid)
        lp.reconstruction()
        self.recon = lp.recon
class Morphological(Base):
    def __init__(self,**kwargs):
        super().__init__("Morphological",**kwargs)

    @staticmethod
    def morph_dilation(image, kernel_size=5):
        # Define the kernel for dilation
        kernel = torch.ones((1, 1, kernel_size, kernel_size), dtype=torch.float32)

        # Perform dilation operation
        dilated_image = F.max_pool2d(image, kernel_size=kernel_size, stride=1, padding=kernel_size//2)

        return dilated_image

    @staticmethod
    def morph_erosion(image, kernel_size=5):
        # Define the kernel for erosion
        kernel = torch.ones((1, 1, kernel_size, kernel_size), dtype=torch.float32)

        # Perform erosion operation
        eroded_image = F.avg_pool2d(image, kernel_size=kernel_size, stride=1, padding=kernel_size//2)

        return eroded_image

    @staticmethod
    def morph_opening(image, kernel_size=5):
        # Perform erosion followed by dilation (opening)
        eroded_image = Morphological.morph_erosion(image, kernel_size=kernel_size)
        opened_image = Morphological.morph_dilation(eroded_image, kernel_size=kernel_size)

        return opened_image

    @staticmethod
    def morph_closing(image, kernel_size=5):
        # Perform dilation followed by erosion (closing)
        dilated_image = Morphological.morph_dilation(image, kernel_size=kernel_size)
        closed_image = Morphological.morph_erosion(dilated_image, kernel_size=kernel_size)

        return closed_image

    def _build_morphology_pyramid(self):
        """
        Constructs a Morphology pyramid from the input image.
        """
        image = self.image
        self.morphology = [image]
        for _ in range(self.layer):
            image  = self.morph_opening(image)
            image = self.morph_closing(image)
            image = self.down_sample(image)
            self.morphology.append(image)

    def _build_base_pyramid(self):
        self._build_morphology_pyramid()

    def decomposition_ordinary(self):
        morph_pyramid = []
        for i in range(self.layer):
            _,_,m,n = self.morphology[i].shape
            expanded = self.up_sample(self.morphology[i+1])[:,:,:m,:n]
            expanded = self.morph_closing(expanded)
            expanded = self.morph_opening(expanded)
            morph = self.morphology[i] - expanded
            morph_pyramid.append(morph)

        self.pyramid = morph_pyramid

    def reconstruction_ordinary(self):
        image_reconstructed = self.morphology[-1]
        for i in reversed(range(self.layer)):
            _,_,m,n = self.pyramid[i].shape
            expanded = self.up_sample(image_reconstructed)[:,:,:m,:n]
            expanded = self.morph_closing(expanded)
            expanded = self.morph_opening(expanded)
            image_reconstructed = self.pyramid[i] + expanded

        self.recon = image_reconstructed
