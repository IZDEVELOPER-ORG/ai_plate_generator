import os
from os import PathLike
import yaml
import fire
from tqdm import tqdm
import mimetypes
from pathlib import Path
from google import genai
from google.genai import types
import logging
import uuid
import random


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_usage.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def save_txt_file(txt_path, content):
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Text metadata saved to: {txt_path}")


def get_images_list(folder):
    folder_path = Path(folder)
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
    images = [str(p)for p in folder_path.iterdir() if p.suffix.lower() in image_extensions]
    return images


def get_api_key(api_key_path):
    try:
        with open(api_key_path, "r", encoding="utf-8") as f:
            # .strip() удаляет случайные пробелы или переносы строк
            return f.read().strip()
    except FileNotFoundError:
        print("Error: API_key.txt file not found in the root folder!")
        return None


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def generate(api_key, model, prompt_text, stacked_text, number, image_path, save_folder, iteration):
    image_path = Path(image_path)
    if not os.path.exists(image_path):
        logger.error(f"Error: File not found in the path {image_path}")
        return

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    client = genai.Client(
        api_key=api_key,
    )

    contents = [types.Content(role="user", parts=[types.Part.from_bytes(mime_type="image/png", data=image_bytes),
                types.Part.from_text(text=prompt_text)])
                ]
    tools = [types.Tool(googleSearch=types.GoogleSearch(search_types=types.SearchTypes(web_search=types.WebSearch())))]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL",),
        image_config=types.ImageConfig(image_size="1K"),
        response_modalities=["IMAGE",
                             # "TEXT"
                             ],
        # tools=tools,
    )

    file_name = f"{image_path.stem}_var{iteration}_{uuid.uuid4()}"
    final_usage = None

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.usage_metadata:
            final_usage = chunk.usage_metadata
        if chunk.parts is None:
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            inline_data = chunk.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            output_image_path = f"{save_folder}/{file_name}{file_extension}"
            output_txt_path = f"{save_folder}/{file_name}.txt"
            save_binary_file(output_image_path, data_buffer)
            save_txt_file(output_txt_path, stacked_text+number)
        else:
            print(chunk.text)

    if final_usage:
        logger.info(
            f"FILE: {image_path.name} | "
            f"Prompt Tokens: {final_usage.prompt_token_count} | "
            f"Candidates Tokens: {final_usage.candidates_token_count} | "
            f"Total Tokens: {final_usage.total_token_count}"
        )


def main(
        cfg: PathLike
):
    config = yaml.safe_load(open(f"./configs/{cfg}"))
    images_folder = config["images_folder"]
    model = config["model"]
    limit = config["limit"]
    prompt_text = config["prompt"]
    stacked_text = config["stacked_text"]
    api_key = get_api_key(config["API_key"])

    if not api_key:
        return
    save_folder = config["save_folder"]
    Path(save_folder).mkdir(parents=True, exist_ok=True)

    image_list = get_images_list(images_folder)

    for image_path in tqdm(image_list, desc="Processing images"):
        for i in range(0, limit):
            random_number = ''.join(str(random.randint(0, 9)) for _ in range(5))
            new_prompt_text = f"{prompt_text}{random_number}"
            logger.info(f"Generating variation {i} for {image_path}")
            generate(api_key, model, new_prompt_text, stacked_text, random_number, image_path, save_folder, iteration=i)


if __name__ == "__main__":
    fire.Fire(main)
