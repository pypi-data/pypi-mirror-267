# util.py
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
from tqdm import tqdm
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torchvision import transforms
from .CIFAR10Albumentations import CIFAR10Albumentations

train_losses = []
test_losses = []
train_acc = []
test_acc = []

failed_samples = []
grad_cam_samples = []



def initialize_device(seed=1):
    use_cuda = torch.cuda.is_available()
    print("CUDA Available?", use_cuda)
    torch.manual_seed(seed)
    if use_cuda:
        torch.cuda.manual_seed(seed)
    return torch.device("cuda" if use_cuda else "cpu"), use_cuda

def get_training_transforms():
    mean_dataset = [0.4914 * 255, 0.4822 * 255, 0.4465 * 255]
    train_transforms = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=45, p=0.5),
        A.CoarseDropout(max_holes=1, max_height=16, max_width=16, min_holes=1, min_height=16, min_width=16, fill_value=mean_dataset, p=0.5),
        A.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.247, 0.243, 0.261]),
        ToTensorV2()
    ])
    return train_transforms

def setup_dataloaders(batch_size=64, num_workers=4, pin_memory=True):
    train_transforms = get_training_transforms()
    train_dataset = CIFAR10Albumentations(root='./data', train=True, transform=train_transforms)
    
    test_transforms = get_testing_transforms()
    test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=test_transforms)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=pin_memory)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)

    return train_loader, test_loader

def get_testing_transforms():
    test_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.247, 0.243, 0.261])
    ])
    return test_transforms




def get_dataloader_args(use_cuda, batch_size=256):
    return dict(shuffle=True, batch_size=batch_size if use_cuda else 128, num_workers=4, pin_memory=True) if use_cuda else dict(shuffle=True, batch_size=128)

def train(model, device, train_loader, optimizer, epoch):
    model.train()
    pbar = tqdm(train_loader)
    correct = 0
    processed = 0
    for batch_idx, (data, target) in enumerate(pbar):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        y_pred = model(data)
        loss = F.nll_loss(y_pred, target)
        train_losses.append(loss)
        loss.backward()
        optimizer.step()
        pred = y_pred.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        processed += len(data)
        pbar.set_description(f'Loss={loss.item()} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}%')
        train_acc.append(100*correct/processed)

def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

              # New code block to check for incorrect predictions
            matches = pred.eq(target.view_as(pred))
            for idx, match in enumerate(matches):
                if not match.item():
                    failed_samples.append((data[idx], target[idx].item(), pred[idx].item()))
                    #grad_cam = GradCAM(model, 'layer4')
                    #heatmap = grad_cam.generate_heatmap(data[idx].unsqueeze(0), pred[idx].item())
                    #grad_cam_samples.append((heatmap, target[idx].item(), pred[idx].item()))

    test_loss /= len(test_loader.dataset)
    test_losses.append(test_loss)
    print(f'\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} ({100. * correct / len(test_loader.dataset):.2f}%)\n')
    test_acc.append(100. * correct / len(test_loader.dataset))

def show_images(failed_samples, title):
    CIFAR10_CLS = {
        0: 'Airplane',
        1: 'Automobile',
        2: 'Bird',
        3: 'Cat',
        4: 'Deer',
        5: 'Dog',
        6: 'Frog',
        7: 'Horse',
        8: 'Ship',
        9: 'Truck'
        }
    fig, axs = plt.subplots(5, 2, figsize=(8, 10))
    fig.suptitle(title, fontsize=16)
    for idx, (img, actual, pred) in enumerate(failed_samples[:10]):
        ax = axs[idx // 2, idx % 2]
        img = img.cpu().numpy().transpose((1, 2, 0))
        img = (img - img.min()) / (img.max() - img.min())
        ax.imshow(img, interpolation='none')
        ax.set_title(f'Actual: {CIFAR10_CLS[actual]}, Pred: {CIFAR10_CLS[pred]}')
        ax.axis('off')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def get_training_stats():
    return train_losses,test_losses,train_acc,test_acc,failed_samples
