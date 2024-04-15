from typing_extensions import Set
import torch

from tqdm.auto import tqdm
from typing import Dict, List, Tuple
import os

from pathlib import Path
import matplotlib.pyplot as plt
from dataclasses import dataclass

from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torchinfo import summary

import torch
import torchvision
import torch.nn as nn
from torchinfo import summary
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torchvision.transforms import ToTensor
assert int(torch.__version__.split(".")[1]) >= 12 or int(torch.__version__.split(".")[0]) == 2, "torch version should be 1.12+"
assert int(torchvision.__version__.split(".")[1]) >= 13, "torchvision version should be 0.13+"
print(f"torch version: {torch.__version__}")
print(f"torchvision version: {torchvision.__version__}")

NUM_WORKERS = os.cpu_count()

@dataclass
class Engine:
    def __init__(
        self,
    ):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def train_step(self,
                model: torch.nn.Module,
                dataloader: torch.utils.data.DataLoader,
                loss_func: str,
                opt: str,
                device: torch.device) -> Tuple[float, float]:

        # Setup the optimizer to optimize our ViT model parameters using hyperparameters from the ViT paper
        if opt == "Adam":
            optimizer = torch.optim.Adam(params=model.parameters(),
                                     lr=3e-3, # Base LR from Table 3 for ViT-* ImageNet-1k
                                     betas=(0.9, 0.999), # default values but also mentioned in ViT paper section 4.1 (Training & Fine-tuning)
                                     weight_decay=0.3) # from the ViT paper section 4.1 (Training & Fine-tuning) and Table 3 for ViT-* ImageNet-1k
        else:
            optimizer = torch.optim.Adam(params=model.parameters(),
                                     lr=3e-3, # Base LR from Table 3 for ViT-* ImageNet-1k
                                     betas=(0.9, 0.999), # default values but also mentioned in ViT paper section 4.1 (Training & Fine-tuning)
                                     weight_decay=0.3)

        # Setup the loss function for multi-class classification
        if loss_func == "CrossEntropy":
            loss_fn = torch.nn.CrossEntropyLoss()
        else:
            loss_fn = torch.nn.CrossEntropyLoss()

        model.train()

        train_loss, train_acc = 0, 0

        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(device), y.to(device)

            y_pred = model(X)

            loss = loss_fn(y_pred, y)
            train_loss += loss.item()

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
            train_acc += (y_pred_class == y).sum().item()/len(y_pred)

        train_loss = train_loss / len(dataloader)
        train_acc = train_acc / len(dataloader)
        return train_loss, train_acc

    def test_step(self, model: torch.nn.Module,
                dataloader: torch.utils.data.DataLoader,
                loss_func: str,
                device: torch.device) -> Tuple[float, float]:

        model.eval()

        if loss_func == "CrossEntropyLoss":
            loss_fn = torch.nn.CrossEntropyLoss()

        else:
            loss_fn = torch.nn.CrossEntropyLoss()

        test_loss, test_acc = 0, 0

        with torch.inference_mode():
            for batch, (X, y) in enumerate(dataloader):
                X, y = X.to(device), y.to(device)

                test_pred_logits = model(X)

                loss = loss_fn(test_pred_logits, y)
                test_loss += loss.item()

                test_pred_labels = test_pred_logits.argmax(dim=1)
                test_acc += ((test_pred_labels == y).sum().item()/len(test_pred_labels))

        test_loss = test_loss / len(dataloader)
        test_acc = test_acc / len(dataloader)
        return test_loss, test_acc

    def train(self, model: torch.nn.Module,
            train_dataloader: torch.utils.data.DataLoader,
            test_dataloader: torch.utils.data.DataLoader,
            optimizer: str,
            loss_fn: str,
            epochs: int) -> Dict[str, List]:

        results = {"train_loss": [],
            "train_acc": [],
            "test_loss": [],
            "test_acc": []
        }

        for epoch in tqdm(range(epochs)):
            train_loss, train_acc = self.train_step(model=model,
                                                dataloader=train_dataloader,
                                                loss_func=loss_fn,
                                                opt=optimizer,
                                                device=self.device)
            test_loss, test_acc = self.test_step(model=model,
                dataloader=test_dataloader,
                loss_func=loss_fn,
                device=self.device)

            print(
                f"Epoch: {epoch+1} | "
                f"train_loss: {train_loss:.4f} | "
                f"train_acc: {train_acc:.4f} | "
                f"test_loss: {test_loss:.4f} | "
                f"test_acc: {test_acc:.4f}"
            )

            results["train_loss"].append(train_loss)
            results["train_acc"].append(train_acc)
            results["test_loss"].append(test_loss)
            results["test_acc"].append(test_acc)

        return results

    def save_model(self, model: torch.nn.Module,
                target_dir: str,
                model_name: str):
        target_dir_path = Path(target_dir)
        target_dir_path.mkdir(parents=True,
                                exist_ok=True)

        assert model_name.endswith(".pth") or model_name.endswith(".pt"), "model_name should end with '.pt' or '.pth'"
        model_save_path = target_dir_path / model_name

        print(f"[INFO] Saving model to: {model_save_path}")
        torch.save(obj=model.state_dict(),
                    f=model_save_path)

    def set_seeds(self, seed: int=42):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)

    def show_model_summary(self, model: torch.nn.Module):
        summary(model=model,
               input_size=(32, 3, 224, 224), # (batch_size, color_channels, height, width)
               # col_names=["input_size"], # uncomment for smaller output
               col_names=["input_size", "output_size", "num_params", "trainable"],
               col_width=20,
               row_settings=["var_names"]
        )

    def plot_loss_curves(self, results: Dict[str, List[float]]):
        """Plots training curves of a results dictionary.

        Args:
            results (dict): dictionary containing list of values, e.g.
                {"train_loss": [...],
                "train_acc": [...],
                "test_loss": [...],
                "test_acc": [...]}
        """

        # Get the loss values of the results dictionary (training and test)
        loss = results['train_loss']
        test_loss = results['test_loss']

        # Get the accuracy values of the results dictionary (training and test)
        accuracy = results['train_acc']
        test_accuracy = results['test_acc']

        # Figure out how many epochs there were
        epochs = range(len(results['train_loss']))

        # Setup a plot
        plt.figure(figsize=(15, 7))

        # Plot loss
        plt.subplot(1, 2, 1)
        plt.plot(epochs, loss, label='train_loss')
        plt.plot(epochs, test_loss, label='test_loss')
        plt.title('Loss')
        plt.xlabel('Epochs')
        plt.legend()

        # Plot accuracy
        plt.subplot(1, 2, 2)
        plt.plot(epochs, accuracy, label='train_accuracy')
        plt.plot(epochs, test_accuracy, label='test_accuracy')
        plt.title('Accuracy')
        plt.xlabel('Epochs')
        plt.legend()

    def create_dataloaders(self,
        train_dir: str,
        test_dir: str,
        image_size: int,
        batch_size: int,
        num_workers: int=NUM_WORKERS
    ):

        manual_transforms = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
        ])

        train_data = datasets.ImageFolder(train_dir, transform=manual_transforms)
        test_data = datasets.ImageFolder(test_dir, transform=manual_transforms)

        class_names = train_data.classes

        train_dataloader = DataLoader(
            train_data,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
        )
        test_dataloader = DataLoader(
            test_data,
            batch_size=batch_size,
            shuffle=False, # don't need to shuffle test data
            num_workers=num_workers,
            pin_memory=True,
        )

        return train_dataloader, test_dataloader, class_names
