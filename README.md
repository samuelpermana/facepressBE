
<body>
    <h1>README - Setup Django Rest Framework</h1>
    <p>Untuk menginstal paket yang diperlukan untuk proyek Django Rest Framework Anda, silakan jalankan perintah berikut satu per satu di terminal Anda:</p>
    <pre>
pip install asgiref==3.8.1
pip install Django==5.1.1
pip install django-cors-headers==4.4.0
pip install django-extensions==3.2.3
pip install djangorestframework==3.15.2
pip install djangorestframework-simplejwt==5.3.1
pip install PyJWT==2.9.0
pip install PyMySQL==1.1.1
pip install sqlparse==0.5.1
pip install tzdata==2024.2
    </pre>
    <p>Jika Anda ingin menginstal <code>setuptools</code> dan <code>pip</code>, gunakan perintah berikut:</p>
    <pre>
pip install setuptools==65.5.0
pip install pip==23.2.1
    </pre>

    <h2>Aktifkan Virtual Environment</h2>
    <p>Pastikan Anda telah mengaktifkan virtual environment sebelum menjalankan perintah di atas untuk menghindari konflik dengan paket lain di sistem Anda. Untuk mengaktifkan virtual environment, jalankan:</p>
    <pre>
# Di Windows
.\env\bin\activate

    </pre>

    <h2>Pengaturan Database</h2>
    <p>Setelah menginstal semua paket, jalankan perintah berikut untuk mengatur database:</p>
    <pre>
python manage.py makemigrations
python manage.py migrate
    </pre>

    <h2>Menjalankan Server</h2>
    <p>Setelah database disiapkan, jalankan server Django dengan perintah:</p>
    <pre>
python manage.py runserver
    </pre>

    <p>Selamat, proyek Django Rest Framework Anda sekarang telah siap untuk digunakan!</p>
</body>
</html>
