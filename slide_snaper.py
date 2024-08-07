import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from utils import remove_bg_color
import numpy as np
import base64
import time


class SlideSnapper:
    def __init__(self, target_element_id, tranparent_target=None) -> None:
        self.target_element_id = target_element_id
        self.tranparent_target = tranparent_target
        options = ChromeOptions()
        # options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options)
        self.driver.maximize_window()


    def __delattr__(self, name: str) -> None:
        self.driver.quit()


    def take_snap_png(self, page_html):
        
        # Load HTML
        encoded_html  = base64.b64encode(page_html.encode('utf-8')).decode()
        self.driver.get("data:text/html;base64," + encoded_html)
        
        # self.driver.execute_script("document.write('{}')".format(json.dumps(page_html)))

        # Find the div wait for bg image and take a screenshot
        div = self.driver.find_element(By.ID, self.target_element_id)
    
        while div.value_of_css_property('background-image') == None:
            self.driver.implicitly_wait(1)

        ss_bytes = div.screenshot_as_png
        ss_image = Image.open(BytesIO(ss_bytes))
        
        if self.tranparent_target:
            ss_image = remove_bg_color(ss_image, self.tranparent_target)
        
        return ss_image
        



if __name__=="__main__":
    with open("slide_template_2.html", "r") as f:
        html_string = f.read()
    
    snapper = SlideSnapper("id_slide")
    image = snapper.take_snap_png(page_html=html_string)
    image.save("output/ss.png")