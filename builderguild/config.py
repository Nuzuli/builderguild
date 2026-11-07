from .graph import FactGraph

def main():
    print("Builderguild CLI siap!")
    fg = FactGraph()
    fg.add("Inisialisasi", "Setup awal graph berhasil", {"path": "cli.py"})
    print("Fakta awal berhasil dimasukkan ke graph.")

if __name__ == "__main__":
    main()
