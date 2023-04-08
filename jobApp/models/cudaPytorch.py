import torch

# Define a tensor on the CPU
x = torch.randn(10, 10)

# Move the tensor to the GPU
x = x.cuda()

# Define a model on the CPU
model = torch.nn.Linear(10, 1)

# Move the model to the GPU
model = model.cuda()
