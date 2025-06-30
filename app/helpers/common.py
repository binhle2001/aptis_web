import base64
import logging
import os
from configparser import ConfigParser
from fastapi import Request
from typing import Generator
import pdfplumber
import psycopg2



def get_env_var(group, var_name): 
    config = ConfigParser()
    file_path = ".env"
    if os.path.exists(file_path):
        config.read(file_path)
        return  config[group][var_name]
    return os.environ.get(var_name)

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

