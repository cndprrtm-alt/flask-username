from flask import Flask, redirect, url_for, abort
import re

app = Flask(__name__)

# Data contoh produk toko
PRODUK = {
    1: {"nama": "Kaos", "harga": 75000},
    2: {"nama": "Hoodie", "harga": 150000},
    3: {"nama": "Tas", "harga": 100000}
}

# Data contoh member
MEMBER = ["cindu", "budi", "siti"]


def halaman(judul, isi):
    menu = f"""
    <nav>
        <a href="{url_for('beranda')}">Beranda</a> |
        <a href="{url_for('tentang')}">Tentang</a> |
        <a href="{url_for('produk')}">Produk</a> |
        <a href="{url_for('kontak')}">Kontak</a>
    </nav>
    """
    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>{judul}</title>
    </head>
    <body>
        {menu}
        <hr>
        <h1>{judul}</h1>
        {isi}
    </body>
    </html>
    """


# 1. Route statis: beranda
@app.route("/")
def beranda():
    isi = """
    <p>Selamat datang di Toko Online Sederhana!</p>
    <p>Cek username member melalui formulir berikut.</p>
    <form action="/cek" method="get">
        <input name="username" placeholder="Masukkan username" required>
        <button type="submit">Cek Username</button>
    </form>
    <p>Contoh: cindu, budi, atau siti.</p>
    """
    return halaman("Beranda", isi)


# 2. Route statis: tentang
@app.route("/tentang")
def tentang():
    return halaman(
        "Tentang Kami",
        "<p>Toko online sederhana untuk latihan Flask.</p>"
    )


# 3. Route statis: daftar produk
@app.route("/produk")
def produk():
    isi = "<ul>"
    for id_produk, data in PRODUK.items():
        link = url_for("produk_detail", id=id_produk)
        isi += (
            f'<li><a href="{link}">{data["nama"]}</a> '
            f'- Rp{data["harga"]:,}</li>'
        )
    isi += "</ul>"
    return halaman("Daftar Produk", isi)


# 4. Route statis: kontak
@app.route("/kontak")
def kontak():
    return halaman(
        "Kontak",
        "<p>Email: toko@example.com</p>"
    )


# Validasi username: 3-20 karakter, huruf, angka, underscore
def username_valid(username):
    return re.fullmatch(r"[A-Za-z0-9_]{3,20}", username) is not None


# 5. Route dinamis untuk pengecekan username
@app.route("/cek/<username>")
def cek_username(username):
    if not username_valid(username):
        return halaman(
            "Username Tidak Valid",
            "<p>Username harus 3-20 karakter dan hanya "
            "boleh berisi huruf, angka, atau underscore.</p>"
        ), 400

    # Redirect menggunakan url_for
    return redirect(url_for("user_profile", username=username))


# Form beranda mengirim username melalui query string
@app.route("/cek")
def cek_form():
    from flask import request

    username = request.args.get("username", "").strip()

    if not username_valid(username):
        return halaman(
            "Username Tidak Valid",
            "<p>Username harus 3-20 karakter dan hanya "
            "boleh berisi huruf, angka, atau underscore.</p>"
        ), 400

    return redirect(url_for("user_profile", username=username))


# 6. Route dinamis: profil member
@app.route("/user/<username>")
def user_profile(username):
    if not username_valid(username):
        return halaman(
            "Username Tidak Valid",
            "<p>Format username tidak sesuai.</p>"
        ), 400

    if username.lower() in MEMBER:
        status = "Username terdaftar sebagai member."
    else:
        status = "Format valid, tetapi username belum terdaftar."

    isi = f"""
    <p>Username: <b>{username}</b></p>
    <p>{status}</p>
    """
    return halaman("Profil Member", isi)


# 7. Route dinamis dengan converter int
@app.route("/produk/<int:id>")
def produk_detail(id):
    if id not in PRODUK:
        abort(404)

    data = PRODUK[id]
    isi = f"""
    <p>Nama produk: {data['nama']}</p>
    <p>Harga: Rp{data['harga']:,}</p>
    """
    return halaman("Detail Produk", isi)


# Custom halaman error 404
@app.errorhandler(404)
def halaman_tidak_ditemukan(error):
    return halaman(
        "404 - Halaman Tidak Ditemukan",
        """
        <p>Maaf, halaman atau produk yang kamu cari tidak ditemukan.</p>
        <p><a href="/">Kembali ke Beranda</a></p>
        """
    ), 404


if __name__ == "__main__":
    app.run(debug=True)