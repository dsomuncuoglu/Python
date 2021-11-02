import cv2
import numpy as np
from easyocr import Reader

# İstenen resmin diskten okunması
image_file_name = 'kitap.jpg'
# OpenCV ile resimin değişkenden okunması
image = cv2.imread(image_file_name)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# EasyOCR'dan okuyucunun özelliklerinin belirlenmesi
reader = Reader(['tr'], gpu=False)

# Gereksiz karakterlerin dikkate alınmamasını sağlayan fonksiyon
def cleanup_text(temiz_metin):
    return "".join([c if ord(c) < 128 else "" for c in temiz_metin]).strip()


# Yüklenen resimin renk ayarlarının yapılma işlemi
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]



# EasyOCR ile resimdeki kelimelerin okunup değişkene atılma işlemi
sonuc = reader.readtext(image, add_margin=0, width_ths=0)

dosya = open("cikti.txt", "w")

for (kutu, metin, yaklasik) in sonuc:
    dosya.write(metin + "\n")
    # Okunan metnin yaklaşık değerini kullanıcıya yüzde olarak verilme işlemi
    print("[Yaklasik Deger] %{:.2f}: {}".format(yaklasik*100, metin))
    # Okunan değerlerin çerçevelerinin oluşturulması
    (tl, tr, br, bl) = kutu
    tl = (int(tl[0]), int(tl[1]))
    tr = (int(tr[0]), int(tr[1]))
    br = (int(br[0]), int(br[1]))
    bl = (int(bl[0]), int(bl[1]))
    # Metinin kullanılmak istemeyen karakterlerin silinme işlemi
    metin = cleanup_text(metin)
    # Belirlenen çerçevelerin çizilme işlemi
    cv2.rectangle(image, tl, br, (0, 0, 255), 2)
    cv2.putText(image, metin, (tl[0], tl[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

dosya.close()

# Resimin kutuları ile birlikte kullanıcıya gösterilme işlemi
cv2.imshow("Sonuc", image)
cv2.imwrite("sonuc.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
