# 🎟️ Generate Stripe Coupons + Promotion Codes

A small Python script to generate a single Stripe coupon and multiple unique promotion codes, and save them all to a CSV file.

---

## 💡 What I Learned (That Might Save You Time)

Stripe **coupons** and **promotion codes** are _not the same thing_:

- A **coupon** defines the discount you want to offer — e.g., 25% off, $20 off, etc.
- A **promotion code** is what your customers actually use — it links to the coupon.

So, instead of creating 1,000 separate coupons, the correct approach is:
> Create **one** coupon, and generate **1,000** promo codes attached to it.

---

## 🚀 How to Run the Script

### 1. Install Dependencies

```bash
pip install stripe python-dotenv
```

### 2. Add Your Stripe Secret Key

Create a `.env` file in the project directory with this line:

```
STRIPE_API_KEY=sk_live_your_secret_key_here
```

⚠️ **Important**: This is your _secret_ API key from the Stripe dashboard — not the public one.

### 3. Run the Script

```bash
python generate_coupons.py
```

---

## ⚙️ What the Script Does

- Creates a single coupon (e.g., 25% off)
- Generates 1,000+ unique promotion codes tied to that coupon
- Saves them in a file called `promotion_codes.csv`

Example CSV output:

```
WT7KEHFS
LIIO8NK5
AFMFDSBL
...
```

---

## 🛠️ Customising the Script

Inside `generate_coupons.py`, you can edit:

| Variable         | Description                                  |
|------------------|----------------------------------------------|
| `percent_off`    | Percentage discount (e.g. 25)                |
| `expires_at`     | Expiry date for each promo code              |
| `TOTAL_CODES`    | Number of promo codes to generate            |
| `max_redemptions`| How many times each code can be used         |
| `metadata`       | Optional: tag with `product_id`, etc.        |

---

## 📁 Project Notes

- Promo codes are saved to `promotion_codes.csv`
- The script handles retries and basic rate limiting
- Python 3.12+ recommended

---

## 📦 .gitignore

This project includes a `.gitignore` that excludes:

```
.env
__pycache__/
.DS_Store
.vscode/
.idea/
```

So your secrets and local system files won’t get committed.

---

## ✅ Final Tip

Make sure you have permission to write files in your directory, and that your API key is active and scoped to allow coupon/promo code creation.

Happy coding — and good luck!
