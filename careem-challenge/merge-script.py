from PIL import Image

new_im = Image.new('RGB', (200,200), (250,250,250))

for i in range(20):
        for j in range(20):
                img = Image.open(f"flag_{(i*20)+j}.png")
                new_im.paste(img, (j*10,i*10))

new_im.save("QR_code-image.png", "PNG")
