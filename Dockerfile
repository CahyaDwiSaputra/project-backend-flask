# 1. Gunakan Python versi ringan
FROM python:3.9-slim

# 2. Set folder kerja di dalam container
WORKDIR /app

# 3. Salin file requirements.txt ke dalam container
COPY requirements.txt .

# 4. Install library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# 5. Salin sisa kode (app.py, dll) ke dalam container
COPY . .

# 6. Buka port 5000 (pintu aplikasi Flask)
EXPOSE 5000

# 7. Perintah untuk menyalakan server saat container jalan
CMD ["python", "app.py"]