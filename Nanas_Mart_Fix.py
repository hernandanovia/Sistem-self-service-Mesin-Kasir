import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import qrcode
from PIL import Image, ImageTk
import os
from datetime import datetime  

# Fungsi untuk memuat data dari file CSV
def load_data():
    try:
        return pd.read_csv("barang.csv")

    except FileNotFoundError:
        messagebox.showerror("Error", "File barang.csv tidak ditemukan!")
        return pd.DataFrame(columns=["Nama Barang", "Harga"])

# Fungsi untuk menambahkan barang ke keranjang
def add_to_cart():
    selected_items = barang_listbox.curselection()
    for item in selected_items:
        item_name = barang_df.iloc[item]['Nama Barang']
        item_price = barang_df.iloc[item]['Harga']
        cart.append((item_name, item_price))
    update_cart_display()
 
# Fungsi untuk menambahkan barang ke keranjang
def add_to_cart():
    selected_items = barang_listbox.curselection()
    if not selected_items:
        messagebox.showerror("Error", "Pilih barang terlebih dahulu!")
        return

    for item in selected_items:
        item_name = barang_df.iloc[item]['Nama Barang']
        item_price = barang_df.iloc[item]['Harga']
        cart.append((item_name, item_price))
    update_cart_display()


# Fungsi untuk memperbarui tampilan keranjang
def update_cart_display():
    cart_listbox.delete(0, tk.END)
    total_price = 0
    for item_name, item_price in cart:
        cart_listbox.insert(tk.END, f"{item_name} - Rp{item_price}")
        total_price += item_price
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

    total_price = sum(item[1] for item in cart)
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

# Fungsi untuk menyelesaikan pembayaran
def finish_payment():
    if not cart:
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return
    cart.clear()
    update_cart_display()
    qr_label.config(image='')
    name_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Pembayaran selesai. Terima kasih!")

# Fungsi untuk mencetak struk belanja
def print_receipt():
    if not cart:
        messagebox.showerror("Error", "Keranjang belanja kosong!")
        return

    name = name_entry.get().strip()
    
    if not name:
        messagebox.showerror("Error", "Nama harus diisi!")
        return

    # Ambil tanggal dan waktu saat ini
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d-%m-%Y %H:%M:%S")  # Format tanggal: DD-MM-YYYY HH:MM:SS

    # Isi struk
    receipt_content = f"Struk Belanja\n"
    receipt_content += f"Tanggal: {formatted_date}\n"  # Tambahkan tanggal
    receipt_content += f"Nama: {name}\n"
    receipt_content += f"{'Nama Barang':<30}{'Harga':>10}\n"
    receipt_content += "-" * 40 + "\n"

    total_price = 0
    for item_name, item_price in cart:
        receipt_content += f"{item_name:<30}Rp{item_price:>10}\n"
        total_price += item_price
    
    receipt_content += "-" * 40 + "\n"
    receipt_content += f"{'Total':<30}Rp{total_price:>10}\n"
    receipt_content += "\nTerima kasih telah berbelanja!\n"


    # Simpan struk ke file teks
    receipt_path = "struk_belanja.txt"
    with open(receipt_path, "w") as file:
        file.write(receipt_content)

    messagebox.showinfo("Struk Belanja", f"Struk berhasil dicetak ke file '{receipt_path}'")
    
# Keluar dari program
def keluar():
    print("Terima kasih telah menggunakan program ini!")
    exit()


# Fungsi untuk menambahkan background ke frame
def add_background(frame, image_path):
    if os.path.exists(image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1366, 768), Image.Resampling.LANCZOS)  # Sesuaikan ukuran
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)  # Isi seluruh frame
      

# Fungsi untuk menampilkan frame tertentu
def show_frame(frame):
    frame.tkraise()

# Inisialisasi aplikasi
app = tk.Tk()
app.title("Nanas-Mart")
app.geometry("800x600")

# Muat data barang
barang_df = load_data()

# List barang
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

# Frame untuk Listbox dan Scrollbar
listbox_frame = tk.Frame(frame_barang)
listbox_frame.pack(padx=20, pady=20)

# Scrollbar untuk Listbox
scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)

# Listbox dengan Scrollbar
barang_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, width=100, height=15, yscrollcommand=scrollbar.set)
barang_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Konfigurasi Scrollbar
scrollbar.config(command=barang_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Muat barang ke Listbox
for index, row in barang_df.iterrows():
    barang_listbox.insert(tk.END, f"{row['Nama Barang']} - Rp{row['Harga']}")

# Tombol Tambah dan Lanjut
add_button = tk.Button(frame_barang, text="Tambah ke Keranjang", fg="black", bg="light sky blue", command=add_to_cart)
add_button.pack(pady=5)

next_button1 = tk.Button(frame_barang, text="Lanjut", fg="black", bg="light sky blue",command=lambda: show_frame(frame_keranjang))
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
keluar_button.pack(side=tk.RIGHT,padx=20, pady=20)
print_button = tk.Button(button_frame_pembayaran, text="Cetak Struk", command=print_receipt)
print_button.pack(pady=20)

# Tambahkan tombol untuk kembali ke Daftar Barang
back_to_barang_button = tk.Button(frame_pembayaran, text="Kembali ke Daftar Barang", command=lambda: show_frame(frame_barang))
back_to_barang_button.pack(side=tk.LEFT, padx=20, pady=20)

# tampilkan frame pertama
show_frame(frame_beranda)
app.mainloop()
