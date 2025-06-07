import matplotlib.pyplot as plt
import math

# Daftar kota
kota_list = [
    "Jakarta", "Bandung", "Surabaya", "Medan", "Makassar",
    "Semarang", "Palembang", "Yogyakarta", "Banjarmasin", "Denpasar"
]

# Susun posisi kota melingkar agar rapi
angle_step = 2 * math.pi / len(kota_list)
positions = {
    kota: (math.cos(i * angle_step), math.sin(i * angle_step))
    for i, kota in enumerate(kota_list)
}

# Daftar jalur antar kota dengan jarak tempuh (km)
jalur = [
    ("Jakarta", "Bandung", 10), ("Jakarta", "Semarang", 20), ("Jakarta", "Yogyakarta", 25),
    ("Jakarta", "Palembang", 35), ("Jakarta", "Medan", 50), ("Bandung", "Yogyakarta", 22),
    ("Bandung", "Semarang", 18), ("Semarang", "Surabaya", 22), ("Semarang", "Yogyakarta", 15),
    ("Surabaya", "Denpasar", 20), ("Surabaya", "Makassar", 45), ("Medan", "Palembang", 40),
    ("Palembang", "Banjarmasin", 42), ("Banjarmasin", "Makassar", 38), ("Makassar", "Denpasar", 50),
    ("Makassar", "Yogyakarta", 45), ("Banjarmasin", "Surabaya", 39), ("Denpasar", "Yogyakarta", 30),
    ("Denpasar", "Semarang", 28), ("Palembang", "Yogyakarta", 27), ("Bandung", "Palembang", 32),
    ("Bandung", "Denpasar", 36), ("Jakarta", "Makassar", 55), ("Surabaya", "Palembang", 40),
    ("Medan", "Makassar", 60), ("Medan", "Denpasar", 65), ("Medan", "Bandung", 45),
    ("Banjarmasin", "Yogyakarta", 31), ("Bandung", "Banjarmasin", 43), ("Jakarta", "Banjarmasin", 46)
]

# Gambar graph
plt.figure(figsize=(12, 12))

# Gambar titik (kota)
for kota, (x, y) in positions.items():
    plt.scatter(x, y, s=1000, color='skyblue', edgecolors='black', zorder=2)
    plt.text(x, y, kota, fontsize=10, fontweight='bold', ha='center', va='center', zorder=3)

# Gambar garis (jalur) dan jarak
for u, v, jarak in jalur:
    x1, y1 = positions[u]
    x2, y2 = positions[v]
    plt.plot([x1, x2], [y1, y2], color='gray', linewidth=1.5, zorder=1)
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    plt.text(mid_x, mid_y, str(jarak), fontsize=8, color='red', zorder=3)

plt.axis('off')
plt.title("Graph Kota Indonesia dengan Jarak Tempuh (KM)", fontsize=14)
plt.tight_layout()
plt.show()



import heapq
import itertools

# ===== Struktur Graph Multimoda =====
class MultiModeGraph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def tambah_kota(self, nama):
        self.vertices.add(nama)
        self.edges[nama] = []

    def tambah_jalan(self, dari, ke, waktu_mobil, waktu_motor, waktu_jalan,
                     jarak_mobil, jarak_motor, jarak_jalan):
        bobot = {
            "mobil": {"waktu": waktu_mobil, "jarak": jarak_mobil},
            "motor": {"waktu": waktu_motor, "jarak": jarak_motor},
            "jalan": {"waktu": waktu_jalan, "jarak": jarak_jalan}
        }
        self.edges[dari].append((ke, bobot))
        self.edges[ke].append((dari, bobot))

    def dijkstra(self, awal, tujuan, moda):
        antrian = [(0, 0, awal, [])]  # (total_waktu, total_jarak, kota, jalur)
        sudah_dikunjungi = set()

        while antrian:
            waktu, jarak, kota, jalur = heapq.heappop(antrian)
            if kota in sudah_dikunjungi:
                continue
            sudah_dikunjungi.add(kota)
            jalur = jalur + [kota]

            if kota == tujuan:
                return waktu, jarak, jalur

            for tetangga, bobot in self.edges[kota]:
                if tetangga not in sudah_dikunjungi:
                    waktu_tambah = bobot[moda]["waktu"]
                    jarak_tambah = bobot[moda]["jarak"]
                    heapq.heappush(antrian, (waktu + waktu_tambah, jarak + jarak_tambah, tetangga, jalur))

        return float('inf'), float('inf'), []

    def tsp_brute_force(self, moda):
        kota_list = list(self.vertices)
        min_waktu = float('inf')
        min_jarak = float('inf')
        rute_terbaik = None

        for urutan in itertools.permutations(kota_list):
            total_waktu = 0
            total_jarak = 0
            valid = True
            for i in range(len(urutan) - 1):
                tetangga_dict = {n: w for n, w in self.edges[urutan[i]]}
                if urutan[i + 1] in tetangga_dict:
                    total_waktu += tetangga_dict[urutan[i + 1]][moda]["waktu"]
                    total_jarak += tetangga_dict[urutan[i + 1]][moda]["jarak"]
                else:
                    valid = False
                    break
            if valid and total_waktu < min_waktu:
                min_waktu = total_waktu
                min_jarak = total_jarak
                rute_terbaik = urutan

        return min_waktu, min_jarak, rute_terbaik

# ===== Graf Kota & Jarak =====
def graf_kota():
    kota_list = [
        "Jakarta", "Bandung", "Surabaya", "Medan", "Makassar",
        "Semarang", "Palembang", "Yogyakarta", "Banjarmasin", "Denpasar"
    ]
    graf = MultiModeGraph()
    for kota in kota_list:
        graf.tambah_kota(kota)

    # Format: (dari, ke, waktu_mobil, waktu_motor, waktu_jalan, jarak_mobil, jarak_motor, jarak_jalan)
    jalur = [
        ("Jakarta", "Bandung", 2.5, 3.0, 10, 150, 140, 120),
        ("Jakarta", "Semarang", 5.0, 6.0, 20, 450, 420, 400),
        ("Jakarta", "Yogyakarta", 7.0, 8.0, 25, 560, 530, 510),
        ("Jakarta", "Palembang", 10.0, 12.0, 35, 780, 750, 700),
        ("Jakarta", "Medan", 18.0, 20.0, 50, 1420, 1380, 1300),
        ("Bandung", "Yogyakarta", 5.5, 6.5, 22, 400, 380, 350),
        ("Bandung", "Semarang", 4.0, 5.0, 18, 340, 320, 300),
        ("Semarang", "Surabaya", 5.0, 6.0, 22, 350, 340, 320),
        ("Semarang", "Yogyakarta", 3.0, 4.0, 15, 140, 130, 120),
        ("Surabaya", "Denpasar", 5.0, 6.5, 20, 410, 400, 380),
        ("Surabaya", "Makassar", 17.0, 19.0, 45, 1350, 1300, 1250),
        ("Medan", "Palembang", 14.0, 16.0, 40, 1200, 1150, 1100),
        ("Palembang", "Banjarmasin", 15.0, 17.0, 42, 1000, 950, 920),
        ("Banjarmasin", "Makassar", 13.0, 15.0, 38, 950, 900, 880),
        ("Makassar", "Denpasar", 20.0, 22.0, 50, 1100, 1050, 1000),
        ("Makassar", "Yogyakarta", 18.0, 20.0, 45, 980, 940, 900),
        ("Banjarmasin", "Surabaya", 14.0, 16.0, 39, 1050, 1000, 950),
        ("Denpasar", "Yogyakarta", 10.0, 12.0, 30, 650, 620, 600),
        ("Denpasar", "Semarang", 9.0, 11.0, 28, 610, 580, 560),
        ("Palembang", "Yogyakarta", 9.0, 11.0, 27, 570, 540, 500),
        ("Bandung", "Palembang", 10.0, 11.5, 32, 670, 640, 600),
        ("Bandung", "Denpasar", 12.0, 14.0, 36, 750, 720, 680),
        ("Jakarta", "Makassar", 22.0, 24.0, 55, 1600, 1550, 1500),
        ("Surabaya", "Palembang", 13.0, 15.0, 40, 980, 950, 920),
        ("Medan", "Makassar", 23.0, 25.0, 60, 1700, 1650, 1600),
        ("Medan", "Denpasar", 24.0, 26.0, 65, 1750, 1700, 1650),
        ("Medan", "Bandung", 15.0, 17.0, 45, 1250, 1200, 1150),
        ("Banjarmasin", "Yogyakarta", 11.0, 13.0, 31, 670, 640, 600),
        ("Bandung", "Banjarmasin", 16.0, 18.0, 43, 980, 940, 900),
        ("Jakarta", "Banjarmasin", 17.0, 19.0, 46, 1020, 980, 950)
    ]

    for data in jalur:
        graf.tambah_jalan(*data)

    return graf, kota_list

# ===== Program Utama =====
def main():
    graf, kota_list = graf_kota()

    print("=== RUTE TERCEPAT MENGGUNAKAN DIJKSTRA ===")
    print("Daftar kota:", ', '.join(kota_list))

    moda = input("Pilih transportasi (mobil/motor/jalan): ").strip().lower()
    asal = input("Masukkan kota asal anda: ").strip().title()
    tujuan = input("Masukkan kota tujuan anda: ").strip().title()

    if asal not in kota_list or tujuan not in kota_list:
        print("❌ Nama kota tidak valid.")
        return

    if moda not in ["mobil", "motor", "jalan"]:
        print("❌ Moda transportasi tidak tersedia.")
        return

    waktu, jarak, jalur = graf.dijkstra(asal, tujuan, moda)
    if jalur:
        print(f"\n✅ Rute tercepat dari {asal} ke {tujuan} dengan {moda}:")
        print(" -> ".join(jalur))
        print(f"Total waktu: {waktu:.2f} jam")
        print(f"Total jarak tempuh: {jarak:.2f} km\n")
    else:
        print("❌ Tidak ditemukan rute yang valid.\n")

    print("=== RUTE TSP TERBAIK (Semua kota dikunjungi sekali) ===")
    waktu_tsp, jarak_tsp, rute_tsp = graf.tsp_brute_force(moda)
    if rute_tsp:
        print(f"📍 Rute TSP: {' -> '.join(rute_tsp)}")
        print(f"Total waktu: {waktu_tsp:.2f} jam")
        print(f"Total jarak tempuh: {jarak_tsp:.2f} km\n")
    else:
        print("❌ Tidak ditemukan rute TSP yang valid.\n")

if __name__ == "__main__":
    main()


