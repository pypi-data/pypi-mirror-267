# 💡 HiDiffusion

> **HiDiffusion: Unlocking Higher-Resolution Creativity and Efficiency in Pretrained Diffusion Models**   
> Shen Zhang, Zhaowei Chen, Zhenyu Zhao, Yuhao Chen, Yao Tang, Jiajun Liang     
> 🧬[[Arxiv]](https://arxiv.org/abs/2311.17528) 🎷[[Project Page]]()


<div align="center">
  <img src="assets/image_gallery.jpg" width="800" ></img>
  <br>
  <em>
      (Select HiDiffusion samples for various diffusion models, resolutions, and aspect ratios.) 
  </em>
</div>
<br>


# 👉 Why HiDiffusion

- A  **training-free method that increases the resolution and speed of pretrained diffusion models.**
- Designed as a **plug-and-play implementation**. It can be integrated into diffusion pipelines by **only adding a single line of code**!

<div align="center">
  <img src="assets/quality_efficiency.jpg" width="800" ></img>
  <br>
  <em>
      (Faster, and better image details.) 
  </em>
</div>
<br>

## 📢 Supported Models

- ✅ [Stable Diffusion XL](https://huggingface.co/papers/2307.01952)
- ✅ [Stable Diffusion XL Turbo](https://huggingface.co/stabilityai/sdxl-turbo)
- ✅ [Stable Diffusion v2](https://huggingface.co/stabilityai/stable-diffusion-2-1)
- ✅ [Stable Diffusion v1](https://huggingface.co/runwayml/stable-diffusion-v1-5)

**Note**: HiDiffusion can also support the dowmstream diffusion models based on these repositories.

## 💣 Supported Tasks

- ✅ Text-to-image
- ✅ ControlNet
- ✅ Inpainting


## 🔎 Main requirements
This repository is tested on
* Python==3.8
* torch==1.13.1
* diffusers==0.25.0
* transformers==4.27.4
* accelerate==0.18.0
* xformers==0.0.16rc425

## 🔑 Install HiDiffusion
After installing the packages in the main requirements, install HiDiffusion:
```shell
pip3 install hidiffusion
```
### Installing from source
Alternatively, you can install from github source. Clone the repository and install:
```bash
git clone https://github.com/ShenZhang-Shin/HiDiffusion.git
cd HiDiffusion
python3 setup.py install
```


## 🚀 Usage

Generating outputs with HiDiffusion is super easy based on 🤗 [diffusers](https://github.com/huggingface/diffusers/tree/main).

## Text-to-image generation

### Stable Diffusion XL

```python
from hidiffusion import apply_hidiffusion, remove_hidiffusion
from diffusers import StableDiffusionXLPipeline, DDIMScheduler
import torch
pretrain_model = "stabilityai/stable-diffusion-xl-base-1.0"
scheduler = DDIMScheduler.from_pretrained(pretrain_model, subfolder="scheduler")
pipe = StableDiffusionXLPipeline.from_pretrained(pretrain_model, scheduler = scheduler, torch_dtype=torch.float16, variant="fp16").to("cuda")

# # Optional. enable_xformers_memory_efficient_attention can save memory usage and increase inference speed. enable_model_cpu_offload and enable_vae_tiling can save memory usage.
# pipe.enable_xformers_memory_efficient_attention()
# pipe.enable_model_cpu_offload()
# pipe.enable_vae_tiling()

# Apply hidiffusion with a single line of code.
apply_hidiffusion(pipe)

prompt = "Standing tall amidst the ruins, a stone golem awakens, vines and flowers sprouting from the crevices in its body."
negative_prompt = "blurry, ugly, duplicate, poorly drawn face, deformed, mosaic, artifacts, bad limbs"
image = pipe(prompt, guidance_scale=7.5, height=2048, width=2048, eta=1.0, negative_prompt=negative_prompt).images[0]
image.save(f"golem.jpg")
```

<details>
<summary>Output:</summary>
<div align="center">
  <img src="assets/sdxl.jpg" width="800" ></img>
</div>
</details>

Set height = 4096, width = 4096, and you can get output with 4096x4096 resolution.

### Stable Diffusion XL Turbo

```python
from hidiffusion import apply_hidiffusion, remove_hidiffusion
from diffusers import AutoPipelineForText2Image
import torch
pretrain_model = "stabilityai/sdxl-turbo"
pipe = AutoPipelineForText2Image.from_pretrained(pretrain_model, torch_dtype=torch.float16, variant="fp16").to('cuda')

# # Optional. enable_xformers_memory_efficient_attention can save memory usage and increase inference speed. enable_model_cpu_offload and enable_vae_tiling can save memory usage.
# pipe.enable_xformers_memory_efficient_attention()
# pipe.enable_model_cpu_offload()
# pipe.enable_vae_tiling()

# Apply hidiffusion with a single line of code.
apply_hidiffusion(pipe)

prompt = "In the depths of a mystical forest, a robotic owl with night vision lenses for eyes watches over the nocturnal creatures."
image = pipe(prompt, num_inference_steps=4, height=1024, width=1024, guidance_scale=0.0).images[0]
image.save(f"./owl.jpg")
```

<details>
<summary>Output:</summary>
<div align="center">
  <img src="assets/sdxl_turbo.jpg" width="800" ></img>
</div>
</details>

### Stable Diffusion v2-1

```python
from hidiffusion import apply_hidiffusion, remove_hidiffusion
from diffusers import DiffusionPipeline, DDIMScheduler
import torch
pretrain_model = "stabilityai/stable-diffusion-2-1-base"
scheduler = DDIMScheduler.from_pretrained(pretrain_model, subfolder="scheduler")
pipe = DiffusionPipeline.from_pretrained(pretrain_model, scheduler = scheduler, torch_dtype=torch.float16).to("cuda")

# # Optional. enable_xformers_memory_efficient_attention can save memory usage and increase inference speed. enable_model_cpu_offload and enable_vae_tiling can save memory usage.
# pipe.enable_xformers_memory_efficient_attention()
# pipe.enable_model_cpu_offload()
# pipe.enable_vae_tiling()

# Apply hidiffusion with a single line of code.
apply_hidiffusion(pipe)

prompt = "An adorable happy brown border collie sitting on a bed, high detail."
negative_prompt = "ugly, tiling, out of frame, poorly drawn face, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, artifacts, bad proportions."
image = pipe(prompt, guidance_scale=7.5, height=1024, width=1024, eta=1.0, negative_prompt=negative_prompt).images[0]
image.save(f"collie.jpg")
```

<details>
<summary>Output:</summary>
<div align="center">
  <img src="assets/sd21.jpg" width="800" ></img>
</div>
</details>

Set height = 2048, width = 2048, and you can get output with 2048x2048 resolution.



### Stable Diffusion v1-5

```python
from hidiffusion import apply_hidiffusion, remove_hidiffusion
from diffusers import DiffusionPipeline, DDIMScheduler
import torch
pretrain_model = "runwayml/stable-diffusion-v1-5"
scheduler = DDIMScheduler.from_pretrained(pretrain_model, subfolder="scheduler")
pipe = DiffusionPipeline.from_pretrained(pretrain_model, scheduler = scheduler, torch_dtype=torch.float16).to("cuda")

# # Optional. enable_xformers_memory_efficient_attention can save memory usage and increase inference speed. enable_model_cpu_offload and enable_vae_tiling can save memory usage.
# pipe.enable_xformers_memory_efficient_attention()
# pipe.enable_model_cpu_offload()
# pipe.enable_vae_tiling()

# Apply hidiffusion with a single line of code.
apply_hidiffusion(pipe)

prompt = "thick strokes, bright colors, an exotic fox, cute, chibi kawaii. detailed fur, hyperdetailed , big reflective eyes, fairytale, artstation,centered composition, perfect composition, centered, vibrant colors, muted colors, high detailed, 8k."
negative_prompt = "ugly, tiling, poorly drawn face, out of frame, disfigured, deformed, blurry, bad anatomy, blurred."
image = pipe(prompt, guidance_scale=7.5, height=1024, width=1024, eta=1.0, negative_prompt=negative_prompt).images[0]
image.save(f"fox.jpg")
```

<details>
<summary>Output:</summary>
<div align="center">
  <img src="assets/sd15.jpg" width="800" ></img>
</div>
</details>

Set height = 2048, width = 2048, and you can get output with 2048x2048 resolution.

### Remove HiDiffusion

If you want to remove HiDiiffusion, simply use `remove_hidiffusion(pipe)`.

## ControlNet

```python
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel, DDIMScheduler
import numpy as np
import torch
import cv2
from PIL import Image
from hidiffusion import apply_hidiffusion, remove_hidiffusion

# load Yoshua_Bengio.jpg in the assets file.
path = 'Yoshua_Bengio.jpg'
image = Image.open(path)
# get canny image
image = np.array(image)
image = cv2.Canny(image, 100, 200)
image = image[:, :, None]
image = np.concatenate([image, image, image], axis=2)
canny_image = Image.fromarray(image)

# initialize the models and pipeline
controlnet_conditioning_scale = 0.5  # recommended for good generalization
controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16, variant="fp16"
)
scheduler = DDIMScheduler.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", subfolder="scheduler")
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet, torch_dtype=torch.float16,
    scheduler = scheduler
)
pipe.enable_model_cpu_offload()
pipe.enable_xformers_memory_efficient_attention()

prompt = "a zombie, high face detail, high detail, muted color, 8k"
negative_prompt = "blurry, ugly, duplicate, poorly drawn, deformed, mosaic, poorly drawn teeth, duplicated teeth."

# Apply hidiffusion with a single line of code.
apply_hidiffusion(pipe)

image = pipe(
    prompt, controlnet_conditioning_scale=controlnet_conditioning_scale, image=canny_image,
    height=2048, width=2048, guidance_scale=7.5, negative_prompt = negative_prompt, eta=1.0
).images[0]

image.save('zombie.jpg')
```

<details>
<summary>Output:</summary>
<div align="center">
  <img src="assets/controlnet_result.jpg" width="800" ></img>
</div>
</details>

## Inpainting

```python
import torch
from diffusers import AutoPipelineForInpainting, DDIMScheduler
from diffusers.utils import load_image
from hidiffusion import apply_hidiffusion, remove_hidiffusion
from PIL import Image

scheduler = DDIMScheduler.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", subfolder="scheduler")
pipeline = AutoPipelineForInpainting.from_pretrained(
    "diffusers/stable-diffusion-xl-1.0-inpainting-0.1", torch_dtype=torch.float16, variant="fp16", 
    scheduler=scheduler
)

# Apply hidiffusion with a single line of code.
apply_hidiffusion(pipeline)

pipeline.enable_model_cpu_offload()
# remove following line if xFormers is not installed
pipeline.enable_xformers_memory_efficient_attention()

# load base and mask image
img_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/sdxl-text2img.png"
init_image = load_image(img_url)
# load mask_image.jpg in the assets file.
mask_image = Image.open("mask_image.png")

prompt =  "A steampunk explorer in a leather aviator cap and goggles, with a brass telescope in hand, stands amidst towering ancient trees, their roots entwined with intricate gears and pipes."

negative_prompt = "blurry, ugly, duplicate, poorly drawn, deformed, mosaic"
image = pipeline(prompt=prompt, image=init_image, mask_image=mask_image, height=2048, width=2048, strength=0.85, guidance_scale=12.5, negative_prompt = negative_prompt, eta=1.0).images[0]
image.save('steampunk_explorer.jpg')
```

<details>
<summary>Output:</summary>
<div align="center">
  <img src="assets/inpainting_result.jpg" width="800" ></img>
</div>
</details>

## 🙏 Acknowledgements

This implementation is based on [tomesd](https://github.com/dbolya/tomesd) and [diffusers](https://github.com/huggingface/diffusers/tree/main). Thanks!



## 🎓 Citation

```
@article{zhang2023hidiffusion,
  title={HiDiffusion: Unlocking Higher-Resolution Creativity and Efficiency in Pretrained Diffusion Models},
  author={Zhang, Shen and Chen, Zhaowei and Zhao, Zhenyu and Chen, Yuhao and Tang, Yao and Liang, Jiajun},
  journal={arXiv preprint arXiv:2311.17528},
  year={2023}
}
```
