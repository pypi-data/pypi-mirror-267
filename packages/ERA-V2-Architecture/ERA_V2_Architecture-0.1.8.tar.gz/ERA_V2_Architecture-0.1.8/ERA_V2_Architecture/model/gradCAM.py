import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import cv2
from torchvision import transforms


class GradCAM:
    def __init__(self, model, layer_name):
        self.model = model
        self.layer_name = layer_name
        self.gradient = None
        self.activation = None
        self.hook_layers()

    def hook_layers(self):
        def get_activation_hook(module, input, output):
            self.activation = output

        def get_gradient_hook(module, grad_in, grad_out):
            self.gradient = grad_out[0]

        for name, module in self.model.named_modules():
            if name == self.layer_name:
                module.register_forward_hook(get_activation_hook)
                module.register_backward_hook(get_gradient_hook)

    def visualize(self, input_image, class_idx):
        # Forward pass
        output = self.model(input_image)
        class_output = output[:, class_idx]

        # Backward pass
        self.model.zero_grad()
        class_output.backward(retain_graph=True)

        # Generate Grad-CAM heatmap
        pooled_gradients = torch.mean(self.gradient, dim=[0, 2, 3])
        for i in range(self.activation.shape[1]):
            self.activation[:, i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(self.activation, dim=1).squeeze().cpu()
        heatmap = relu(heatmap)
        heatmap /= torch.max(heatmap)

        # Render heatmap
        import cv2
        import numpy as np
        import matplotlib.pyplot as plt
        img = input_image.cpu().data.numpy()[0].transpose((1, 2, 0))
        img = (img - img.min()) / (img.max() - img.min())
        heatmap = heatmap.numpy()
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        superimposed_img = heatmap * 0.4 + img * 255
        plt.imshow(superimposed_img / 255)
        plt.show()

    def generate_heatmap(self, input_image, class_idx):
        self.model.eval()
        output = self.model(input_image)
        output.requires_grad_(True)
        class_output = output[:, class_idx]
        self.model.zero_grad()
        class_output.backward(retain_graph=True)

        pooled_gradients = torch.mean(self.gradient, dim=[0, 2, 3])
        for i in range(self.activation.shape[1]):
            self.activation[:, i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(self.activation, dim=1).squeeze()
        heatmap = F.relu(heatmap)
        heatmap /= torch.max(heatmap)
        heatmap = heatmap.cpu().numpy()
        heatmap = cv2.resize(heatmap, (input_image.shape[2], input_image.shape[3]))  # Resize to the input size
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        return heatmap
