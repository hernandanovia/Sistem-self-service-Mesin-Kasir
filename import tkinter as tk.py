import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import qrcode
import daftarbarang as db

# Fungsi untuk mengecek ketersediaan barang
def cek_barang(barang):
    if barang in barang_harga:
        return f"Barang tersedia, harga: {barang_harga[barang]}"
    else:
        return "Barang tidak tersedia"

# Data barang dan harga
barang_harga = {
    db
}

# Inisialisasi GUI
root = tk.Tk()
root.title("NanasMart")

# Variabel untuk menyimpan data belanja
total_harga = 0
daftar_belanja = []

# Fungsi untuk menambah barang ke daftar belanja
def tambah_barang():
    barang = simpledialog.askstring("Input", "Masukkan nama barang:")
    if barang == "done":
        return
    pesan = cek_barang(barang)
    if "tidak tersedia" in pesan:
        messagebox.showwarning("Peringatan", pesan)
    else:
        jumlah_beli = simpledialog.askinteger("Input", "Masukkan jumlah barang yang dibeli:")
        harga_barang = barang_harga[barang]
        harga_total = harga_barang * jumlah_beli
        global total_harga
        total_harga += harga_total
        daftar_belanja.append((barang, harga_barang, jumlah_beli, harga_total))
        list_belanja.insert(tk.END, f"{barang} ({jumlah_beli} x {harga_barang}): {harga_total}")

# Fungsi untuk menyelesaikan transaksi dan menampilkan struk
def selesai_transaksi():
    nama_pembeli = simpledialog.askstring("Input", "Nama pembeli:")
    waktu_transaksi = datetime.datetime.now()

    struk = f"Nama Pembeli: {nama_pembeli}\n"
    struk += f"Waktu Transaksi: {waktu_transaksi}\n"
    struk += "Daftar Belanja:\n"
    for barang, harga, jumlah, harga_total in daftar_belanja:
        struk += f"{barang} ({jumlah} x {harga}): {harga_total}\n"
    struk += f"Total Harga: {total_harga}\n"
    struk += "bersama NanasMart Happy Shopping! :)"

    # Menampilkan struk
    messagebox.showinfo("Struk Pembelian", struk)

    # Menyimpan struk ke file
    with open("struk_pembelian.txt", "w") as file:
        file.write(struk)

import qrcode

def create_gopay_qr(phone_number):
    # Pastikan qr_data diberi nilai sebelum digunakan
    qr_data = f"gopay://payment/{phone_number}"  # Menginisialisasi qr_data

    # Membuat objek QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Menambahkan data ke QR code
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Membuat gambar QR code
    img = qr.make_image(fill="black", back_color="white")
    img.save(f"gopay_qr_{phone_number}.png")

# Contoh pemanggilan fungsi
create_gopay_qr("085649876156")


# Untuk membuat QR tanpa jumlah pembayaran
create_gopay_qr("085649876156")

# GUI Layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

list_belanja = tk.Listbox(frame, width=50, height=10)
list_belanja.pack(padx=5, pady=5)

tambah_button = tk.Button(frame, text="Tambah Barang", command=tambah_barang)
tambah_button.pack(side=tk.LEFT, padx=5, pady=5)

selesai_button = tk.Button(frame, text="Selesai Transaksi", command=selesai_transaksi)
selesai_button.pack(side=tk.RIGHT, padx=5, pady=5)

root.mainloop()

