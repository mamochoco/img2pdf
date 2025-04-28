import os
from PIL import Image, ImageSequence

LOG_FILE = "conversion_log.txt"

def convert_images_to_pdfs(folder_path):
    image_extensions = (".tif", ".jpeg", ".jpg", ".png")
    converted_files = []

    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write(f"変換対象フォルダ: {folder_path}\n\n")

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_path = os.path.join(root, file)
                    pdf_path = os.path.splitext(image_path)[0] + ".pdf"

                    # TIFFの場合は各ページを処理
                    img = Image.open(image_path)
                    if image_path.lower().endswith(".tif"):
                        images = []
                        for page in ImageSequence.Iterator(img):
                            page = page.convert("RGB")  # RGBに変換
                            images.append(page)
                        # 複数ページを一つのPDFに保存
                        images[0].save(pdf_path, save_all=True, append_images=images[1:])
                    else:
                        img = img.convert("RGB")
                        img.save(pdf_path, "PDF")
                    
                    converted_files.append(pdf_path)
                    log.write(f"PDF作成: {pdf_path}\n")

        log.write(f"\n合計変換ファイル数: {len(converted_files)}\n")
        print(f"変換されたファイルのログを '{LOG_FILE}' に保存しました。")

# 使用例
convert_images_to_pdfs("指定フォルダのパス")