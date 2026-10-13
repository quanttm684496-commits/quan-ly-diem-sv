import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình trang web
st.set_page_config(page_title="QUẢN LÝ ĐIỂM SINH VIÊN", layout="wide")

# 1. Tạo DataFrame
data = {
    'Ho_ten': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyen_can': [9.0, 8.5, 7.0, 9.5, 8.0, 6.0, 9.0, 7.5, 8.0, 10.0],
    'Giua_ky': [8.0, 8.0, 6.5, 9.0, 7.0, 5.5, 8.5, 7.0, 7.5, 9.0],
    'Cuoi_ky': [7.5, 8.5, 6.5, 9.0, 7.5, 6.0, 8.0, 6.5, 7.0, 9.0]
}
df = pd.DataFrame(data)

# 2. Tính điểm tổng kết (20% CC, 30% GK, 50% CK)
df['Tong_ket'] = (0.2 * df['Chuyen_can'] + 0.3 * df['Giua_ky'] + 0.5 * df['Cuoi_ky']).round(2)

# 3. Xếp loại
def xep_loai(diem):
    if diem >= 8.5: return 'Giỏi'
    elif diem >= 7.0: return 'Khá'
    elif diem >= 5.0: return 'Trung bình'
    else: return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# === GIAO DIỆN STREAMLIT ===
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm
st.subheader("📋 Bảng điểm của 10 sinh viên")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# Thống kê
st.subheader("📊 Thống kê chung")
dtb_lop = df['Tong_ket'].mean()
sv_max = df.loc[df['Tong_ket'].idxmax()]
sv_min = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Điểm TB lớp", f"{dtb_lop:.2f}")
col2.metric("Điểm cao nhất", f"{sv_max['Ho_ten']} ({sv_max['Tong_ket']})")
col3.metric("Điểm thấp nhất", f"{sv_min['Ho_ten']} ({sv_min['Tong_ket']})")
col4.metric("Số SV đạt (>=5)", f"{so_sv_dat}/{len(df)}")

st.markdown("---")

# Selectbox chọn sinh viên
st.subheader("🔍 Chi tiết từng sinh viên")
selected_student = st.selectbox("Chọn sinh viên để xem chi tiết:", df['Ho_ten'])
sv_info = df[df['Ho_ten'] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.write(f"**Chuyên cần:** {sv_info['Chuyen_can']}")
c2.write(f"**Giữa kỳ:** {sv_info['Giua_ky']}")
c3.write(f"**Cuối kỳ:** {sv_info['Cuoi_ky']}")
c4.write(f"**Tổng kết:** {sv_info['Tong_ket']}")
c5.write(f"**Xếp loại:** {sv_info['Xep_loai']}")

st.markdown("---")

# Biểu đồ cột
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(df['Ho_ten'], df['Tong_ket'], color='#1f77b4')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval}', ha='center', va='bottom')
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle='--', alpha=0.6)
st.pyplot(fig)

# Thông tin sinh viên tạo app (Bạn sửa lại Họ tên & MSSV của bạn ở đây)
st.markdown("---")
st.caption("👨‍🎓 **Họ và tên:** Tôn Thất Minh Quân | **MSSV:** 068208004496")
