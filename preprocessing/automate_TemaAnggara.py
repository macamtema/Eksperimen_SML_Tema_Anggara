import os
import shutil
import random
import argparse
from tqdm import tqdm
from pathlib import Path

def split_dataset(source_dir, target_dir, split_ratios=(0.7, 0.15, 0.15)):
    """
    Membagi dataset gambar dari source_dir ke target_dir menjadi folder
    train, val, dan test berdasarkan rasio yang diberikan.

    Struktur yang diharapkan di source_dir:
    - source_dir/
      - class_A/
        - img1.jpg
        - img2.jpg
      - class_B/
        - img3.jpg
        - img4.jpg
    
    Struktur yang akan dihasilkan di target_dir:
    - target_dir/
      - train/
        - class_A/
        - class_B/
      - val/
        - class_A/
        - class_B/
      - test/
        - class_A/
        - class_B/
    """
    
    # Pastikan total rasio adalah 1.0
    assert sum(split_ratios) == 1.0, "Total rasio pembagian (train, val, test) harus 1.0"
    
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # Buat folder tujuan (train, val, test) jika belum ada
    for split in ['train', 'val', 'test']:
        (target_path / split).mkdir(parents=True, exist_ok=True)

    print(f"Memproses dataset dari: {source_path}")
    print(f"Menyimpan hasil ke: {target_path}")

    # Iterasi melalui setiap folder kelas di direktori sumber
    class_dirs = [d for d in source_path.iterdir() if d.is_dir()]
    if not class_dirs:
        print(f"Peringatan: Tidak ada sub-direktori (kelas) yang ditemukan di '{source_path}'. Pastikan struktur folder sudah benar.")
        return

    for class_dir in tqdm(class_dirs, desc="Memproses semua kelas"):
        class_name = class_dir.name
        images = list(class_dir.glob('*.*')) # Mengambil semua file gambar
        random.shuffle(images)

        total_images = len(images)
        train_end = int(split_ratios[0] * total_images)
        val_end = train_end + int(split_ratios[1] * total_images)

        # Definisikan file untuk setiap split
        splits_files = {
            'train': images[:train_end],
            'val': images[train_end:val_end],
            'test': images[val_end:]
        }

        # Salin file ke direktori tujuan yang sesuai
        for split_name, files in splits_files.items():
            split_class_dir = target_path / split_name / class_name
            split_class_dir.mkdir(parents=True, exist_ok=True)
            
            for file_path in files:
                shutil.copy2(file_path, split_class_dir / file_path.name)
    
    print("\nProses pemisahan dataset selesai.")
    print(f"Hasil tersimpan di folder '{target_path}'.")


if __name__ == '__main__':
    # Menggunakan argparse untuk fleksibilitas, tapi kita set default sesuai struktur Anda
    parser = argparse.ArgumentParser(description="Split image dataset into train, val, and test sets.")
    # Path relatif dari root folder proyek
    parser.add_argument('--source', type=str, default='Rice_Image_Dataset', help='Direktori sumber dataset.')
    parser.add_argument('--target', type=str, default='preprocessing/data_split', help='Direktori tujuan untuk menyimpan hasil split.')
    args = parser.parse_args()

    split_dataset(args.source, args.target)