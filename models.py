import os, json, sys, shutil, datetime, time

def fileContent(fileName, passAPIKey=False):
    with open(fileName, "r") as f:
        f_content = f.read()
        if passAPIKey:
            f_content = f_content.replace("\{{ API_KEY }}", os.environ["APIKey"])
            return f_content
        return f_content