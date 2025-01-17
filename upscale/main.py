# implementation from https://youtu.be/ar4NwuqgRN4?si=RNFdkk6i48inFYJp

import warnings

warnings.filterwarnings("ignore")

import torch
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

model_path = "./upscale/RealESRGAN_x4plus.pth"

state_dict = torch.load(model_path, map_location=torch.device('cpu'))["params_ema"]

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
model.load_state_dict(state_dict, strict=True)

upsampler = RealESRGANer(model_path=model_path, scale=4, model=model, tile=0, pre_pad=0, half=True)

img = Image.open("./upscale/image.png.").convert("RGB")
img = np.array(img)

output, _ = upsampler.enhance(img, outscale=4)

output_img = Image.fromarray(output)

output_img.save("./upscale/output.png")