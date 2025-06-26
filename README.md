# AntikaHub

AntikaHub is a Django-based web application for discovering, buying, and reviewing antiques and artworks. Users can browse products, view artist profiles, add items to cart or wishlist, and leave ratings and reviews.

---

## Features

- User registration, login, and profile management
- Browse products with images, descriptions, and prices
- View artist profiles with photo, biography, and their artworks
- Add products to cart and wishlist
- Place orders and view order history
- Rate and review products (with average rating display)
- Filter reviews by rating (highest, lowest, latest)
- Contact form with confirmation message
- "About Us" page

---

## Setup Instructions

1. **Clone the repository**

   ```sh
   git clone <your-repo-url>
   cd antikahub
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Apply migrations**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**

   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server**

   ```sh
   python manage.py runserver
   ```

6. **Access the site**

   - Visit `http://127.0.0.1:8000/` in your browser.
   - Visit `http://127.0.0.1:8000/admin/` for the Django admin.

---

## Media & Static Files

- Product and artist images are uploaded to the `media/` directory.
- Make sure your `settings.py` includes:
  ```python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
  ```
- In `urls.py`:
  ```python
  from django.conf import settings
  from django.conf.urls.static import static

  urlpatterns = [
      # ... your other urls ...
  ]

  if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

---

## Customization

- Update the `about.html` file for your own About Us content.
- Add or edit artists and products via Django admin.
- Adjust styles in the templates as needed.

---

## License

This project is for educational/demo purposes. Please add your own license if
