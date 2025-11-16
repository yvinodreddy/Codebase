from PIL import Image
import os

issues_folder = "."
max_size = 1800  # Safe limit under 2000px

for filename in os.listdir(issues_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        filepath = os.path.join(issues_folder, filename)
        try:
            with Image.open(filepath) as img:
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    if filename.lower().endswith('.png'):
                        img.save(filepath, optimize=True)
                    else:
                        img.save(filepath, quality=85, optimize=True)
                    print(f"✅ Resized: {filename}")
                else:
                    print(f"⏭️  OK: {filename}")
        except Exception as e:
            print(f"❌ Error: {filename} - {e}")
print("✨ All images processed!")