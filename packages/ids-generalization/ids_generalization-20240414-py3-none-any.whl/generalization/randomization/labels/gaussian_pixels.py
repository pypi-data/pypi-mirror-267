import torch
from generalization.randomization import corruptions
from generalization.randomization import utils as dataset_utils


@corruptions.add_randomization("gaussian_pixels")
def gaussian_pixels(
    img, target, corruption_prob, apply_corruption=False, use_cifar=False
):
    c, w, h = img.size()

    sampled = None

    if torch.rand(1) <= corruption_prob:
        if use_cifar:
            mean = dataset_utils.CIFAR10_CHANNEL_MEAN
            std = dataset_utils.CIFAR10_CHANNEL_STD
        else:
            mean = dataset_utils.IMAGENET_CHANNEL_MEAN
            std = dataset_utils.IMAGENET_CHANNEL_STD
        normal = torch.distributions.Normal(torch.tensor(mean), torch.tensor(std))
        sampled = normal.sample((h, w)).permute(2, 0, 1).clamp(0, 255).type(torch.uint8)

        if apply_corruption:
            img = sampled

    return img, target, sampled
