#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from logger import LOGGER
try:
   import os
   import heroku3
   from dotenv import load_dotenv
   from ast import literal_eval as is_enabled
   from pytgcalls.types.input_stream.quality import (
        HighQualityVideo,
        HighQualityAudio,
        MediumQualityAudio,
        MediumQualityVideo,
        LowQualityAudio,
        LowQualityVideo
    )

except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


class Config:
    #Telegram API Stuffs
    load_dotenv()  # load enviroment variables from .env file
    ADMIN = os.environ.get("ADMINS", '')
    SUDO = [int(admin) for admin in (ADMIN).split()] # Exclusive for heroku vars configuration.
    ADMINS = [int(admin) for admin in (ADMIN).split()] #group admins will be appended to this list.
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")

    #Stream Chat and Log Group
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")

    #Stream 
    STREAM_URL=os.environ.get("STARTUP_STREAM", None)
   
    #Database
    DATABASE_URI=os.environ.get("DATABASE_URI", None)
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "VCPlayerBot")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", None)
    APP_NAME=os.environ.get("HEROKU_APP_NAME", None)
    
    #Optional Configuration
    SHUFFLE=is_enabled(os.environ.get("SHUFFLE", 'True'))
    ADMIN_ONLY=is_enabled(os.environ.get("ADMIN_ONLY", "False"))
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", False)
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    #others
    
    RECORDING_DUMP=os.environ.get("RECORDING_DUMP", False)
    RECORDING_TITLE=os.environ.get("RECORDING_TITLE", False)
    TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")    
    IS_VIDEO=is_enabled(os.environ.get("IS_VIDEO", 'True'))
    IS_LOOP=is_enabled(os.environ.get("IS_LOOP", 'True'))
    DELAY=int(os.environ.get("DELAY", '10'))
    PORTRAIT=is_enabled(os.environ.get("PORTRAIT", 'False'))
    IS_VIDEO_RECORD=is_enabled(os.environ.get("IS_VIDEO_RECORD", 'True'))
    DEBUG=is_enabled(os.environ.get("DEBUG", 'False'))

    #Quality vars
    BITRATE=os.environ.get("BITRATE", False)
    FPS=os.environ.get("FPS", False)
    CUSTOM_QUALITY=os.environ.get("QUALITY", "HIGH")




    #Dont touch these, these are not for configuring player
    GET_FILE={}
    DATA={}
    STREAM_END={}
    SCHEDULED_STREAM={}
    DUR={}
    msg = {}

    SCHEDULE_LIST=[]
    playlist=[]

    STARTUP_ERROR=None

    ADMIN_CACHE=False
    CALL_STATUS=False
    YPLAY=False
    YSTREAM=False
    STREAM_SETUP=False
    LISTEN=False
    STREAM_LINK=False
    IS_RECORDING=False
    WAS_RECORDING=False
    PAUSE=False
    MUTED=False
    HAS_SCHEDULE=None
    IS_ACTIVE=None
    VOLUME=100
    CURRENT_CALL=None
    BOT_USERNAME=None
    USER_ID=None

    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    if not API_KEY or \
       not APP_NAME:
       HEROKU_APP=None
    else:
       HEROKU_APP=heroku3.from_key(API_KEY).apps()[APP_NAME]


    if EDIT_TITLE in ["NO", 'False']:
        EDIT_TITLE=False
        LOGGER.info("Title Editing turned off")
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        REPLY_PM=True
        LOGGER.info("Reply Message Found, Enabled PM MSG")
    else:
        REPLY_MESSAGE=None
        REPLY_PM=False

    if BITRATE:
       try:
          BITRATE=int(BITRATE)
       except:
          LOGGER.error("Invalid bitrate specified.")
          BITRATE=False
    else:
       BITRATE=False
    
    if FPS:
       try:
          FPS=int(FPS)
       except:
          LOGGER.error("Invalid FPS specified")
          if BITRATE:
             FPS=False
       if not FPS <= 30:
          FPS=False
    else:
       FPS=False

    if CUSTOM_QUALITY.lower() == 'high':
       VIDEO_Q=HighQualityVideo()
       AUDIO_Q=HighQualityAudio()
    elif CUSTOM_QUALITY.lower() == 'medium':
       VIDEO_Q=MediumQualityVideo()
       AUDIO_Q=MediumQualityAudio()
    elif CUSTOM_QUALITY.lower() == 'low':
       VIDEO_Q=LowQualityVideo()
       AUDIO_Q=LowQualityAudio()
    else:
       LOGGER.warning("Invalid QUALITY specified.Defaulting to High.")
       VIDEO_Q=HighQualityVideo()
       AUDIO_Q=HighQualityVideo()
   

    #help strings 
    PLAY_HELP="""
__Anda dapat bermain menggunakan salah satu opsi ini__


1. Putar video dari tautan YouTube.
   Perintah: **/play**
   __Anda dapat menggunakan ini sebagai balasan ke tautan YouTube atau meneruskan tautan bersama perintah. atau sebagai balasan pesan untuk mencarinya di YouTube.__

2. Putar dari file telegram.
   Perintah: **/play**
   __Balas ke media yang didukung (video dan dokumen atau file audio).__
 Catatan: __Untuk kedua kasus /fplay juga dapat digunakan oleh admin untuk memutar lagu segera tanpa menunggu antrian berakhir.__
3. Putar dari daftar putar YouTube
   Perintah: **/yplay**
   __Pertama dapatkan file playlist dari @musikkugroup atau @musikkuchannel dan balas file playlist.__

4. Siaran Langsung
   Perintah: **/stream**
   __Lewati URL streaming langsung atau URL langsung apa pun untuk memutarnya sebagai streaming.__

5. Impor daftar putar lama.
   Perintah: **/import**
   __Balas ke file daftar putar yang diekspor sebelumnya.
"""
    SETTINGS_HELP="""
** Anda dapat dengan mudah menyesuaikan pemain Anda sesuai kebutuhan Anda. Konfigurasi berikut tersedia:**

Perintah: **/settings**

KONFIGURASI YANG TERSEDIA:

**Mode Pemutar** - __Ini memungkinkan Anda menjalankan pemutar sebagai pemutar musik 24/7 atau hanya jika ada lagu dalam antrean.
Jika dinonaktifkan, pemain akan keluar dari panggilan saat daftar putar kosong.
Jika tidak, STARTUP_STREAM akan dialirkan saat id daftar putar kosong.__

**Video Diaktifkan** - __Ini memungkinkan Anda untuk beralih antara audio dan video.
jika dinonaktifkan, file video akan diputar sebagai audio.__

**Admin Only** - __Mengaktifkan ini akan membatasi pengguna non-admin menggunakan perintah play.__

**Edit Judul** - __Mengaktifkan ini akan mengedit judul VideoChat Anda menjadi nama lagu yang sedang diputar.__

**Mode Acak** - __Mengaktifkan ini akan mengacak daftar putar setiap kali Anda mengimpor daftar putar atau menggunakan /yplay __

**Balasan Otomatis** - __Pilih apakah akan membalas pesan PM dari akun pengguna yang sedang diputar.
Anda dapat mengatur pesan balasan khusus menggunakan konfigurasi `REPLY_MESSAGE`.__
"""
    SCHEDULER_HELP="""
__VCPlayer memungkinkan Anda menjadwalkan streaming.
Ini berarti Anda dapat menjadwalkan streaming untuk tanggal yang akan datang dan pada tanggal yang dijadwalkan, streaming akan diputar secara otomatis.
Saat ini Anda dapat menjadwalkan streaming bahkan untuk satu tahun!!. Pastikan Anda telah menyiapkan database, jika tidak, Anda akan kehilangan jadwal setiap kali pemutar dimulai ulang. __

Perintah: **/schedule**

__Balas file atau video youtube atau bahkan pesan teks dengan perintah jadwal.
Media balasan atau video youtube akan dijadwalkan dan akan diputar pada tanggal yang dijadwalkan.
Waktu penjadwalan secara default di IST dan Anda dapat mengubah zona waktu menggunakan konfigurasi `TIME_ZONE`.__

Perintah: **/slist**
__Lihat streaming terjadwal Anda saat ini.__

Perintah: **/cancel**
__Batalkan jadwal dengan id jadwalnya, Anda bisa mendapatkan id jadwal menggunakan perintah /slist__

Perintah: **/cancelall**
__Batalkan semua streaming terjadwal__
"""
    RECORDER_HELP="""
__Dengan VCPlayer Anda dapat dengan mudah merekam semua obrolan video Anda.
Secara default telegram memungkinkan Anda merekam untuk durasi maksimum 4 jam.
Upaya untuk mengatasi batas ini telah dilakukan dengan memulai ulang perekaman secara otomatis setelah 4 jam__

Perintah: **/record**

KONFIGURASI YANG TERSEDIA:
1. Rekam Video: __Jika diaktifkan, video dan audio streaming akan direkam, jika tidak, hanya audio yang akan direkam.__

2. Dimensi video: __Pilih antara dimensi potret dan lanskap untuk rekaman Anda__

3. Judul Rekaman Kustom: __Atur judul rekaman khusus untuk rekaman Anda. Gunakan perintah /rtitle untuk mengkonfigurasi ini.
Untuk menonaktifkan judul khusus, gunakan `/rtitle False `__

4. Merekam Bodoh: __Anda dapat mengatur penerusan semua rekaman Anda ke saluran, ini akan berguna karena jika tidak, rekaman akan dikirim ke pesan tersimpan dari akun streaming.
Setup menggunakan `RECORDING_DUMP` config.__

⚠️ Jika Anda memulai rekaman dengan vcplayer, pastikan Anda menghentikannya dengan vcplayer.
"""

    CONTROL_HELP="""
__VCPlayer memungkinkan Anda mengontrol streaming dengan mudah__
1. Lewati lagu.
    Perintah: **/skip**
    __Anda dapat melewati angka yang lebih besar dari 2 untuk melewati lagu di posisi tersebut.__

 2. Jeda pemutar.
    Perintah: **/pause**

 3. Lanjutkan pemutar.
    Perintah: **/resume**

 4. Ubah Volume.
    Perintah: **/volume**
    __Lewati volume di antara 1-200.__

 5. Tinggalkan VC.
    Perintah: **/leave**

 6. Acak daftar putar.
    Perintah: **/shuffle**

 7. Kosongkan antrean daftar putar saat ini.
    Perintah: **/clearplaylist**

 8. Cari videonya.
    Perintah: **/seek**
    __Anda dapat melewatkan beberapa detik untuk dilewati. Contoh: /seek 10 untuk melewati 10 detik. /seek -10 untuk memundurkan 10 detik.__

 9. Matikan suara pemutar.
    Perintah: **/mute**

 10. Suarakan pemutar.
    Perintah : **/unmute**

 11. Menampilkan daftar putar.
    Perintah: **/playlists**
    __Gunakan /player untuk ditampilkan dengan tombol kontrol__
 """

    ADMIN_HELP="""
__VCPlayer memungkinkan untuk mengontrol admin, yaitu Anda dapat menambahkan admin dan menghapusnya dengan mudah.
Disarankan untuk menggunakan database MongoDb untuk pengalaman yang lebih baik, jika tidak semua admin Anda akan direset setelah restart.__

Perintah: **/vcpromote**
__Anda dapat mempromosikan admin dengan nama pengguna atau id pengguna mereka atau dengan membalas pesan pengguna tersebut.__

Perintah: **/vcdemote**
__Hapus admin dari daftar admin__

Perintah: **/refresh**
"""

    MISC_HELP="""
Perintah: **/export**
__VCPlayer memungkinkan Anda mengekspor daftar putar Anda saat ini untuk penggunaan di masa mendatang.__
__Sebuah file json akan dikirimkan kepada Anda dan hal yang sama dapat digunakan bersama perintah /import.__

Perintah : **/logs**
__Jika pemutar Anda mengalami kesalahan, Anda dapat dengan mudah memeriksa log menggunakan /logs__
 
Perintah : **/env**
__Setup vars konfigurasi Anda dengan perintah /env.__
__Contoh: Untuk mengatur a__ `REPLY_MESSAGE` __use__ `/env REPLY_MESSAGE=Hai, Lihat @musikkuchannel daripada spam di PM`__
__Anda dapat menghapus var konfigurasi dengan menghilangkan nilai untuk itu, Contoh:__ `/env LOG_GROUP=` __ini akan menghapus konfigurasi LOG_GROUP yang ada.

Perintah: **/config**
__Sama seperti menggunakan /env**

Perintah: **/update**
__Memperbarui bot Anda dengan perubahan terbaru__

Tip: __Anda dapat dengan mudah mengubah konfigurasi CHAT dengan menambahkan akun pengguna dan akun bot ke grup lain dan perintah apa pun di grup baru__
"""
    ENV_HELP="""
**Ini adalah vars yang dapat dikonfigurasi yang tersedia dan Anda dapat mengaturnya masing-masing menggunakan perintah /env**


**Vars Wajib**

1. `API_ID` : __Dapatkan Dari [my.telegram.org](https://my.telegram.org/)__

2. `API_HASH` : __Dapatkan dari [my.telegram.org](https://my.telegram.org)__

3. `BOT_TOKEN` : __[@Botfather](https://telegram.dog/BotFather)__

4. `SESSION_STRING` : __Hasilkan Dari sini [GenerateStringName](https://repl.it/@subinps/getStringName)__

5. `CHAT` : __ID Channel/Grup tempat bot memutar Musik.__

6. `STARTUP_STREAM` : __Ini akan dialirkan pada startup dan restart bot.
Anda dapat menggunakan STREAM_URL apa pun atau tautan langsung dari video mana pun atau tautan Youtube Live.
Anda juga dapat menggunakan Daftar Putar YouTube. Temukan Tautan Telegram untuk daftar putar Anda dari [PlayList Dumb](https://telegram.dog/DumpPlaylist) atau dapatkan Daftar Putar dari [Ekstrak PlayList](https://telegram.dog/GetAPlaylistbot) .
Tautan Daftar Putar harus dalam bentuk `https://t.me/kenkanasw/xxx`.__

**Vars Opsional yang Direkomendasikan**

1. `DATABASE_URI`: __ Url database MongoDB, dapatkan dari [mongodb](https://cloud.mongodb.com). Ini adalah var opsional, tetapi disarankan untuk menggunakan ini untuk merasakan fitur lengkapnya.__

2. `HEROKU_API_KEY`: __Kunci api heroku Anda. Dapatkan satu dari [di sini](https://dashboard.heroku.com/account/applications/authorizations/new)__

3. `HEROKU_APP_NAME`: __Nama aplikasi heroku Anda.__

**Vars Opsional Lainnya**
1. `LOG_GROUP` : __Group untuk mengirim Playlist, jika CHAT adalah Group__

2. `ADMINS` : __ID pengguna yang dapat menggunakan perintah admin.__

3. `REPLY_MESSAGE` : __A membalas mereka yang mengirim pesan ke akun USER di PM. Biarkan kosong jika Anda tidak membutuhkan fitur ini. (Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /settings)__

4. `ADMIN_ONLY` : __Pass `True` Jika Anda ingin membuat perintah /play hanya untuk admin `CHAT`. Secara default /play tersedia untuk semua.(Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /settings)__

5. `DATABASE_NAME`: __Nama database untuk database mongodb Anda.mongodb__

6. `SHUFFLE` : __Jadikan `False` jika Anda tidak ingin mengacak playlist. (Dapat dikonfigurasi melalui tombol)__

7. `EDIT_TITLE` : __Jadikan `False` jika tidak ingin bot mengedit judul video chat sesuai lagu yang diputar. (Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /settings)__

8. `RECORDING_DUMP` : __A Channel ID dengan akun USER sebagai admin, untuk membuang rekaman video chat.__

9. `RECORDING_TITLE`: __Judul khusus untuk rekaman obrolan video Anda.__

10. `TIME_ZONE` : __Zona Waktu negara Anda, secara default IST__

11. `IS_VIDEO_RECORD` : __Jadikan `False` jika Anda tidak ingin merekam video, dan hanya audio yang akan direkam. (Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /record)__

12. `IS_LOOP` ; __Jadikan `False` jika Anda tidak ingin Obrolan Video 24/7. (Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /pengaturan)__

13. `IS_VIDEO` : __Jadikan `False` jika ingin menggunakan player sebagai pemutar musik tanpa video. (Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /settings)__

14. `PORTRAIT`: __Jadikan `True` jika Anda ingin merekam video dalam mode potret. (Dapat dikonfigurasi melalui tombol jika mongodb ditambahkan. Gunakan /record)__

15. `DELAY` : __Pilih batas waktu untuk menghapus perintah. 10 detik secara default.__

16. `QUALITY` : __Sesuaikan kualitas video chat, gunakan salah satu dari `high`, `medium`, `low` . __

17. `BITRATE` : __Bitrate audio (Tidak disarankan untuk diubah).__

18. `FPS` : __Fps video yang akan diputar (Tidak disarankan untuk diubah.)__

"""