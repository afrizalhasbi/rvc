<div align="center">

<h1>Retrieval-based-Voice-Conversion-WebUI</h1>
一个基于VITS的简单易用的变声框架<br><br>

[![madewithlove](https://img.shields.io/badge/made_with-%E2%9D%A4-red?style=for-the-badge&labelColor=orange
)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

<img src="https://counter.seku.su/cmoe?name=rvc&theme=r34" /><br>

[![Open In Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)](https://colab.research.google.com/github/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/Retrieval_based_Voice_Conversion_WebUI.ipynb)
[![Licence](https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)
[![Huggingface](https://img.shields.io/badge/🤗%20-Spaces-yellow.svg?style=for-the-badge)](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)

[![Discord](https://img.shields.io/badge/RVC%20Developers-Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/HcsmBBGyVk)

[**更新日志**](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/Changelog_CN.md) | [**常见问题解答**](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E8%A7%A3%E7%AD%94) | [**AutoDL·5毛钱训练AI歌手**](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/wiki/Autodl%E8%AE%AD%E7%BB%83RVC%C2%B7AI%E6%AD%8C%E6%89%8B%E6%95%99%E7%A8%8B) | [**对照实验记录**](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/wiki/Autodl%E8%AE%AD%E7%BB%83RVC%C2%B7AI%E6%AD%8C%E6%89%8B%E6%95%99%E7%A8%8B](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/wiki/%E5%AF%B9%E7%85%A7%E5%AE%9E%E9%AA%8C%C2%B7%E5%AE%9E%E9%AA%8C%E8%AE%B0%E5%BD%95)) | [**在线演示**](https://modelscope.cn/studios/FlowerCry/RVCv2demo)

[**English**](./docs/en/README.en.md) | [**中文简体**](./README.md) | [**日本語**](./docs/jp/README.ja.md) | [**한국어**](./docs/kr/README.ko.md) ([**韓國語**](./docs/kr/README.ko.han.md)) | [**Français**](./docs/fr/README.fr.md) | [**Türkçe**](./docs/tr/README.tr.md) | [**Português**](./docs/pt/README.pt.md)

</div>

> 底模使用接近50小时的开源高质量VCTK训练集训练，无版权方面的顾虑，请大家放心使用

> 请期待RVCv3的底模，参数更大，数据更大，效果更好，基本持平的推理速度，需要训练数据量更少。

<table>
   <tr>
		<td align="center">训练推理界面</td>
		<td align="center">实时变声界面</td>
	</tr>
  <tr>
		<td align="center"><img src="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/assets/129054828/092e5c12-0d49-4168-a590-0b0ef6a4f630"></td>
    <td align="center"><img src="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/assets/129054828/730b4114-8805-44a1-ab1a-04668f3c30a6"></td>
	</tr>
	<tr>
		<td align="center">go-web.bat</td>
		<td align="center">go-realtime-gui.bat</td>
	</tr>
  <tr>
    <td align="center">可以自由选择想要执行的操作。</td>
		<td align="center">我们已经实现端到端170ms延迟。如使用ASIO输入输出设备，已能实现端到端90ms延迟，但非常依赖硬件驱动支持。</td>
	</tr>
</table>

## Introduction
This repository has the following features:
+ Uses top1 retrieval to replace input source features with training set features to prevent timbre leakage.
+ Capable of rapid training even on relatively low-end GPUs.
+ Achieves good results with a small amount of training data (recommended to collect at least 10 minutes of low-noise speech data).
+ Allows for timbre alteration through model fusion (using the ckpt-merge option in the ckpt processing tab).
+ Features a simple and user-friendly web interface.
+ Can invoke the UVR5 model for quick separation of vocals and accompaniment.
+ Utilizes the state-of-the-art [InterSpeech2023-RMVPE](#reference-projects) pitch extraction algorithm to eliminate voiceless issues. It offers the best performance (significantly) and is faster and less resource-intensive than crepe_full.
+ Supports acceleration for AMD and Intel GPUs.

Click here to watch our [demo video](https://www.bilibili.com/video/BV1pm4y1z7Gm/)!

## Environment Setup
The following instructions should be executed in a Python environment with a version greater than 3.8.

### Universal Method for Windows/Linux/MacOS Platforms
Choose one of the following methods.
#### 1. Install Dependencies via pip
1. Install Pytorch and its core dependencies. Skip this step if already installed. Reference: https://pytorch.org/get-started/locally/
```bash
pip install torch torchvision torchaudio
```
2. For Windows systems with Nvidia Ampere architecture (RTX30xx), based on #21's experience, you need to specify the corresponding CUDA version for Pytorch:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```
3. Install the corresponding dependencies based on your graphics card:
- Nvidia GPUs
```bash
pip install -r requirements.txt
```
- AMD/Intel GPUs
```bash
pip install -r requirements-dml.txt
```
- AMD ROCm (Linux)
```bash
pip install -r requirements-amd.txt
```
- Intel IPEX (Linux)
```bash
pip install -r requirements-ipex.txt
```

## Preparation of Other Pre-trained Models
RVC requires some additional pre-trained models for inference and training.

You can download these models from our [Hugging Face space](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/).

### 1. Download Assets
Below is a list of all the pre-trained models and other files required by RVC. You can find scripts to download them in the `tools` folder.

- ./assets/hubert/hubert_base.pt

- ./assets/pretrained 

- ./assets/uvr5_weights

If you want to use the v2 version models, you need to additionally download:

- ./assets/pretrained_v2

### 2. Install ffmpeg
Skip this step if ffmpeg and ffprobe are already installed.

#### Ubuntu/Debian Users
```bash
sudo apt install ffmpeg
```

### 3. Download Files for RMVPE Pitch Extraction Algorithm

If you want to use the latest RMVPE pitch extraction algorithm, you need to download the pitch extraction model parameters and place them in the RVC root directory.

- Download [rmvpe.pt](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/rmvpe.pt)

#### Download RMVPE for DML Environment (Optional, for AMD/Intel GPU Users)

- Download [rmvpe.onnx](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/rmvpe.onnx)

### 4. AMD ROCm Setup (Optional, Linux Only)

If you want to run RVC on Linux using AMD's ROCm technology, first install the required drivers [here](https://rocm.docs.amd.com/en/latest/deploy/linux/os-native/install.html).

For Arch Linux users, you can install the necessary drivers using pacman:
````
pacman -S rocm-hip-sdk rocm-opencl-sdk
````
For certain GPU models (e.g., RX6700XT), you may need to configure additional environment variables as follows:
````
export ROCM_PATH=/opt/rocm
export HSA_OVERRIDE_GFX_VERSION=10.3.0
````
Also, ensure your current user is part of the `render` and `video` groups:
````
sudo usermod -aG render $USERNAME
sudo usermod -aG video $USERNAME
````

## Getting Started
### Direct Launch
Use the following command to start the WebUI:
```bash
python infer-web.py
```

If you previously installed dependencies using Poetry, you can start the WebUI with:
```bash
poetry run python infer-web.py
```

### Using the All-in-One Package
Download and extract `RVC-beta.7z`.
#### Windows Users
Double-click `go-web.bat`.
#### MacOS Users
```bash
sh ./run.sh
```
### For Intel GPU Users Requiring IPEX Technology (Linux Only)
```bash
source /opt/intel/oneapi/setvars.sh
```

## Reference Projects
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [FFmpeg](https://github.com/FFmpeg/FFmpeg)
+ [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
+ [audio-slicer](https://github.com/openvpi/audio-slicer)
+ [Vocal pitch extraction:RMVPE](https://github.com/Dream-High/RMVPE)
  + The pretrained model is trained and tested by [yxlllc](https://github.com/yxlllc/RMVPE) and [RVC-Boss](https://github.com/RVC-Boss).

## Acknowledgments to All Contributors for Their Efforts
<a href="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=RVC-Project/Retrieval-based-Voice-Conversion-WebUI" />
</a>
