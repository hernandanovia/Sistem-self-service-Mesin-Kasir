import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import qrcode
from PIL import Image, ImageTk
import os
from datetime import datetime  
import csv

# Fungsi untuk memuat data dari file CSV
def load_data():
    try:
        return pd.read_csv("barang.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "File barang.csv tidak ditemukan!")
        return pd.DataFrame(columns=["Nama Barang", "Harga"])

# Fungsi untuk menambahkan barang ke keranjang
def add_to_cart():
    selected_index = barang_combobox.current()
    jumlah_barang = jumlah_entry.get()
    
    if selected_index == -1 or not jumlah_barang.isdigit():
        messagebox.showerror("Error", "Pilih barang dan masukkan jumlah terlebih dahulu!")
        return

    selected_item = barang_df.iloc[selected_index]
    item_name = selected_item['Nama Barang']
    item_price = selected_item['Harga']
    jumlah = int(jumlah_barang)
    
    # Update keranjang dengan menambahkan jumlah barang yang sama
    for item in cart:
        if item[0] == item_name:
            item[2] += jumlah  # Tambahkan jumlah barang yang sama
            update_cart_display()
            return

    cart.append((item_name, item_price, jumlah))  # Menambahkan barang baru
    update_cart_display()

# Fungsi untuk memperbarui tampilan keranjang
def update_cart_display():
    cart_listbox.delete(0, tk.END)
    total_price = 0
    for item_name, item_price, quantity in cart:
        subtotal = item_price * quantity
        cart_listbox.insert(tk.END, f"{item_name} x {quantity} - Rp{subtotal}")
        total_price += subtotal
    total_label.config(text=f"Total: Rp{total_price}")

# Fungsi untuk menghasilkan QR Code
def generate_qr():
    if not cart:
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return

    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Nama harus diisi!")
        return

    total_price = sum(item[1] * item[2] for item in cart)
    payment_info = f"Pembayaran oleh {name} \nTotal: Rp{total_price}"

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(payment_info)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_path = "qr_code.png"
    qr_img.save(qr_img_path)

    qr_image = Image.open(qr_img_path)
    qr_image_tk = ImageTk.PhotoImage(qr_image)
    qr_label.config(image=qr_image_tk)
    qr_label.image = qr_image_tk

# Fungsi untuk menyelesaikan pembayaran (tanpa mencetak struk)
def finish_payment():
    if not cart:
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return

    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Nama harus diisi!")
        return

    total_price = sum(item[1] * item[2] for item in cart)
    formatted_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Simpan ke database, tetapi tidak mencetak ke file struk
    save_receipt_to_csv(name, formatted_date, cart, total_price)


    # Reset keranjang dan input
    cart.clear()
    update_cart_display()
    qr_label.config(image="")
    name_entry.delete(0, tk.END)

    messagebox.showinfo("Sukses", "Pembayaran selesai. Terima kasih telah berbelanja!")

# Fungsi untuk memastikan database CSV tersedia
def initialize_receipt_db():
    if not os.path.exists("receipt_database.csv"):
        with open("receipt_database.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Tanggal", "Nama Pembeli", "Nama Barang", "Harga", "Total"])

# Fungsi untuk memuat database struk
def load_receipt_database():
    if os.path.exists("receipt_database.csv"):
        return pd.read_csv("receipt_database.csv")
    else:
        # Jika file tidak ada, buat dengan header yang sesuai
        initialize_receipt_db()
        return pd.read_csv("receipt_database.csv")

# Fungsi untuk menyimpan struk belanja ke database CSV (dengan pencegahan duplikasi)
def save_receipt_to_csv(name, formatted_date, cart, total_price):
    # Muat database struk
    receipt_db = load_receipt_database()

    # Gabungkan data transaksi baru menjadi satu string untuk validasi
    new_transaction = f"{formatted_date}|{name}|{cart}|{total_price}"

    # Periksa apakah transaksi sudah ada
    if not receipt_db.empty:
        for index, row in receipt_db.iterrows():
            existing_transaction = f"{row['Tanggal']}|{row['Nama Pembeli']}|{row['Nama Barang']}|{row['Total']}"
            if new_transaction == existing_transaction:
                messagebox.showinfo("Info", "Transaksi sudah tersimpan sebelumnya.")
                return  # Tidak menambahkan transaksi yang sama

    # Simpan transaksi baru
    with open("receipt_database.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([formatted_date, name, "", "", ""])
        for item_name, item_price, quantity in cart:
            subtotal = item_price * quantity
            writer.writerow(["", "", item_name, item_price, subtotal])
        writer.writerow(["", "", "", "Total", total_price])

    messagebox.showinfo("Sukses", "Transaksi berhasil disimpan!")

# Fungsi untuk menyimpan struk belanja ke database CSV
def save_receipt_to_csv(name, formatted_date, cart, total_price):
    with open("receipt_database.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([formatted_date, name, "", "", ""])
        for item_name, item_price, quantity in cart:
            subtotal = item_price * quantity
            writer.writerow(["", "", item_name, item_price, subtotal])
        writer.writerow(["", "", "", "Total", total_price])

# Fungsi untuk mencetak struk belanja (hanya mencetak dan menyimpan ke file struk)
def print_receipt():
    if not cart:
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return

    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Nama harus diisi!")
        return

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

    receipt_content = f"Struk Belanja\n"
    receipt_content += f"Tanggal: {formatted_date}\n"
    receipt_content += f"Nama: {name}\n"
    receipt_content += f"{'Nama Barang':<30}{'Jumlah':>10}{'Harga':>10}{'Subtotal':>10}\n"
    receipt_content += "-" * 70 + "\n"

    total_price = 0
    for item_name, item_price, quantity in cart:
        subtotal = item_price * quantity
        receipt_content += f"{item_name:<30}{quantity:>10}{'Rp':>5}{item_price:>10}{'Rp':>5}{subtotal:>15}\n"
        total_price += subtotal
    
    receipt_content += "-" * 75 + "\n"
    receipt_content += f"{'Total':<55}{'Rp':>5}{total_price:>15}\n"
    receipt_content += "\nTerima kasih telah berbelanja!\n"

    receipt_path = "struk_belanja.txt"
    with open(receipt_path, "w") as file:
        file.write(receipt_content)

    messagebox.showinfo("Struk Belanja", f"Struk berhasil dicetak ke file '{receipt_path}'.")

# Keluar dari program
def keluar():
    print("Terima kasih telah menggunakan program ini!")
    exit()

# Fungsi untuk menambahkan background ke frame
def add_background(frame, image_path):
    if os.path.exists(image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1366, 768), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)

# Fungsi untuk menampilkan frame tertentu
def show_frame(frame):
    frame.tkraise()

# Inisialisasi aplikasi
app = tk.Tk()
app.title("Nanas-Mart")
app.geometry("800x600")

# Muat data barang
barang_df = load_data()
cart = []

# Frame untuk setiap bagian
frame_beranda = tk.Frame(app)
frame_barang = tk.Frame(app)
frame_keranjang = tk.Frame(app)
frame_data_pengguna = tk.Frame(app)
frame_pembayaran = tk.Frame(app)
frame_struk = tk.Frame(app)

# Path gambar untuk background
image_path = "MART (Presentasi).png"

# Tambahkan background ke semua frame
for frame in (frame_beranda, frame_barang, frame_keranjang, frame_data_pengguna, frame_pembayaran, frame_struk):
    frame.grid(row=0, column=0, sticky='nsew')
    add_background(frame, image_path)

# Konfigurasi pusat untuk setiap frame
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# --- Beranda Aplikasi ---
tk.Label(frame_beranda, text="Selamat Datang di Nanas-Mart", font=("Arial", 25), fg="navy").pack(pady=20)
tk.Label(frame_beranda, text="Solusi Belanja Mudah, Cepat, dan Praktis!", font=("Arial", 16), fg="navy").pack(pady=10)

start_button = tk.Button(
    frame_beranda,
    text="Mulai Belanja",
    font=("Arial", 16),
    bg="navy",
    fg="white",
    command=lambda: show_frame(frame_barang)
)
start_button.pack(pady=20)

exit_button = tk.Button(
    frame_beranda,
    text="Keluar",
    font=("Arial", 16),
    bg="red",
    fg="white",
    command=keluar
)
exit_button.pack(pady=10)

# --- Bagian Daftar Barang ---
tk.Label(frame_barang, text="Daftar Barang", font=("Arial", 25), bg="light sky blue").pack(pady=10)

# Frame untuk input jumlah barang
jumlah_frame = tk.Frame(frame_barang)
jumlah_frame.pack(padx=20, pady=20)

barang_combobox = ttk.Combobox(jumlah_frame, values=[row['Nama Barang'] for index, row in barang_df.iterrows()], width=60)
barang_combobox.set("Pilih Barang")
barang_combobox.pack(side=tk.LEFT, padx=5)

jumlah_label = tk.Label(jumlah_frame, text="Jumlah:", font=("Arial", 16), bg="light sky blue")
jumlah_label.pack(side=tk.LEFT, padx=5)
jumlah_entry = tk.Entry(jumlah_frame, width=10)
jumlah_entry.pack(side=tk.LEFT, padx=5)

# Tombol Tambah ke Keranjang
add_button = tk.Button(frame_barang, text="Tambah ke Keranjang", fg="black", bg="light sky blue", command=add_to_cart)
add_button.pack(pady=5)

next_button1 = tk.Button(frame_barang, text="Lanjut", fg="black", bg="light sky blue", command=lambda: show_frame(frame_keranjang))
next_button1.pack(pady=20)

# --- Bagian Keranjang Belanja ---
tk.Label(frame_keranjang, text="Keranjang Belanja", font=("Arial", 18)).pack(pady=10)
cart_listbox = tk.Listbox(frame_keranjang, width=100, height=15)
cart_listbox.pack(padx=20, pady=20)
total_label = tk.Label(frame_keranjang, text="Total: Rp0", font=("Arial", 18))
total_label.pack()

button_frame_keranjang = tk.Frame(frame_keranjang)
button_frame_keranjang.pack(pady=20)
back_button1 = tk.Button(button_frame_keranjang, text="Kembali", command=lambda: show_frame(frame_barang))
back_button1.pack(side=tk.LEFT, padx=20)
next_button2 = tk.Button(button_frame_keranjang, text="Lanjut", command=lambda: show_frame(frame_data_pengguna))
next_button2.pack(side=tk.RIGHT, padx=20)

# --- Bagian Input Nama dan ID ---
tk.Label(frame_data_pengguna, text="Data Pembeli", font=("Arial", 18)).pack(pady=10)
tk.Label(frame_data_pengguna, text="Nama:", font=("Arial", 16)).pack(pady=20)
name_entry = tk.Entry(frame_data_pengguna)
name_entry.pack(pady=20)

button_frame_data_pengguna = tk.Frame(frame_data_pengguna)
button_frame_data_pengguna.pack(pady=20)
back_button2 = tk.Button(button_frame_data_pengguna, text="Kembali", command=lambda: show_frame(frame_keranjang))
back_button2.pack(side=tk.LEFT, padx=20)
next_button3 = tk.Button(button_frame_data_pengguna, text="Lanjut", command=lambda: show_frame(frame_pembayaran))
next_button3.pack(side=tk.RIGHT, padx=20)

# --- Bagian Pembayaran dan QR Code ---
tk.Label(frame_pembayaran, text="Pembayaran", font=("Arial", 18)).pack(pady=10)
generate_button = tk.Button(frame_pembayaran, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=20)

qr_label = tk.Label(frame_pembayaran)
qr_label.pack(pady=20)

button_frame_pembayaran = tk.Frame(frame_pembayaran)
button_frame_pembayaran.pack(pady=20)
back_button3 = tk.Button(button_frame_pembayaran, text="Kembali", command=lambda: show_frame(frame_data_pengguna))
back_button3.pack(side=tk.LEFT, padx=20)
finish_button = tk.Button(button_frame_pembayaran, text="Selesai & Bayar", command=finish_payment, bg="green", fg="white")
finish_button.pack(side=tk.RIGHT, padx=20)
keluar_button = tk.Button(frame_pembayaran, text='Keluar', command=keluar, bg='red', fg='white')
keluar_button.pack(side=tk.RIGHT, padx=20, pady=20)
print_button = tk.Button(button_frame_pembayaran, text="Cetak Struk", command=print_receipt)
print_button.pack(pady=20)

# Tambahkan tombol untuk kembali ke Daftar Barang
back_to_barang_button = tk.Button(frame_pembayaran, text="Kembali ke Daftar Barang", command=lambda: show_frame(frame_barang))
back_to_barang_button.pack(side=tk.LEFT, padx=20, pady=20)

# Tampilkan frame pertama
show_frame(frame_beranda)
app.mainloop()
