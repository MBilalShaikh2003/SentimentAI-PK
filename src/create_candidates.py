import csv
from pathlib import Path

rows = [
    # Roman Urdu — Positive
    ("Roman Urdu", "Yeh mobile bohat zabardast chal raha hai", "positive"),
    ("Roman Urdu", "Is website ka design mujhe bohat pasand aya", "positive"),
    ("Roman Urdu", "Customer support ne foran masla hal kar diya", "positive"),
    ("Roman Urdu", "Parcel waqt par aur sahi halat mein mila", "positive"),
    ("Roman Urdu", "Is hotel ka khana lajawab tha", "positive"),
    ("Roman Urdu", "Staff ne bohat tameez se baat ki", "positive"),
    ("Roman Urdu", "Main dobara isi seller se shopping karunga", "positive"),
    ("Roman Urdu", "App use karna bohat asaan hai", "positive"),
    ("Roman Urdu", "Paise ke hisaab se quality zabardast hai", "positive"),
    ("Roman Urdu", "Mera is service ke sath tajurba bohat acha raha", "positive"),

    # Roman Urdu — Negative
    ("Roman Urdu", "Yeh mobile har thori dair baad hang hota hai", "negative"),
    ("Roman Urdu", "Website khulti hi nahi hai", "negative"),
    ("Roman Urdu", "Customer support ne meri bilkul madad nahi ki", "negative"),
    ("Roman Urdu", "Parcel tootay huay dabbe mein mila", "negative"),
    ("Roman Urdu", "Khanay ka zaiqa bohat bura tha", "negative"),
    ("Roman Urdu", "Staff ka rawayya bohat badtameezana tha", "negative"),
    ("Roman Urdu", "Mujhe ghalat product bhej diya gaya", "negative"),
    ("Roman Urdu", "App baar baar crash ho rahi hai", "negative"),
    ("Roman Urdu", "Itni qeemat mein quality bohat ghatiya hai", "negative"),
    ("Roman Urdu", "Main is seller se dobara order nahi karunga", "negative"),

    # Roman Urdu — Neutral
    ("Roman Urdu", "Mera parcel aaj subah deliver hua", "neutral"),
    ("Roman Urdu", "Is mobile mein do SIM cards lagte hain", "neutral"),
    ("Roman Urdu", "Website par teen payment options mojood hain", "neutral"),
    ("Roman Urdu", "Maine kal customer support ko email ki thi", "neutral"),
    ("Roman Urdu", "Parcel ke andar charger bhi tha", "neutral"),
    ("Roman Urdu", "Yeh hotel railway station ke qareeb hai", "neutral"),
    ("Roman Urdu", "App Android aur iPhone dono par chalti hai", "neutral"),
    ("Roman Urdu", "Order ki qeemat do hazaar rupay thi", "neutral"),
    ("Roman Urdu", "Dukaan raat nau bajay band hoti hai", "neutral"),
    ("Roman Urdu", "Maine blue rang ka shirt order kiya tha", "neutral"),

    # Urdu script — Positive
    ("Urdu script", "یہ موبائل بہت اچھا کام کر رہا ہے", "positive"),
    ("Urdu script", "اس ویب سائٹ کا ڈیزائن بہت خوبصورت ہے", "positive"),
    ("Urdu script", "کسٹمر سپورٹ نے فوراً میرا مسئلہ حل کر دیا", "positive"),
    ("Urdu script", "پارسل وقت پر اور صحیح حالت میں ملا", "positive"),
    ("Urdu script", "اس ہوٹل کا کھانا بہت مزیدار تھا", "positive"),
    ("Urdu script", "عملے نے بہت اچھے طریقے سے بات کی", "positive"),
    ("Urdu script", "میں دوبارہ اسی دکاندار سے خریداری کروں گا", "positive"),
    ("Urdu script", "یہ ایپ استعمال کرنا بہت آسان ہے", "positive"),
    ("Urdu script", "قیمت کے مقابلے میں معیار بہترین ہے", "positive"),
    ("Urdu script", "اس سروس کے ساتھ میرا تجربہ اچھا رہا", "positive"),

    # Urdu script — Negative
    ("Urdu script", "یہ موبائل بار بار بند ہو جاتا ہے", "negative"),
    ("Urdu script", "ویب سائٹ کھل ہی نہیں رہی", "negative"),
    ("Urdu script", "کسٹمر سپورٹ نے میری کوئی مدد نہیں کی", "negative"),
    ("Urdu script", "پارسل ٹوٹے ہوئے ڈبے میں ملا", "negative"),
    ("Urdu script", "کھانے کا ذائقہ بہت خراب تھا", "negative"),
    ("Urdu script", "عملے کا رویہ بہت بدتمیز تھا", "negative"),
    ("Urdu script", "مجھے غلط چیز بھیجی گئی", "negative"),
    ("Urdu script", "ایپ بار بار بند ہو رہی ہے", "negative"),
    ("Urdu script", "اتنی قیمت میں معیار بہت خراب ہے", "negative"),
    ("Urdu script", "میں اس دکاندار سے دوبارہ خریداری نہیں کروں گا", "negative"),

    # Urdu script — Neutral
    ("Urdu script", "میرا پارسل آج صبح پہنچا", "neutral"),
    ("Urdu script", "اس موبائل میں دو سم کارڈ لگتے ہیں", "neutral"),
    ("Urdu script", "ویب سائٹ پر ادائیگی کے تین طریقے ہیں", "neutral"),
    ("Urdu script", "میں نے کل کسٹمر سپورٹ کو ای میل کی", "neutral"),
    ("Urdu script", "پارسل کے اندر چارجر بھی موجود تھا", "neutral"),
    ("Urdu script", "یہ ہوٹل ریلوے اسٹیشن کے قریب ہے", "neutral"),
    ("Urdu script", "یہ ایپ اینڈرائیڈ اور آئی فون دونوں پر چلتی ہے", "neutral"),
    ("Urdu script", "آرڈر کی قیمت دو ہزار روپے تھی", "neutral"),
    ("Urdu script", "دکان رات نو بجے بند ہوتی ہے", "neutral"),
    ("Urdu script", "میں نے نیلے رنگ کی قمیض منگوائی تھی", "neutral"),

    # English — Positive
    ("English", "The battery lasts much longer than I expected", "positive"),
    ("English", "The refund was processed quickly and smoothly", "positive"),
    ("English", "The staff were friendly and helpful", "positive"),
    ("English", "The instructions were clear and easy to follow", "positive"),
    ("English", "The product feels reliable and well made", "positive"),

    # English — Negative
    ("English", "The battery drains within a few hours", "negative"),
    ("English", "My refund request was ignored for weeks", "negative"),
    ("English", "The staff were rude when I asked for help", "negative"),
    ("English", "The instructions were confusing and incomplete", "negative"),
    ("English", "The product stopped working after one day", "negative"),

    # English — Neutral
    ("English", "The package contains a charger and a cable", "neutral"),
    ("English", "The store opens at ten in the morning", "neutral"),
    ("English", "The order includes three separate items", "neutral"),
    ("English", "The product is available in four colours", "neutral"),
    ("English", "The meeting was scheduled for Monday", "neutral"),

    # Mixed Urdu/Roman Urdu and English — Positive
    ("Mixed", "Product ki quality excellent hai aur delivery bhi fast thi", "positive"),
    ("Mixed", "Customer support ne mera issue quickly resolve kar diya", "positive"),
    ("Mixed", "Phone ki battery life amazing hai", "positive"),
    ("Mixed", "App ka interface simple aur user friendly hai", "positive"),
    ("Mixed", "Parcel safely deliver hua aur packaging bhi great thi", "positive"),

    # Mixed — Negative
    ("Mixed", "Product acha nahi hai aur build quality poor hai", "negative"),
    ("Mixed", "Delivery late thi aur customer support was unhelpful", "negative"),
    ("Mixed", "Phone frequently hang hota hai, performance is terrible", "negative"),
    ("Mixed", "Refund abhi tak nahi mila, service is disappointing", "negative"),
    ("Mixed", "Packaging damaged thi aur product bhi broken tha", "negative"),

    # Mixed — Neutral
    ("Mixed", "Order confirm ho gaya hai and delivery is scheduled for Monday", "neutral"),
    ("Mixed", "Package mein charger aur user manual included hain", "neutral"),
    ("Mixed", "Payment successfully process ho gayi, amount was Rs. 2500", "neutral"),
    ("Mixed", "Store Karachi mein hai and it opens at 10 AM", "neutral"),
    ("Mixed", "Maine black colour select kiya, the size is medium", "neutral"),

    # Mixed sentiment — needs careful review
    ("Mixed - review", "Product acha hai lekin delivery bohat late thi", "neutral"),
    ("Mixed - review", "Quality excellent hai but price bohat zyada hai", "neutral"),
    ("Mixed - review", "Food tasty tha lekin service bohat slow thi", "neutral"),
    ("Mixed - review", "Phone fast hai but battery jaldi khatam hoti hai", "neutral"),
    ("Mixed - review", "Staff helpful tha lekin mera issue solve nahi hua", "neutral"),
]

output = Path("data/sentiment_candidates.csv")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "sentiment", "category", "review_status"])
    for category, text, sentiment in rows:
        status = "REVIEW_REQUIRED" if category == "Mixed - review" else "PROPOSED"
        writer.writerow([text, sentiment, category, status])

print(f"Candidate file created: {output}")
print(f"Total candidates: {len(rows)}")
print(f"Review-required mixed-sentiment examples: {sum(1 for r in rows if r[0] == 'Mixed - review')}")
print("Original dataset was not modified.")
