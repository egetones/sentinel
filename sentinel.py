import os
import hashlib
import time
import sys

# Renkler
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def calculate_file_hash(filepath):
    """Bir dosyanın SHA-256 özetini (hash) hesaplar."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Dosyayı parça parça oku (RAM'i şişirmemek için)
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (IOError, OSError):
        return None

def create_baseline(target_dir, baseline_file):
    """Hedef dizindeki dosyaların hash'lerini kaydeder."""
    print(f"{BLUE}[*] Baseline (Referans) oluşturuluyor...{RESET}")
    
    if os.path.exists(baseline_file):
        os.remove(baseline_file)

    count = 0
    with open(baseline_file, "w") as f:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    # Format: DosyaYolu|Hash
                    f.write(f"{filepath}|{file_hash}\n")
                    count += 1
    
    print(f"{GREEN}[+] Başarılı! {count} dosya veritabanına işlendi: {baseline_file}{RESET}")

def monitor_integrity(target_dir, baseline_file):
    """Mevcut durumu baseline ile karşılaştırır ve değişiklikleri raporlar."""
    print(f"{YELLOW}[*] İzleme Modu Başlatıldı... (Durdurmak için CTRL+C){RESET}")
    print("-" * 50)

    # Baseline'ı belleğe (Dictionary) yükle
    baseline_dict = {}
    try:
        with open(baseline_file, "r") as f:
            for line in f:
                path, original_hash = line.strip().split("|")
                baseline_dict[path] = original_hash
    except FileNotFoundError:
        print(f"{RED}[!] Hata: Baseline dosyası bulunamadı. Önce 'A' seçeneği ile oluşturun.{RESET}")
        return

    while True:
        time.sleep(1) # Sistemi yormamak için 1 saniye bekle
        
        # Anlık dosyaları tara
        current_files = {}
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    current_files[filepath] = file_hash

        # 1. KONTROL: Dosya Değiştirildi mi veya Yeni mi Eklendi?
        for path, current_hash in current_files.items():
            if path not in baseline_dict:
                print(f"{GREEN}[+] YENİ DOSYA OLUŞTURULDU: {path}{RESET}")
                # Alarmı tekrar etmemek için listeye ekle (Opsiyonel)
                baseline_dict[path] = current_hash 
            else:
                if baseline_dict[path] != current_hash:
                    print(f"{RED}[!] UYARI: DOSYA DEĞİŞTİRİLDİ! -> {path}{RESET}")
                    baseline_dict[path] = current_hash

        # 2. KONTROL: Dosya Silindi mi?
        # Sözlüğü kopyalayarak dönüyoruz ki silme işlemi hata vermesin
        for path in list(baseline_dict.keys()):
            if path not in current_files:
                print(f"{RED}[-] KRİTİK: DOSYA SİLİNDİ! -> {path}{RESET}")
                del baseline_dict[path]

def main():
    print(f"""{BLUE}
   _____            _   _            _ 
  / ____|          | | (_)          | |
 | (___   ___ _ __ | |_ _ _ __   ___| |
  \___ \ / _ \ '_ \| __| | '_ \ / _ \ |
  ____) |  __/ | | | |_| | | | |  __/ |
 |_____/ \___|_| |_|\__|_|_| |_|\___|_|
  File Integrity Monitor (FIM) v1.0
    {RESET}""")

    target_dir = input("Hedef Klasör Yolu (Örn: ./test_folder): ").strip()
    baseline_file = "baseline.txt"

    if not os.path.isdir(target_dir):
        print(f"{RED}[!] Geçersiz klasör yolu.{RESET}")
        return

    print("\n1) Yeni Baseline Oluştur (Veritabanını Sıfırla)")
    print("2) İzlemeyi Başlat (Monitor)")
    choice = input("\nSeçiminiz (1/2): ")

    if choice == "1":
        create_baseline(target_dir, baseline_file)
    elif choice == "2":
        monitor_integrity(target_dir, baseline_file)
    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    main()
