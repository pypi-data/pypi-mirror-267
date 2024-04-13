# util.py
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
from tqdm import tqdm

def initialize_device(seed=1):
    use_cuda = torch.cuda.is_available()
    print("CUDA Available?", use_cuda)
    torch.manual_seed(seed)
    if use_cuda:
        torch.cuda.manual_seed(seed)
    return torch.device("cuda" if use_cuda else "cpu"), use_cuda

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
        loss.backward()
        optimizer.step()
        pred = y_pred.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        processed += len(data)
        pbar.set_description(f'Loss={loss.item()} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}%')

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
    test_loss /= len(test_loader.dataset)
    print(f'\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} ({100. * correct / len(test_loader.dataset):.2f}%)\n')

def show_images(failed_samples, title):
    fig, axs = plt.subplots(5, 2, figsize=(8, 10))
    fig.suptitle(title, fontsize=16)
    for idx, (img, actual, pred) in enumerate(failed_samples[:10]):
        ax = axs[idx // 2, idx % 2]
        img = img.cpu().numpy().transpose((1, 2, 0))
        img = (img - img.min()) / (img.max() - img.min())
        ax.imshow(img, interpolation='none')
        ax.set_title(f'Actual: {actual}, Pred: {pred}')
        ax.axis('off')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
