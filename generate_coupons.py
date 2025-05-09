import stripe
import csv
import time
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os
import random
import string

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")

# 🏷️ Metadata for tracking restrictions
target_price_id = 'price_1R9Ic2GWt28Mi4FnzhrXWvjZ'
target_product_id = 'prod_S3PQodEWVRXKPR'

# ⏳ Expiry date
expiry_date = datetime.datetime(2025, 8, 30, 23, 59, 59)
expires_at_unix = int(time.mktime(expiry_date.timetuple()))

# 🎟️ Create the coupon once
coupon = stripe.Coupon.create(
    name='Everyday Business', # @ 700_000 @ 25% off
    # name='Business Growth' # @ 100_000 @ 50% off
    # YFB
    duration='once',
    percent_off=25,
    # amount_off=0,
    # currency='aud',
    metadata={
        'intended_price': target_price_id,
        'intended_product': target_product_id,
    }
)

# 🔧 Constants
TOTAL_CODES = 10
WORKER_COUNT = 10
BATCH_SIZE = 400
PROMO_CODE_PREFIX = "YFB"  # <-- Add your desired prefix here (at least 3 chars)

# 🧾 CSV setup
lock = threading.Lock()
csv_file = open('promotion_codes.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(["Discount Codes", "Expiry Date", "Offer"])  # <-- Add header row

def generate_code(prefix, length=16):
    # Generates a code like PREFIX-AB12CD34
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{random_part}"

def create_promo_code(_):
    for attempt in range(3):
        try:
            code = generate_code(PROMO_CODE_PREFIX)
            promo = stripe.PromotionCode.create(
                coupon=coupon.id,
                max_redemptions=1,
                expires_at=expires_at_unix,
                code=code,  # Pass the full code here
            )
            with lock:
                expiry_str = expiry_date.strftime("%d/%m/%Y")
                offer_text = f"{coupon.percent_off:.0f}% off on the Group Essentials Subscription for {coupon.name} customers"
                writer.writerow([promo.code, expiry_str, offer_text])
            return True
        except stripe.error.RateLimitError:
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1}: {e}")
            return False

# 🕒 Progress tracking
start_time = time.time()
completed = 0
successful_codes = 0

print(f"🚀 Starting generation of {TOTAL_CODES} promo codes with {WORKER_COUNT} workers...")
print(f"📦 Fixed batch size: {BATCH_SIZE}\n")

try:
    while completed < TOTAL_CODES:
        remaining = TOTAL_CODES - completed
        batch = min(BATCH_SIZE, remaining)

        print(f"🔄 Starting batch of {batch} with {WORKER_COUNT} threads...")

        batch_start = time.time()
        success_count = 0

        with ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
            futures = [executor.submit(create_promo_code, i) for i in range(batch)]
            for i, future in enumerate(as_completed(futures), 1):
                if future.result():
                    success_count += 1
                if (completed + i) % 200 == 0:
                    print(f"✅ {completed + i} codes attempted...")

        batch_duration = time.time() - batch_start
        per_code_time = batch_duration / batch if batch else 1

        completed += batch
        successful_codes += success_count
        print(f"✔️ Batch complete: {success_count}/{batch} codes | {per_code_time:.2f}s/code | {completed}/{TOTAL_CODES} total\n")

        time.sleep(1)  # Cooldown for Stripe rate limits

except KeyboardInterrupt:
    print("\n⚠️ Interrupted by user. Saving progress...")

finally:
    csv_file.close()
    total_time = time.time() - start_time
    print(f"\n🏁 Finished. {successful_codes} promo codes generated in {int(total_time)} seconds.")