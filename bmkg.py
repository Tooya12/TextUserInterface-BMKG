"""
Author: Ayzalme
Github: Tooya12
"""

import httpx
import sys
import time
import ujson
from glob import glob
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from mod import zalsTime as zt
from mod import cacheTime


class getBmkgWebsite:
    def __init__(self):
        self.cacheName = "cache.json"
        self.nameConfig = "configCuaca.json"
        self.configWilayah = "kepmendagri-2022.json"
        self.cmd = [
            "help",
            "ganti-provinsi",
            "version",
            "daftar-kelurahan/desa",
            "daftar-provinsi",
            "ganti-kelurahan/desa",
            "ganti-kecamatan",
            "ganti-kabupaten/kota",
            "daftar-kelurahan/desa",
            "daftar-kecamatan",
            "daftar-kabupaten/kota",
        ]
        self.cmdQuit = ["exit", "quit"]
        self.promptStr = ">>> "
        self.universalExit = False
        self.zalTime = zt.zalsTime()
        self.console = Console()
        self.configCuaca = glob(self.nameConfig)

        """ Wilayah var """
        self.provinsi = None
        self.kabupatenKota = None
        self.kecamatan = None
        self.kelurahanDesa = None

        with open(self.configWilayah) as file:
            self.rawDataWilayah = file.read()
            file.close()

        self.jsonWilayah = ujson.loads(self.rawDataWilayah)

        """ API URL BMKG """
        self.url = "https://api.bmkg.go.id/publik/prakiraan-cuaca"
        self.wilayah = None

        """ Set user-agent """
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
        }
        self.parameters = {}

    def requestBmkg(self):
        self.console.print(
            "[yellow]Mengambil data BMKG... :smiling_face_with_sunglasses:\n"
        )

        try:
            self.request = httpx.get(
                self.url, headers=self.headers, params=self.parameters
            )
            self.response = self.request.raise_for_status()
            self.responseDump = ujson.dumps(self.response.json(), indent=4)

        except httpx.RequestError as err:
            self.console.print(
                f"[bold red]Error untuk terhubung ke {err.request.url}.\n"
            )
            self.console.print("Mohon periksa jaringan anda!.")
            sys.exit(1)

        except httpx.HTTPStatusError as err:
            self.console.print(
                f"[bold red]Error response {err.response.status_code} ketika terhubung ke {err.request.url}."
            )
            sys.exit(1)

        with open(self.cacheName, "w") as file:
            file.write(self.responseDump)
            file.close()

        self.console.print("[green]Berhasil mengambil data BMKG :face_savoring_food:\n")

    def parserDataHTML(self):
        self.console.print("[yellow]Menyusun data BMKG...:face_with_monocle:\n")

        with open(self.cacheName) as file:
            self.rawData = file.read()
            file.close()

        """ Loads all Json """
        self.jsonData = ujson.loads(self.rawData)
        self.dataCuaca = self.jsonData["data"][0]["cuaca"]
        self.dataLokasi = self.jsonData["data"][0]["lokasi"]

        self.lengthDataCuaca = len(self.dataCuaca)
        self.checkPoint = 1

        self.dictCuaca = {}
        self.dictLokasi = {
            "Provinsi": self.dataLokasi["provinsi"],
            "Kota/Kabupaten": self.dataLokasi["kotkab"],
            "Kecamatan": self.dataLokasi["kecamatan"],
            "Desa": self.dataLokasi["desa"],
        }

        def convertMataAngin(mataAngin):
            listMataAnginEng = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            listMataAnginInd = [
                "Utara",
                "Timur Laut",
                "Timur",
                "Tenggara",
                "Selatan",
                "Barat Daya",
                "Barat",
                "Barat Laut",
            ]
            indexMataAngin = listMataAnginEng.index(mataAngin)

            return listMataAnginInd[indexMataAngin]

        self.dateCheckPoint = None

        for repeat in range(self.lengthDataCuaca):
            for index, itter in enumerate(self.dataCuaca[repeat]):
                self.time = self.zalTime.isoToDefault(itter["datetime"])
                self.date = self.time.split()[2]

                if index == 0 and repeat == 0:
                    self.dateCheckPoint = self.date

                    self.dictCuaca.update(
                        {
                            f"{self.dateCheckPoint}": {
                                f"{self.checkPoint}": {
                                    "Waktu": self.time,
                                    "Cuaca": itter["weather_desc"],
                                    "Suhu": str(itter["t"]) + " °C",
                                    "Tutupan Awan": str(itter["tcc"]) + "%",
                                    "Jarak Pandang": itter["vs_text"],
                                    "Kelembapan Udara": str(itter["hu"]) + "%",
                                    "Kecepatan Angin": str(itter["ws"]) + " km/jam",
                                    "Arah Angin": convertMataAngin(itter["wd"]),
                                }
                            }
                        }
                    )

                    self.checkPoint += 1
                    continue

                if self.dateCheckPoint == self.date:
                    self.dictCuaca[f"{self.dateCheckPoint}"].update(
                        {
                            f"{self.checkPoint}": {
                                "Waktu": self.time,
                                "Cuaca": itter["weather_desc"],
                                "Suhu": str(itter["t"]) + " °C",
                                "Tutupan Awan": str(itter["tcc"]) + "%",
                                "Jarak Pandang": itter["vs_text"],
                                "Kelembapan Udara": str(itter["hu"]) + "%",
                                "Kecepatan Angin": str(itter["ws"]) + " km/jam",
                                "Arah Angin": convertMataAngin(itter["wd"]),
                            }
                        }
                    )

                    self.checkPoint += 1

                else:
                    self.dateCheckPoint = self.date
                    self.checkPoint = 1

                    self.dictCuaca.update(
                        {
                            f"{self.dateCheckPoint}": {
                                f"{self.checkPoint}": {
                                    "Waktu": self.time,
                                    "Cuaca": itter["weather_desc"],
                                    "Suhu": str(itter["t"]) + " °C",
                                    "Tutupan Awan": str(itter["tcc"]) + "%",
                                    "Jarak Pandang": itter["vs_text"],
                                    "Kelembapan Udara": str(itter["hu"]) + "%",
                                    "Kecepatan Angin": str(itter["ws"]) + " km/jam",
                                    "Arah Angin": convertMataAngin(itter["wd"]),
                                }
                            }
                        }
                    )

                    self.checkPoint += 1

        self.console.print(
            "[green]Berhasil menyusun data BMKG...:face_savoring_food:\n"
        )

    def showingResult(self):
        self.console.print("\n[green]Initialisasi...:face_with_monocle:\n")

        """ Table Content """

        def makeTable():
            waktuSekarang = self.zalTime.timeNow()
            tanggalSekarang = waktuSekarang.split()[2]
            repeat = len(self.dictCuaca[tanggalSekarang])

            """ Judul Stuff """
            waktuIndo = self.zalTime.translateToIndo(
                self.dictCuaca[tanggalSekarang]["1"]["Waktu"]
            )
            hari = waktuIndo.split()[0]
            tanggal = " ".join(waktuIndo.split()[2:])
            text = Text("Cuaca Saat Ini", justify="center")
            judul = " - ".join(
                [
                    self.dictLokasi["Provinsi"],
                    self.dictLokasi["Kota/Kabupaten"],
                    self.dictLokasi["Kecamatan"],
                    self.dictLokasi["Desa"],
                ]
            )
            judulTable = (
                f"[bold dodger_blue1]Prakiraan Cuaca BMKG\n{judul}\n\n{hari} {tanggal}"
            )

            self.console.print(judulTable, justify="center")

            for loop in range(repeat):
                jam = self.dictCuaca[tanggalSekarang][str(loop + 1)]["Waktu"].split()[1]
                fullJam = self.dictCuaca[tanggalSekarang][str(loop + 1)]["Waktu"]
                text = Text(f"{jam}", justify="center")
                compareTime = self.zalTime.timeCompare(fullJam, waktuSekarang)

                if not compareTime and not loop + 1 == repeat:
                    continue

                table = Table(expand=True, style="blue")
                table.add_column(text, justify="full", no_wrap=True)
                table.add_row(
                    f"Cuaca            : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Cuaca"]}"
                )
                table.add_row(
                    f"Suhu             : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Suhu"]}"
                )
                table.add_row(
                    f"Tutupan Awan     : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Tutupan Awan"]}"
                )
                table.add_row(
                    f"Jarak Pandang    : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Jarak Pandang"]}"
                )
                table.add_row(
                    f"Kelembapan Udara : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Kelembapan Udara"]}"
                )
                table.add_row(
                    f"Kecepatan Angin  : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Kecepatan Angin"]}"
                )
                table.add_row(
                    f"Arah Angin       : {self.dictCuaca[tanggalSekarang][str(loop + 1)]["Arah Angin"]}"
                )

                self.console.print(table)

        def updateParams():
            self.parameters = {"adm4": self.wilayah}

        def daftarProvinsi():
            checkPoint = 1
            word = []
            grid = Table.grid(expand=True)
            grid.add_column()

            for itter in self.jsonWilayah.keys():
                if itter == "value":
                    continue

                grid.add_row("", f"{checkPoint}. {itter}")
                word.append(itter)
                checkPoint += 1

            self.console.print("", grid, "")
            provinsiCompleter = WordCompleter(word, ignore_case=True, sentence=True)

            return word, provinsiCompleter

        def daftarKabupatenKota():
            checkPoint = 1
            word = []
            grid = Table.grid(expand=True)
            grid.add_column()

            for itter in self.jsonWilayah[self.provinsi].keys():
                if itter == "value":
                    continue

                grid.add_row("", f"{checkPoint}. {itter}")
                word.append(itter)
                checkPoint += 1

            self.console.print("", grid, "")
            kabupatenKotaCompleter = WordCompleter(
                word, ignore_case=True, sentence=True
            )

            return word, kabupatenKotaCompleter

        def daftarKecamatan():
            checkPoint = 1
            word = []
            grid = Table.grid(expand=True)
            grid.add_column()

            for itter in self.jsonWilayah[self.provinsi][self.kabupatenKota].keys():
                if itter == "value":
                    continue

                grid.add_row("", f"{checkPoint}. {itter}")
                word.append(itter)
                checkPoint += 1

            self.console.print("", grid, "")
            kecamatanCompleter = WordCompleter(word, ignore_case=True, sentence=True)

            return word, kecamatanCompleter

        def daftarKelurahanDesa():
            checkPoint = 1
            word = []
            grid = Table.grid(expand=True)
            grid.add_column()

            for itter in self.jsonWilayah[self.provinsi][self.kabupatenKota][
                self.kecamatan
            ].keys():
                if itter == "value":
                    continue

                grid.add_row("", f"{checkPoint}. {itter}")
                word.append(itter)
                checkPoint += 1

            self.console.print("", grid, "")
            kelurahanDesaCompleter = WordCompleter(
                word, ignore_case=True, sentence=True
            )

            return word, kelurahanDesaCompleter

        def pilihProvinsi(changePrompt=False, startUp=False):
            word, provinsiCompleter = daftarProvinsi()
            number = len(self.jsonWilayah.keys())
            quitLoop = False

            if changePrompt:
                self.promptStr = "ganti-provinsi >>> "

            while True:
                userInput = prompt(
                    self.promptStr,
                    completer=provinsiCompleter,
                    complete_while_typing=True,
                )

                if userInput in self.cmdQuit:
                    if startUp:
                        sys.exit(0)

                    if changePrompt:
                        self.promptStr = ">>> "

                    self.universalExit = True

                    break

                for itter in word:
                    key = itter.lower()

                    if userInput.lower() == key:
                        self.provinsi = itter
                        self.console.print(f"\nAnda memilih provinsi {itter}")

                        if changePrompt:
                            self.promptStr = ">>> "

                        quitLoop = True
                        break

                if quitLoop:
                    break

                userNumber = [num for num in userInput if num.isdigit()]
                if userNumber:
                    userNumber = int("".join(userNumber))

                    if userNumber > 0 and userNumber <= number:
                        self.provinsi = word[userNumber - 1]
                        self.console.print(
                            f"\nAnda memilih provinsi {word[userNumber - 1]}"
                        )

                        if changePrompt:
                            self.promptStr = ">>> "

                        break

                    else:
                        self.console.print(f"Mohon masukan angka antara 1 - {number}")

                else:
                    self.console.print(
                        "Mohon pilih dengan angka atau ketik nama provinsi dengan benar!"
                    )

        def pilihKabupatenKota(changePrompt=False, startUp=False):
            word, kabupatenKotaCompleter = daftarKabupatenKota()
            number = len(self.jsonWilayah[self.provinsi].keys())
            quitLoop = False

            if changePrompt:
                self.promptStr = "ganti-kabupaten/kota >>> "

            while True:
                userInput = prompt(
                    self.promptStr,
                    completer=kabupatenKotaCompleter,
                    complete_while_typing=True,
                )

                if userInput in self.cmdQuit:
                    if startUp:
                        sys.exit(0)

                    if changePrompt:
                        self.promptStr = ">>> "

                    self.universalExit = True

                    break

                for itter in word:
                    key = itter.lower()

                    if userInput.lower() == key:
                        self.kabupatenKota = itter
                        self.console.print(f"\nAnda memilih kabupaten/kota {itter}")

                        if changePrompt:
                            self.promptStr = ">>> "

                        quitLoop = True
                        break

                if quitLoop:
                    break

                userNumber = [num for num in userInput if num.isdigit()]
                if userNumber:
                    userNumber = int("".join(userNumber))

                    if userNumber > 0 and userNumber <= number:
                        self.kabupatenKota = word[userNumber - 1]
                        self.console.print(
                            f"\nAnda memilih kabupaten/kota {word[userNumber - 1]}"
                        )

                        if changePrompt:
                            self.promptStr = ">>> "

                        break

                    else:
                        self.console.print(f"Mohon masukan angka antara 1 - {number}")

                else:
                    self.console.print(
                        "Mohon pilih dengan angka atau ketik nama provinsi dengan benar!"
                    )

        def pilihKecamatan(changePrompt=False, startUp=False):
            word, kecamatanCompleter = daftarKecamatan()
            number = len(self.jsonWilayah[self.provinsi][self.kabupatenKota].keys())
            quitLoop = False

            if changePrompt:
                self.promptStr = "ganti-kecamatan >>> "

            while True:
                userInput = prompt(
                    self.promptStr,
                    completer=kecamatanCompleter,
                    complete_while_typing=True,
                )

                if userInput in self.cmdQuit:
                    if startUp:
                        sys.exit(0)

                    if changePrompt:
                        self.promptStr = ">>> "

                    self.universalExit = True

                    break

                for itter in word:
                    key = itter.lower()

                    if userInput.lower() == key:
                        self.kecamatan = itter
                        self.console.print(f"\nAnda memilih kecamatan {itter}")

                        if changePrompt:
                            self.promptStr = ">>> "

                        quitLoop = True
                        break

                if quitLoop:
                    break

                userNumber = [num for num in userInput if num.isdigit()]
                if userNumber:
                    userNumber = int("".join(userNumber))

                    if userNumber > 0 and userNumber <= number:
                        self.kecamatan = word[userNumber - 1]
                        self.console.print(
                            f"\nAnda memilih kecamatan {word[userNumber - 1]}"
                        )

                        if changePrompt:
                            self.promptStr = ">>> "

                        break

                    else:
                        self.console.print(f"Mohon masukan angka antara 1 - {number}")

                else:
                    self.console.print(
                        "Mohon pilih dengan angka atau ketik nama provinsi dengan benar!"
                    )

        def pilihKelurahanDesa(changePrompt=False, startUp=False):
            word, kelurahanDesaCompleter = daftarKelurahanDesa()
            number = len(word)
            quitLoop = False

            if changePrompt:
                self.promptStr = "ganti-kelurahan/desa >>> "

            while True:
                userInput = prompt(
                    self.promptStr,
                    completer=kelurahanDesaCompleter,
                    complete_while_typing=True,
                )

                if userInput in self.cmdQuit:
                    if startUp:
                        sys.exit(0)

                    if changePrompt:
                        self.promptStr = ">>> "

                    break

                for itter in word:
                    key = itter.lower()

                    if userInput.lower() == key:
                        self.wilayah = self.jsonWilayah[self.provinsi][
                            self.kabupatenKota
                        ][self.kecamatan][itter]["value"]
                        self.kelurahanDesa = itter
                        self.console.print(f"\nAnda memilih kelurahan/desa {itter}")
                        updateParams()
                        self.requestBmkg()
                        self.parserDataHTML()

                        if changePrompt:
                            self.promptStr = ">>> "

                        quitLoop = True
                        break

                if quitLoop:
                    break

                userNumber = [num for num in userInput if num.isdigit()]
                if userNumber:
                    userNumber = int("".join(userNumber))

                    if userNumber > 0 and userNumber <= number:
                        self.wilayah = self.jsonWilayah[self.provinsi][
                            self.kabupatenKota
                        ][self.kecamatan][word[userNumber - 1]]["value"]
                        self.kelurahanDesa = word[userNumber - 1]
                        self.console.print(
                            f"\nAnda memilih kelurahan/desa {word[userNumber - 1]}"
                        )
                        updateParams()
                        self.requestBmkg()
                        self.parserDataHTML()

                        if changePrompt:
                            self.promptStr = ">>> "

                        break

                    else:
                        self.console.print(f"Mohon masukan angka antara 1 - {number}")

                else:
                    self.console.print(
                        "Mohon pilih dengan angka atau ketik nama provinsi dengan benar!"
                    )

        if self.configCuaca:
            with open(self.nameConfig) as file:
                self.jsonDump = ujson.loads(file.read())
                self.provinsi = self.jsonDump["Provinsi"]
                self.kabupatenKota = self.jsonDump["Kabupaten/Kota"]
                self.kecamatan = self.jsonDump["Kecamatan"]
                self.kelurahanDesa = self.jsonDump["Kelurahan/Desa"]
                file.close()

            self.wilayah = self.jsonWilayah[self.provinsi][self.kabupatenKota][
                self.kecamatan
            ][self.kelurahanDesa]["value"]
            updateParams()

            """
                Check apakah cache sudah expired jika sudah
                request data baru, jika cache hilang buat
                cache baru
            """
            expired = cacheTime.isCacheExpired()

            if expired:
                self.requestBmkg()
                self.parserDataHTML()

                """ Buat cache yang expired setiap 10 menit """
                makeCache = cacheTime.makeCacheFile(10)

            else:
                self.parserDataHTML()

        else:
            self.console.rule()
            self.console.print(
                "[bold green]Prakiraan Cuaca BMKG v1.0 by Ayzalme\n", justify="center"
            )
            self.console.print(
                "[green]Silahkan Pilih Provinsi anda...\n", justify="center"
            )
            self.console.rule()
            sleep(1)

            """ Memilih Provinsi """
            pilihProvinsi(startUp=True)

            self.console.rule()
            self.console.print(
                "[green]Silahkan pilih Kabupaten/Kota anda...\n", justify="center"
            )
            self.console.rule()
            time.sleep(1)

            """ Memilih Kabupaten/Kota """
            pilihKabupatenKota(startUp=True)

            self.console.rule()
            self.console.print(
                "[green]Silahkan pilih Kecamatan anda...\n", justify="center"
            )
            self.console.rule()
            time.sleep(1)

            """ Memilih Kelurahan/Desa """
            pilihKecamatan(startUp=True)

            self.console.rule()
            self.console.print(
                "[green]Silahkan pilih Kelurahan/Desa anda...\n", justify="center"
            )
            self.console.rule()
            time.sleep(1)

            """ Memilih Kelurahan/Desa """
            pilihKelurahanDesa(startUp=True)

            """ Simpan config """
            with open(self.nameConfig, "w") as file:
                self.jsonConfig = ujson.dumps(
                    {
                        "Provinsi": self.provinsi,
                        "Kabupaten/Kota": self.kabupatenKota,
                        "Kecamatan": self.kecamatan,
                        "Kelurahan/Desa": self.kelurahanDesa,
                    },
                    indent=4,
                )

                file.write(self.jsonConfig)
                file.close()

        """ Call Table """
        makeTable()

        while True:
            userInput = prompt(self.promptStr)
            self.isCmd = userInput in self.cmd

            if userInput in self.cmdQuit:
                break

            if self.isCmd:
                if userInput == "help":
                    self.console.print("\nList Command yang tersedia :\n")

                    grid = Table.grid(padding=(0, 2), expand=True)
                    grid.add_column()
                    grid.add_row("help", "Untuk menampilkan pesan ini.\n")
                    grid.add_row("exit atau quit", "Untuk keluar dari program.\n")
                    grid.add_row(
                        "version", "Untuk menampilkan versi dan author script ini.\n"
                    )
                    grid.add_row("ganti-provinsi", "Untuk mengganti provinsi.\n")
                    grid.add_row(
                        "ganti-kabupaten/kota", "Untuk mengganti kabupaten/kota.\n"
                    )
                    grid.add_row("ganti-kecamatan", "Untuk mengganti kecamatan.\n")
                    grid.add_row(
                        "ganti-kelurahan/desa", "Untuk mengganti kelurahan/desa.\n"
                    )
                    grid.add_row(
                        "daftar-provinsi", "Untuk menampilkan daftar provinsi.\n"
                    )
                    grid.add_row(
                        "daftar-kabupaten/kota",
                        "Untuk menampilkan daftar kabupaten/kota yang ada di provinsi saat ini.\n",
                    )
                    grid.add_row(
                        "daftar-kecamatan",
                        "Untuk menampilkan daftar kecamatan yang ada di provinsi saat ini.\n",
                    )
                    grid.add_row(
                        "daftar-kelurahan/desa",
                        "Untuk menampilkan daftar kelurahan/desa yang ada di provinsi saat ini.\n",
                    )

                    self.console.print(grid)

                elif userInput == "version":
                    self.console.print("Prakiraan Cuaca BMKG v1.0 by Ayzalme")

                elif userInput == "ganti-provinsi":
                    self.console.print("\nSilahkan pilih provinsi yang anda inginkan :")
                    pilihProvinsi(changePrompt=True)

                    if self.universalExit:
                        self.universalExit = False
                        makeTable()
                        continue

                    self.console.print(
                        "\nSilahkan pilih kabupaten/kota yang anda inginkan :"
                    )
                    pilihKabupatenKota(changePrompt=True)
                    self.console.print(
                        "\nSilahkan pilih kecamatan yang anda inginkan :"
                    )
                    pilihKecamatan(changePrompt=True)
                    self.console.print(
                        "\nSilahkan pilih kelurahan/desa yang anda inginkan :"
                    )
                    pilihKelurahanDesa(changePrompt=True)
                    makeTable()

                elif userInput == "ganti-kabupaten/kota":
                    self.console.print(
                        "\nSilahkan pilih kabupaten/kota yang anda inginkan :"
                    )
                    pilihKabupatenKota(changePrompt=True)

                    if self.universalExit:
                        self.universalExit = False
                        makeTable()
                        continue

                    self.console.print(
                        "\nSilahkan pilih kecamatan yang anda inginkan :"
                    )
                    pilihKecamatan(changePrompt=True)
                    self.console.print(
                        "\nSilahkan pilih kelurahan/desa yang anda inginkan :"
                    )
                    pilihKelurahanDesa(changePrompt=True)
                    self.universalExit = False
                    makeTable()

                elif userInput == "ganti-kecamatan":
                    self.console.print(
                        "\nSilahkan pilih kecamatan yang anda inginkan :"
                    )
                    pilihKecamatan(changePrompt=True)

                    if self.universalExit:
                        self.universalExit = False
                        makeTable()
                        continue

                    self.console.print(
                        "\nSilahkan pilih kelurahan/desa yang anda inginkan :"
                    )
                    pilihKelurahanDesa(changePrompt=True)
                    self.universalExit = False
                    makeTable()

                elif userInput == "ganti-kelurahan/desa":
                    self.console.print(
                        "\nSilahkan pilih kelurahan/desa yang anda inginkan :"
                    )
                    pilihKelurahanDesa(changePrompt=True)
                    makeTable()

                elif userInput == "daftar-provinsi":
                    self.console.print("\nDaftar provinsi :")
                    daftarProvinsi()

                elif userInput == "daftar-kabupaten/kota":
                    self.console.print(
                        "\nDaftar kabupaten/kota yang tersedia di provinsi ini :"
                    )
                    daftarKabupatenKota()

                elif userInput == "daftar-kecamatan":
                    self.console.print(
                        "\nDaftar kecamatan yang tersedia di provinsi ini :"
                    )
                    daftarKecamatan()

                elif userInput == "daftar-kelurahan/desa":
                    self.console.print(
                        "\nDaftar kelurahan/desa yang tersedia di provinsi ini :"
                    )
                    daftarKelurahanDesa()

            else:
                self.console.print(
                    f"'{userInput}' Command tidak tersedia, ketik 'help' untuk menampilkan command yang tersedia"
                )


""" Lets The Show Begins! """
objectStartUp = getBmkgWebsite()
objectStartUp.showingResult()
