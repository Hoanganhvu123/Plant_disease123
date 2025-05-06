import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm
import os

# Đọc file CSV gốc - sửa đường dẫn để đọc file từ thư mục hiện tại
df = pd.read_csv("disease_info.csv")

# Hiển thị tiến độ dịch
tqdm.pandas()

# Hàm dịch an toàn
def safe_translate(text):
    try:
        return GoogleTranslator(source='auto', target='vi').translate(str(text))
    except:
        return text

# Dịch nội dung các cột sang tiếng Việt (KHÔNG đổi tên cột)
columns_to_translate = ['disease_name', 'description', 'Possible Steps']

for col in columns_to_translate:
    df[col] = df[col].progress_apply(safe_translate)

# Lưu file mới, giữ nguyên tên cột
df.to_csv("disease_infor_vi.csv", index=False, encoding='utf-8')

print("✅ Đã dịch toàn bộ nội dung và giữ nguyên tiêu đề cột. File mới: disease_infor_vi.csv")
