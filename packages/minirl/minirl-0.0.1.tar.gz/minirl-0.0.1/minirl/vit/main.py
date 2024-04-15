from components.engine import Engine

from network.embedding import PatchEmbedding
from network.attention import MultiheadSelfAttentionBlock
from network.mlp import MLPBlock
from network.transformer import TransformerEncoderBlock
from network.vit import ViT

engine = Engine()

##* Load the data *##
train_dir = "minirl/vit/data/test"
test_dir = "minirl/vit/data/train"

# Create image size (from Table 3 in the ViT paper)
IMG_SIZE = 224

# Set the batch size
BATCH_SIZE = 32 # this is lower than the ViT paper but it's because we're starting small

# Create data loaders
train_dataloader, test_dataloader, class_names = engine.create_dataloaders(
    train_dir=train_dir,
    test_dir=test_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Get a batch of images
image_batch, label_batch = next(iter(train_dataloader))

# Get a single image from the batch
image, label = image_batch[0], label_batch[0]

engine.set_seeds()

# Create an instance of ViT with the number of classes we're working with (pizza, steak, sushi)
vit = ViT(num_classes=len(class_names))

engine.show_model_summary(vit)

# Train the model and save the training results to a dictionary
vit_results = engine.train(model=vit,
                      train_dataloader=train_dataloader,
                      test_dataloader=test_dataloader,
                      optimizer="Adam",
                      loss_fn="CrossEntropyLoss",
                      epochs=10)
# 9.5 Plot the loss curves of our ViT model

# Plot our ViT model's loss curves
engine.plot_loss_curves(vit_results)


# 0.6 Save feature extractor ViT model and check file size
#
# # Save the model
#from components import utils

engine.save_model(model=vit_results,
                  target_dir="models",
                  model_name="pretrained_vit_feature_extractor.pth")
