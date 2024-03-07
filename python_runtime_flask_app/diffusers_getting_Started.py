from diffusers import DiffusionPipeline
pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", use_safetensors=True)
pipeline.to("cuda")
image = pipeline("An image of a squirrel in Picasso style").images[0]
# save the image to disk
image.save("squirrel_picasso.jpg")
