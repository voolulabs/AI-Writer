from openai import OpenAI
from loguru import logger
import sys

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from .save_image import save_generated_image


@retry(wait=wait_random_exponential(min=1, max=120), stop=stop_after_attempt(6))
def generate_dalle3_images(img_prompt, image_dir, size="1024x1024", quality="hd", n=1):
    """
    Generates images using the DALL-E 3 model based on a given text prompt.

    Args:
        img_prompt (str): Text prompt to generate the image.
        image_dir (str): Directory where the generated image will be saved.
        size (str, optional): Size of the generated images. Defaults to "1024x1024".
        quality (str, optional): Quality of the generated images. Defaults to "hd".
        n (int, optional): Number of images to generate. Defaults to 1.

    Returns:
        str: Path to the saved image.

    Raises:
        SystemExit: If an error occurs in image generation or saving.
    """
    try:
        logger.info("Generating Dall-e-3 image for the blog.")
        client = OpenAI()

        img_generation_response = client.images.generate(
            model="dall-e-3",
            prompt=img_prompt,
            size=size,
            quality=quality,
            n=n
        )

        img_path = save_generated_image(img_generation_response, image_dir)
        return img_path

    except openai.OpenAIError as e:
        logger.error(f"Dalle-3 image generation error: HTTP Status {e.http_status}, Error: {e.error}")
        sys.exit("Exiting due to Dalle-3 image generation error.")

    except Exception as e:
        logger.error(f"Failed to generate images with Dalle3: {e}")
        sys.exit("Exiting due to a general error in image generation.")

# Example usage
if __name__ == "__main__":
    try:
        image_path = generate_dalle3_images("A futuristic cityscape", "/path/to/image/dir")
        print(f"Image generated and saved at: {image_path}")
    except SystemExit as e:
        print(f"Terminated: {e}")
