import torch
from torch import nn


class SimpleNetwork(nn.Module):
    """Input layer -> single hidden layer -> output layer -> softmax."""

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.hidden = nn.Linear(input_size, hidden_size)
        self.activation = nn.ReLU()
        self.output = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.activation(self.hidden(x))
        x = self.output(x)
        return self.softmax(x)


class SimpleCNN1D(nn.Module):
    """Two stride-2 Conv1d hidden layers with ReLU activations."""

    def __init__(self, in_channels: int = 1, hidden_channels: int = 4, kernel_size: int = 3):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels, hidden_channels, kernel_size, stride=2)
        self.conv2 = nn.Conv1d(hidden_channels, 2 * hidden_channels, kernel_size, stride=2)
        self.activation = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, channels, length); length shrinks roughly by half per layer
        x = self.activation(self.conv1(x))
        return self.activation(self.conv2(x))


class CNNRegressor(nn.Module):
    """SimpleCNN1D -> flatten -> fully connected layer -> single real-valued output."""

    def __init__(self, input_length: int, in_channels: int = 1, hidden_channels: int = 4,
                 kernel_size: int = 3, fc_size: int = 16):
        super().__init__()
        self.features = SimpleCNN1D(in_channels, hidden_channels, kernel_size)
        # Size of the flattened conv output depends on the input length
        channels, length = get_output_size(self.features, (in_channels, input_length))
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(channels * length, fc_size)
        self.activation = nn.ReLU()
        self.regression = nn.Linear(fc_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.flatten(self.features(x))
        x = self.activation(self.fc(x))
        return self.regression(x).squeeze(-1)  # shape (batch,)


def _infer_input_shape(model: nn.Module) -> tuple[int, ...] | None:
    """Guess the per-sample input shape from the first Linear/Conv layer, if any."""
    for layer in model.modules():
        if isinstance(layer, nn.Linear):
            return (layer.in_features,)
        if isinstance(layer, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
            # Spatial size can't be determined from the layer; use a modest default.
            dims = len(layer.kernel_size)
            return (layer.in_channels,) + (32,) * dims
    return None


def get_output_size(
    model: nn.Module, input_shape: tuple[int, ...] | None = None, batch_size: int = 2
) -> tuple[int, ...]:
    """Send dummy data through `model` and return the per-sample output shape.

    `input_shape` excludes the batch dimension. If omitted, it is inferred from
    the first Linear or Conv layer; a ValueError is raised if that fails.
    The batch dimension is not included in the returned shape.
    """
    if input_shape is None:
        input_shape = _infer_input_shape(model)
        if input_shape is None:
            raise ValueError("Could not infer input shape; please pass input_shape.")

    was_training = model.training
    model.eval()  # avoids batch-norm/dropout side effects and batch-size-1 issues
    try:
        with torch.no_grad():
            device = next(model.parameters(), torch.empty(0)).device
            out = model(torch.randn(batch_size, *input_shape, device=device))
    finally:
        model.train(was_training)
    return tuple(out.shape[1:])


def print_model_summary(model):
    print("Model architecture:")
    print(model)
    print("\nLayer parameter shapes:")
    for name, layer in model.named_modules():
        if name:
            shapes = {
                parameter_name: tuple(parameter.shape)
                for parameter_name, parameter in layer.named_parameters(recurse=False)
            }
            print(f"{name} ({layer.__class__.__name__}): {shapes or 'no parameters'}")

if __name__ == "__main__":
    print('\n--- Simple fully connected network ---')
    model = SimpleNetwork(input_size=4, hidden_size=8, output_size=3)

    print_model_summary(model)

    print('Output size via dummy input method:', get_output_size(model))  # (3,)
    
    print('Output probabilities for a batch of 2 samples:')
    probs = model(torch.randn(2, 4))
    print(probs)
    print(probs.sum(dim=-1))  # each row sums to 1

    print('\n--- 1D convolutional network ---')
    cnn = SimpleCNN1D(in_channels=1, hidden_channels=4, kernel_size=3)
    print_model_summary(cnn)

    signal_length = 64
    x = torch.randn(2, 1, signal_length)
    print('Input shape:', tuple(x.shape))
    h1 = cnn.activation(cnn.conv1(x))
    print('After conv1 (stride 2):', tuple(h1.shape))  # (2, 4, 31)
    h2 = cnn.activation(cnn.conv2(h1))
    print('After conv2 (stride 2):', tuple(h2.shape))  # (2, 8, 15)
    print('Output size via dummy input method:',
          get_output_size(cnn, input_shape=(1, signal_length)))  # (8, 15)

    print('\n--- CNN regression network ---')
    regressor = CNNRegressor(input_length=signal_length)
    print_model_summary(regressor)
    preds = regressor(x)
    print('Predictions for batch of 2 (one real number each):', preds)
    print('Output shape (batch):', tuple(preds.shape))
    print('Per-sample output size via dummy input method:',
          get_output_size(regressor, input_shape=(1, signal_length)))  # () = scalar
