import shutil
import time


import os
import json
import math
import re
import torch
import gdown
from pydub import AudioSegment
from . import commons
from . import utils
import soundfile as sf
from .models import SynthesizerTrn
from .text.symbols import symbols
from .text import text_to_sequence
def _ensure_drive_url(url: str) -> str:
    m = re.search(r'/d/([^/]+)/', url)
    if m:
        return f"https://drive.google.com/uc?id={m.group(1)}"
    return url

AUDIO_BEEP = "/app/ai_tools/model/beep.mp3"
os.makedirs("/app/raw_file/speaking/instruction", exist_ok=True)
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

def speak_EN(text, speed: float = 1.0, vocal:str = "female", output_path = "/app/raw_file/speaking/instruction/audio.mp3"):
    temp_dir = "/app/ai_tools/data_temp"
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)
    pretrained_path = "/app/ai_tools/model/pretrained_ljs.pth"
    weight_url = "https://drive.google.com/file/d/1ut7UkshBXGbe5ElQkaOIeUULb2I1tO48/view?usp=sharing"
    if not os.path.isfile(pretrained_path):
        download_url = _ensure_drive_url(weight_url)
        gdown.download(download_url, output=pretrained_path, quiet=False)
    hps = utils.get_hparams_from_file(f"/app/ai_tools/model/config.json")
    i = 0
    if vocal == "female":
        net_g = SynthesizerTrn(
            len(symbols),
            hps.data.filter_length // 2 + 1,
            hps.train.segment_size // hps.data.hop_length,
            **hps.model)
        _ = net_g.eval()

        _ = utils.load_checkpoint(pretrained_path, net_g, None)   
    if isinstance(text, str):
        text = text.replace("\n", ". ")
        paragraphs = text.split(".")
        for paragraph in paragraphs[:-1]:
            output_file = f"{temp_dir}/{i:04d}.mp3"
            i+= 1
            stn_tst = get_text(paragraph, hps)
            with torch.no_grad():
                if vocal == "female": 
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                else: 
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    sid = torch.LongTensor([4])
                    audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                sf.write(output_file, audio, int(hps.data.sampling_rate * speed))
        
        folder = os.listdir(temp_dir)
        file_names = [f"{temp_dir}/{file_name}" for file_name in folder] + [AUDIO_BEEP]
        audio_segments = [AudioSegment.from_file(file_name) for file_name in file_names]
        
        audio = sum(audio_segments)
        audio.export(output_path, format="mp3")
        del net_g, hps, audio, audio_segments
        shutil.rmtree(temp_dir, ignore_errors=True)
        return output_path
    if isinstance(text, list):
        topic = text[1]
        paragraphs = topic.split(".")
        for paragraph in paragraphs[:-1]:
            output_file = f"{temp_dir}/{i:04d}.mp3"
            i += 1
            stn_tst = get_text(paragraph, hps)
            with torch.no_grad():
                if vocal == "female": 
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                else: 
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    sid = torch.LongTensor([4])
                    audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                sf.write(output_file, audio, int(hps.data.sampling_rate * speed))
        question = text[2]
        paragraphs = question.split(".")
        for paragraph in paragraphs[:-1]:
            output_file = f"{temp_dir}/{i:04d}.mp3"
            i += 1
            stn_tst = get_text(paragraph, hps)
            with torch.no_grad():
                if vocal == "female": 
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                else: 
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    sid = torch.LongTensor([4])
                    audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                sf.write(output_file, audio, int(hps.data.sampling_rate * speed))
                
        folder = os.listdir(temp_dir)
        file_names = [f"{temp_dir}/{file_name}" for file_name in folder]
        file_names = file_names + [AUDIO_BEEP]
        audio_segments = [AudioSegment.from_file(file_name) for file_name in file_names]
            
        audio = sum(audio_segments)
        audio.export(output_path, format="mp3")
        del net_g, hps, audio, audio_segments
        shutil.rmtree(temp_dir, ignore_errors=True)
        return output_path

