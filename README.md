Deskripsi
Aplikasi Chatroom dibuat dengan menggunakan Socket Programming dan protokol UDP menggunakan Python.
Program ini memungkinkan banyak klien berkomunikasi secara real-time melalui server yang mengatur pengiriman pesan.
Protokol UDP yang digunakan tidak membutuhkan koneksi, sehingga cocok untuk komunikasi cepat seperti pada chatroom.

Fitur
Protokol UDP Socket untuk Komunikasi: Menggunakan socket UDP yang cepat dan efisien untuk komunikasi antara klien dan server.
Threading di Server: Server menggunakan Threading untuk menangani banyak klien secara bersamaan, sehingga tidak ada penundaan dalam melayani pesan dari klien.
User Interface (GUI) dengan tkinter: Klien dan server memiliki antarmuka grafis yang mudah digunakan, dibuat dengan pustaka tkinter.
Autentikasi: Klien harus memasukkan password yang benar dan username unik sebelum bergabung dalam chatroom.
Broadcast Pesan: Pesan yang diterima oleh server dari satu klien akan diperlihatkan ke semua klien lain yang terhubung.
Menyimpan pesan : Program akan menyimpan pesan-pesan lampau meskipun telah ditutup baik di client maupun di server.
Enkripsi Pesan : Pesan akan dienkripsi menggunakan algoritma kriptografi modern RSA, jika pengguna ingin mengenkripsi pesannya dapat memencet tombol Send Encrypted

Kebutuhan
Python 3: Pastikan Anda memiliki Python versi 3 terinstal di perangkat Anda.

Cara Menjalankan Program
1. Menjalankan Server
Buka terminal atau command prompt dan jalankan file server.py
Tekan tombol "Start" untuk memulai server, yang akan menunggu klien untuk terhubung dan mengirim pesan.

2. Menjalankan Klien
Buka terminal lain atau gunakan perangkat lain dan jalankan file client.py
Pastikan Anda sudah mengubah IP di kode client.py agar sesuai dengan IP perangkat yang menjalankan server.
Setelah menjalankan client.py, pengguna akan diminta untuk memasukkan server ip, port, dan password.
Jika password benar, pengguna akan diminta untuk memasukkan username unik, tetapi jika salah pengguna akan diminta memasukkan ulang hingga benar.
Setelah proses autentikasi selesai, client dapat mengirim pesan yang akan diteruskan ke semua klien yang terhubung sehingga client yang lain dapat melihatnya.

yang akan diteruskan ke semua klien yang terhubung.

Pengembang
Muhammad Azizdzaki Khrisnanurmuflih / [18223128]
Leonard Arif Sutiono / [18223120]