import torch

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
# Create a tensor on GPU
x = torch.randn(3, 3, device=device)
print(x)

