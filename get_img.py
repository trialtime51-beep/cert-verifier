import urllib.request
import re
html = urllib.request.urlopen("https://www.uww.edu/career/student-alumni-resources/major-and-career-exploration/forage").read().decode("utf-8")
imgs = re.findall(r'<img[^>]+src="([^"]+)"[^>]*>', html)
for img in imgs:
    if "forage" in img.lower():
        print(img)
