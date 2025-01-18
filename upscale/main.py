import warnings
import time

warnings.filterwarnings("ignore")

import torch
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

model_path = "./upscale/RealESRGAN_x4plus.pth"

print(f"[{timestamp()}] Starting upscaling script...")

print(f"[{timestamp()}] Loading state dictionary...")
state_dict = torch.load(model_path, map_location=torch.device('cpu'))["params_ema"]
print(f"[{timestamp()}] State dictionary loaded successfully.")

print(f"[{timestamp()}] Creating upscaling model...")

print(f"[{timestamp()}] Creating RRDBNet model...")
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
model.load_state_dict(state_dict, strict=True)
print(f"[{timestamp()}] RRDBNet model created successfully.")

print(f"[{timestamp()}] Creating RealESRGAN model...")
upsampler = RealESRGANer(model_path=model_path, scale=4, model=model, tile=0, pre_pad=0, half=True)
print(f"[{timestamp()}] Model created successfully.")

print(f"[{timestamp()}] Image processing...")

print(f"[{timestamp()}] Loading and preparing image...")
img = Image.open("./upscale/image.png").convert("RGB")
img = np.array(img)
print(f"[{timestamp()}] Image loaded successfully.")

print(f"[{timestamp()}] Upscaling image...")
output, _ = upsampler.enhance(img, outscale=4)
print(f"[{timestamp()}] Image upscaled successfully.")

print(f"[{timestamp()}] Saving upscaled image...")
output_img = Image.fromarray(output)
output_img.save("./upscale/output.png")
print(f"[{timestamp()}] Upscaled image saved successfully. Upscaling script completed successfully. Check the output.png file in the upscale directory. Note that the output image may not be as sharp as the original due to the upscaling process.")

print(f"[{timestamp()}] Image processing completed successfully.")