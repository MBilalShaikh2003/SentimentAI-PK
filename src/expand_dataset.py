
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sentiment_dataset.csv"

new_examples = [
    # 20 positive comments
    ("Is product ka result bohat acha nikla", "positive"),
    ("Mujhe is service se bohat satisfaction mili", "positive"),
    ("Quality dekh kar main khush ho gaya", "positive"),
    ("Staff ne meri bohat achi guidance ki", "positive"),
    ("Order expected time se pehle aa gaya", "positive"),
    ("Yeh paison ke hisaab se behtareen hai", "positive"),
    ("Product use karna bohat asaan hai", "positive"),
    ("Customer support ka response zabardast tha", "positive"),
    ("Packaging saaf aur professional thi", "positive"),
    ("Main dobara isi website se order karunga", "positive"),
    ("Meri problem foran solve ho gayi", "positive"),
    ("Product bilkul meri umeed ke mutabiq hai", "positive"),
    ("Delivery service bohat reliable hai", "positive"),
    ("Is brand ka experience yaadgar raha", "positive"),
    ("Mujhe quality aur design dono pasand aaye", "positive"),
    ("Team ne bohat achi service di", "positive"),
    ("Purchase kar ke mujhe acha laga", "positive"),
    ("Product ki performance excellent hai", "positive"),
    ("Yeh service recommend karne ke qabil hai", "positive"),
    ("Mera overall experience bohat umda raha", "positive"),

    # 20 negative comments
    ("Product ki quality bilkul achi nahi hai", "negative"),
    ("Meri delivery bohat zyada late hui", "negative"),
    ("Customer support ne jawab nahi diya", "negative"),
    ("Mujhe yeh purchase kar ke afsos hua", "negative"),
    ("Product meri umeed par poora nahi utra", "negative"),
    ("Website par order place karna mushkil tha", "negative"),
    ("Package damage condition mein mila", "negative"),
    ("Staff ne meri baat theek se nahi suni", "negative"),
    ("Is product ki performance bohat buri hai", "negative"),
    ("Mujhe ghalat item bhej diya gaya", "negative"),
    ("Refund abhi tak receive nahi hua", "negative"),
    ("Service ka experience bohat disappointing tha", "negative"),
    ("Product kuch din mein kharab ho gaya", "negative"),
    ("Price ke muqablay mein quality buri hai", "negative"),
    ("Mera masla solve karne mein bohat der lagi", "negative"),
    ("Packaging ki wajah se product toot gaya", "negative"),
    ("Main is seller par bharosa nahi karunga", "negative"),
    ("Order ki details ghalat thi", "negative"),
    ("Is service se mujhe koi faida nahi hua", "negative"),
    ("Main is product ko bilkul recommend nahi karta", "negative"),

    # 20 neutral comments
    ("Maine website par account banaya", "neutral"),
    ("Order ki quantity do units thi", "neutral"),
    ("Parcel subah das baje deliver hua", "neutral"),
    ("Product ka model A200 hai", "neutral"),
    ("Payment debit card se ki gayi", "neutral"),
    ("Order status abhi shipped hai", "neutral"),
    ("Package mein aik charger tha", "neutral"),
    ("Maine delivery address change kiya", "neutral"),
    ("Product ka size large hai", "neutral"),
    ("Invoice ke andar order number likha hai", "neutral"),
    ("Maine teen din pehle order diya", "neutral"),
    ("Website par chaar categories hain", "neutral"),
    ("Parcel courier service se aya", "neutral"),
    ("Product ka weight aik kilogram hai", "neutral"),
    ("Order number 56789 hai", "neutral"),
    ("Warranty ki muddat barah mahine hai", "neutral"),
    ("Maine cash on delivery select kiya", "neutral"),
    ("Product ka colour black hai", "neutral"),
    ("Order abhi processing stage mein hai", "neutral"),
    ("Package mein user manual shamil hai", "neutral"),
]

# Load the existing dataset
df = pd.read_csv(DATA_PATH)
before = len(df)

# Prepare new rows
new_df = pd.DataFrame(new_examples, columns=["text", "sentiment"])

# Add only examples whose text is not already present
existing_texts = set(df["text"].astype(str).str.strip().str.lower())
new_df = new_df[
    ~new_df["text"].str.strip().str.lower().isin(existing_texts)
]

# Combine and remove any exact duplicate texts
combined = pd.concat([df, new_df], ignore_index=True)
combined["text"] = combined["text"].astype(str).str.strip()
combined["sentiment"] = combined["sentiment"].astype(str).str.strip().str.lower()
combined = combined.drop_duplicates(subset=["text"], keep="first")

# Save the updated dataset
combined.to_csv(DATA_PATH, index=False)

print("Dataset expansion completed!")
print("Rows before:", before)
print("New unique examples added:", len(combined) - before)
print("Rows after:", len(combined))
print("\nSentiment counts:")
print(combined["sentiment"].value_counts())
print("\nDuplicate texts:", combined["text"].duplicated().sum())
