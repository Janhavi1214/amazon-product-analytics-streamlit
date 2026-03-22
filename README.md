# 🛒 amazon-analytics-streamlit

An interactive data analytics dashboard built with **Streamlit** and **SQLite** to explore and visualize Amazon product data — including pricing, ratings, discounts, and trending products.

---

## 📸 Features

- **Dynamic Filters** — Filter products by category, price range, and rating from the sidebar
- **Interactive Visualizations** — Powered by Matplotlib and Seaborn:
  - Rating distribution by category (box plot)
  - Top categories by average rating (bar chart)
  - Average discount by category
  - Rating vs. discounted price (scatter plot)
  - Top products by rating count
- **Trending Products** — Surfaces high-engagement products (rating count > 1000)
- **Deals of the Day** — Lists products with 50%+ discount

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| UI / App | Streamlit |
| Data | SQLite + Pandas |
| Visualizations | Matplotlib, Seaborn |
| Language | Python 3.x |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/amazon-analytics-streamlit.git
cd amazon-analytics-streamlit
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up the database

Make sure `amazon_data.db` (SQLite) is in the project root. The database should have a `products` table with at least these columns:

| Column | Type |
|---|---|
| `product_name` | TEXT |
| `main_category` | TEXT |
| `discounted_price` | REAL |
| `actual_price` | REAL |
| `discount_percentage` | REAL |
| `rating` | REAL |
| `rating_count` | INTEGER |

> You can source this data from the [Amazon Sales Dataset on Kaggle](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset).

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
amazon-analytics-streamlit/
├── app.py               # Main Streamlit application
├── amazon_data.db       # SQLite database (not tracked in git)
├── requirements.txt
└── README.md
```

---

## ⚠️ Known Issues / Improvements

- `matplotlib as plt` import alias is non-standard — should be `import matplotlib.pyplot as plt`
- `@st.cache_resource` on the DB connection can cause stale reads; consider using `st.cache_data` with TTL for dynamic data
- Parameterized queries use `?` placeholders correctly — safe from SQL injection ✅

---

## 📄 License

MIT
