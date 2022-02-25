# Careem Challenege

- Careem posted a Job on Linkedin for a position of Offensive Security engineer.
https://www.linkedin.com/posts/careem_careem-everydaylifemadesimple-activity-6902151090846916608-vHeg/

- They pasted a link, mentioining the applicants need to crack the code in the link, to apply for the job.
https://lnkd.in/efNFmMJz

./careem-posting.png

- The link redirects to an image.
./ c_challange.png

- Its my first time doing a steganography challenge.

## Initial

- Used 'wget' to download the image.

```bash
$wget https://blog.careem.com/wp-content/uploads/2022/02/c_challange.png

```

- I run strings on the image and dumped the data in a file.

```bash
$strings c_challange.png >> string_dump
```
./string_dump

- Its gibberish at first but it gets interesting later as I see 'flags' following with number with .txt extensions.

./strings-dump.png

- I suspect some kind of data is embedded with the image based on the results above.

- Used the tool "binwalk" (which is a utilty to find embedded files and codes in a given binary image file) to extract the embedded files from the image.

```bash
$binwalk -e c_challange.png
```
 - This command produces a verbose output extracting multiple flag text files.

 ```bash
 DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 3320 x 1263, 8-bit/color RGBA, non-interlaced
901390        0xDC10E         Zip archive data, at least v2.0 to extract, compressed size: 77, uncompressed size: 81, name: flag_0.txt
901535        0xDC19F         Zip archive data, at least v2.0 to extract, compressed size: 77, uncompressed size: 81, name: flag_1.txt
901680        0xDC230         Zip archive data, at least v2.0 to extract, compressed size: 77, uncompressed size: 81, name: flag_10.txt
901826        0xDC2C2         Zip archive data, at least v2.0 to extract, compressed size: 77, uncompressed size: 81, name: flag_100.txt
901973        0xDC355         Zip archive data, at least v2.0 to extract, compressed size: 83, uncompressed size: 87, name: flag_101.txt
902126        0xDC3EE         Zip archive data, at least v2.0 to extract, compressed size: 82, uncompressed size: 86, name: flag_102.txt
902278        0xDC486         Zip archive data, at least v2.0 to extract, compressed size: 91, uncompressed size: 96, name: flag_103.txt
902439        0xDC527         Zip archive data, at least v2.0 to extract, compressed size: 84, uncompressed size: 88, name: flag_104.txt
902593        0xDC5C1         Zip archive data, at least v2.0 to extract, compressed size: 89, uncompressed size: 93, name: flag_105.txt
902752        0xDC660         Zip archive data, at least v2.0 to extract, compressed size: 82, uncompressed size: 86, name: flag_106.txt
902904        0xDC6F8         Zip archive data, at least v2.0 to extract, compressed size: 85, uncompressed size: 88, name: flag_107.txt
903059        0xDC793         Zip archive data, at least v2.0 to extract, compressed size: 84, uncompressed size: 88, name: flag_108.txt
903213        0xDC82D         Zip archive data, at least v2.0 to extract, compressed size: 84, uncompressed size: 88, name: flag_109.txt
903367        0xDC8C7         Zip archive data, at least v2.0 to extract, compressed size: 77, uncompressed size: 81, name: flag_11.txt
.
.
.
.

 ```

- The command above created a folder '_c_challange.png.extracted'.
- Inside the folder, 'DC10E.zip' contains the backup of all extracted files.
- Extracted files include 400 flag text files numbering from flag_0.txt to flag_399.txt and a file named 'step2.txt'

- I tried reading the contents of the file, but it was binary encoded.
./binary-encode.png

- Ran the type command on the flag files, turns out they were PNG files.
./file-type.png

- A simple bash script will automate my task in converting all these flag files extention from .txt to .png.

```bash
$for file in *.txt; do mv "$file" "${file/.txt/.png}"; done
```
- All the files can bo be visualize and black and white pictures. 
./black-white.png

- As i need to merge thes pictures numberwise, I first thought of using an online converter or a tool, but failed to succeed. After I thought of using HTML, importing these images using image headers. 
- I used python to generate image headers with images locations numerically.

```python                                                              
print("<html>")
print("<body>")

# For Minimum spaces between images top bottom
print("""<style type="text/css">""")
print("html,body {margin:0;padding:0;}")
print("</style>")


for i in range(400):
        print(f"""<img src="flag_{i}.png" hspace='0'>""")
print("</body>")
print("</html>")

```
- Execute this script and dump them into index.html file.

```bash
$python3 html-script.py > index.html
```
- Opening the html in a browser and zooming gave me an idea that it is a dispersed image of a QR code.

./QR-code.png

- Still the problem arises is that I am not able to remove spaces between images and I am not able to see the image as one.
- What I was able to conclude is that the QR code image resolution is 200x200. Which means images will be placed 20x20 as each image is 10x10 resolution.
- To tackle this problem i took help of a python library "Pillow", which can merge multiple pictures.
- Made a script to automate my task using python.

```python
from PIL import Image

new_im = Image.new('RGB', (200,200), (250,250,250))

for i in range(20):
        for j in range(20):
                img = Image.open(f"flag_{(i*20)+j}.png")
                new_im.paste(img, (j*10,i*10))

new_im.save("QR_code-image.png", "PNG")

```
- Executing the script on the same folder where images where produced a beautifull QR code picture.
./QR_code-image.png

- scanning the QR code generates a code. 
code = 'XXXXXXXX'

- After extracting the code, s the challenge over? I still don't know where to send the code too.
- Plus there is a file 'step2.txt' left. 
- The contents of the file is also binary encoded, I repeat the step to check the file type using 'file' tool.

```bash
$file step2.txt 

step2.txt: GPG symmetrically encrypted data (AES256 cipher)

```

- This file is encrypted and requires a passphrase to decrypt the contents
- gpg2john to calculate the hash

```bash
$gpg2john step2 > hash
$cat hash 

$gpg$*0*126*3ded05b7cd4812e1571d04f1a958b5920f50bac052b88a9c986dfab6da1e47893a176d67b323e7b112a368d1afde61ce44ece9afbe34a9e858f53d67a1d14832c65a46d12d1c72bc48d54195f12f261ae3bbc11577fb2191a0de3553030588ede15066be1fbd51ac154a2d3199905a45e8e5624ebf10e947422a90dc58fc*3*18*2*9*39845888*4d9023a6063aee32

```

- Crack the hash using john and rockyou.txt wordlist

```bash
$john hash --wordlist=~/Desktop/rockyou.txt

$john --show hash 
?:jojojo

1 password hash cracked, 0 left

```
Password : 'jojojo'

- Use the passsword to decrypt the file and view its contenet

```bash
$gpg --decrypt --output decrypt-contents step2 
$cat decrypt-contents 
Send the FLAG along with your resume at quentin.gaumer@careem.com
```
./decrypt-contents

- I can now send the flag and and my resume to this email.
