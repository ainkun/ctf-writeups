print("<html>")
print("<body>")

print("""<style type="text/css">""")
print("html,body {margin:0;padding:0;}")
print("</style>")


for i in range(400):
	print(f"""<img src="flag_{i}.png" hspace='0'>""")
print("</body>")
print("</html>")

