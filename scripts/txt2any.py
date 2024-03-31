import modules.scripts as scripts
import gradio as gr
import os
import re
import requests
from urllib3.exceptions import InsecureRequestWarning
from io import BytesIO
from modules import script_callbacks
from PIL import Image

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
url = 'https://api.txt2any.com/v1/images'
ext_path = scripts.basedir()

def save_apikey(apikey):
    f = open(f"{ext_path}/.apikey", "w")
    f.write(apikey)
    f.close()
    return apikey

def read_apikey():
    try:
        f = open(f"{ext_path}/.apikey", "r")
        return f.read()
    except Exception:
        return ''

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Column(scale=1, elem_classes='t2a-tab-content'):
            with gr.Row():
                apikey = gr.Textbox(
                    label="txt2any API Key",
                    lines=3,
                    value="",
                    placeholder="Paste the key content here"
                )
                ui_component.load(lambda x: gr.update(value=read_apikey()), None, apikey, queue=True)
            with gr.Row():
                save_button = gr.Button(value="Save", variant='primary')
                save_button.click(lambda x: save_apikey(x), apikey, apikey, queue=True)
                clear_button = gr.ClearButton(value="Clear", variant='secondary')
                clear_button.click(lambda x: gr.update(value=''), None, apikey, queue=True)
            with gr.Row():
                gr.HTML(value="You can find the key content in \"My Account > API keys\" section on <a href=\"https://www.txt2any.com\" target=\"_blank\">https://www.txt2any.com</a>")
            with gr.Row():
                help_img = os.path.join(ext_path, "images/apikey-gen-example.png")
                gr.Image(type="pil", value=help_img, width=1083, scale=0.8, container=False, show_download_button=False)
            return [(ui_component, "txt2any Cloud", "extension_t2a_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)

class T2ACloudExtension(scripts.Script):
    def title(self):
        return "txt2any Cloud"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('txt2any Cloud', open=True):
            with gr.Row():
                checkbox_save_to_cloud = gr.inputs.Checkbox(label="Save to txt2any cloud", default=True)
                return [checkbox_save_to_cloud]

    def postprocess(self, p, processed, checkbox_save_to_cloud):
        if not checkbox_save_to_cloud:
            return True

        multiple_files = []

        for i in range(len(processed.images)):
            image = processed.images[i]
            filename = re.split(r'\\|/', image.already_saved_as)[-1]
            file_upload = ('files', (filename, open(image.already_saved_as, 'rb'), 'image/png'))
            multiple_files.append(file_upload)

        headers = {
            'Authorization': f'Bearer {read_apikey()}'
            }
        r = requests.post(url, files=multiple_files, headers=headers, verify=False)
        return True