import json
import re

from comfy.comfy_types import IO  # , ComfyNodeABC, InputTypeDict

## 
# placeholder prompting node
# allows placing ** some name ** in prompts and replaces
# the placeholder with the correct stored description
# for easy and reliable prompt creation
##


class PlaceholderWithUI:
    NODE_NAME = "easy prompting"
    CATEGORY = "prompting"
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("parsed_text", )
    FUNCTION = "replace_placeholders"
    OUTPUT_NODE = True

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"raw_text": (IO.STRING, {"multiline": True, "dynamicPrompts": True, "tooltip": "The text to be encoded."}), }}

    def replace_placeholders(self, raw_text):
        # parses the prompt and replaces placeholders with the given prompt
        # allows ## .... ## for comments/greyed out text
        # allows ** .... ** for text placeholders

        # load the placeholders from placeholders.json
        with open('custom_nodes/comfyui_placeholder_prompting/placeholders/placeholders.json') as data:
            self.data = json.load(data)

        def replace_placeholder(match):
            # replaces **placeholders** with value found in placeholder.json
            key = match.group(1).strip()
            return self.data.get(key, match.group(0))  # fallback to original

        # remove greyed out text
        parsed_text = re.sub(r"##.*?##", "", raw_text, flags=re.DOTALL)
        
        # replace **placeholders**
        parsed_text = re.sub(r"\*\*(.*?)\*\*", replace_placeholder, parsed_text)

        return {"ui": {"text": (parsed_text,)}, "result": (parsed_text,)}


NODE_CLASS_MAPPINGS = {
    "PlaceholderPrompting": PlaceholderWithUI,
}
