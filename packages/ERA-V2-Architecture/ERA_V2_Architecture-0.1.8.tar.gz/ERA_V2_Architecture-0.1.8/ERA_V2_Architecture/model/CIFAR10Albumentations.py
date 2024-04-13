from torchvision import datasets
from torch.utils.data import Dataset
import numpy as np

class CIFAR10Albumentations:
    def __init__(self, root='./data', train=True, transform=None):
        self.data = datasets.CIFAR10(root, train=train, download=True)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image, label = self.data[idx]
        if self.transform:
            # Convert PIL image to numpy array
            image_np = np.array(image)
            # Apply the transformations
            augmented = self.transform(image=image_np)
            image = augmented['image']
        return image, label