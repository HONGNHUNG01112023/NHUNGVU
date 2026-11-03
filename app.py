import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import random

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN & MÀU XANH NGỌC LỤC BẢO ĐẬM
# ==========================================
st.set_page_config(page_title="Dispute Hub - Professional", layout="wide", page_icon="🛡️")

EMERALD_CSS = """
<style>
    /* Màu nền chính ứng dụng */
    .stApp {
        background-color: #F4F8F7;
    }
    
    /* Tùy chỉnh Sidebar: Xanh ngọc lục bảo thanh lịch */
    section[data-testid="stSidebar"] {
        background-color: #E2ECE8;
        border-right: 2px solid #B8D4CC;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] span {
        color: #04211C !important;
    }

    /* Căn lề trái thẳng hàng tuyệt đối cho tất cả các nút trong Sidebar */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 14px !important;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* 1. Nút đang được chọn (Active - Primary): Xanh ngọc lục bảo ĐẬM SÂU, chữ trắng nổi bật */
    div.stSidebar div.stButton > button[kind="primary"] {
        background-color: #022B21 !important;
        color: #FFFFFF !important;
        border: 1px solid #011712 !important;
        font-weight: 700 !important;
        border-radius: 6px;
        text-align: left !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    div.stSidebar div.stButton > button[kind="primary"]:hover {
        background-color: #011E17 !important;
    }

    /* 2. Nút bình thường (Secondary): Nền trắng sạch sẽ, chữ xanh đậm */
    div.stSidebar div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #06382F !important;
        border: 1px solid #A4C7BE !important;
        font-weight: 500 !important;
        border-radius: 6px;
        text-align: left !important;
    }
    div.stSidebar div.stButton > button[kind="secondary"]:hover {
        background-color: #C8E3DC !important;
        border-color: #064035 !important;
        color: #022620 !important;
    }

    /* Tiêu đề chính ứng dụng */
    h1, h2, h3 {
        color: #042E26 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Nút bấm chính (Primary Button) bên trong nội dung trang */
    div.stMain div.stButton > button[kind="primary"] {
        background-color: #043D32 !important;
        color: white !important;
        border-radius: 6px;
        border: none;
        font-weight: 600;
    }
    div.stMain div.stButton > button[kind="primary"]:hover {
        background-color: #022B21 !important;
    }

    /* Các khối metric thống kê */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-left: 5px solid #043D32;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetric"] label {
        color: #555555 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #042E26 !important;
        font-weight: 700;
    }
    
    /* Khung Expander (Chức năng lớn) tinh tế */
    .streamlit-expanderHeader {
        background-color: #B9DCD2 !important;
        color: #04211C !important;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
"""
st.markdown(EMERALD_CSS, unsafe_allow_html=True)

st.title("🛡️ Dispute Hub - Quản lý & Tra soát Giao dịch")

# ==========================================
# 2. KHỞI TẠO 50 GIAO DỊCH MẪU (CHUẨN 12 TRƯỜNG)
# ==========================================
if 'disputes_db' not in st.session_state:
    keys = [
        "Mã tra soát", "Trạng thái tra soát", "Trạng thái hạch toán", "CIF", 
        "Tên chủ thẻ", "Ngày giao dịch", "Số thẻ", "RRN", "Loại giao dịch", 
        "Số tiền giao dịch", "Số chuẩn chi", "Mã thiết bị"
    ]
    
    names = ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D", "Hoàng Văn E", "Vũ Thị F", "Đỗ Văn G", "Bùi Thị H"]
    types = ["ATM", "POS"]
    statuses = ["Chờ xử lý", "Chờ phê duyệt", "Đang xử lý", "Từ chối xử lý", "Hoàn thành"]
    accounting_statuses = ["Chờ duyệt hạch toán", "Hạch toán thành công", "Hạch toán thất bại"]
    
    raw_data = []
    base_date = datetime(2026, 6, 1)
    
    for i in range(1, 51):
        tx_id = f"TS-2026-{i:03d}"
        cif = f"100{i:03d}"
        name = names[(i - 1) % len(names)]
        d_str = (base_date + timedelta(days=(i % 15))).strftime("%d/%m/%Y")
        card = f"4000-xxxx-xxxx-{1000 + i}"
        rrn = f"{123456780000 + i}"
        tx_type = types[i % len(types)]
        
        amount_val = ((i * 350000) % 4800000) + 200000
        amount = f"{amount_val:,.0f} VND".replace(",", ".")
        
        cc = f"CC-{900000 + i}"
        device = f"ATM_HN_{i % 5 + 1:02d}"
        status = statuses[i % len(statuses)]
        acc_status = accounting_statuses[i % len(accounting_statuses)]
        
        raw_data.append((tx_id, status, acc_status, cif, name, d_str, card, rrn, tx_type, amount, cc, device))
        
    st.session_state.disputes_db = [dict(zip(keys, row)) for row in raw_data]

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Tạo tra soát đơn lẻ"

current_page = st.session_state.current_page

# Phân nhóm danh mục sidebar
group_tao = ["Tạo tra soát đơn lẻ", "Tạo tra soát theo lô"]
group_xu_ly = ["Tất cả hồ sơ", "Hồ sơ của tôi", "Sắp đến hạn"]
group_van_tin = ["Vấn tin tra soát", "Quản lý chứng từ"]
group_bao_cao = ["Báo cáo thống kê TSKN", "Xuất file báo cáo"]

# ==========================================
# 3. CỘT CHỨC NĂNG BÊN TRÁI (SIDEBAR)
# ==========================================
st.sidebar.title("📌 Danh mục chức năng")

with st.sidebar.expander("📝 Tạo tra soát", expanded=(current_page in group_tao)):
    if st.button("• Tạo tra soát đơn lẻ", type="primary" if current_page == "Tạo tra soát đơn lẻ" else "secondary", use_container_width=True, key="btn_don_le"):
        st.session_state.current_page = "Tạo tra soát đơn lẻ"
        st.rerun()
    if st.button("• Tạo tra soát theo lô (Batch)", type="primary" if current_page == "Tạo tra soát theo lô" else "secondary", use_container_width=True, key="btn_batch"):
        st.session_state.current_page = "Tạo tra soát theo lô"
        st.rerun()

with st.sidebar.expander("⏳ Tra soát chờ xử lý", expanded=(current_page in group_xu_ly)):
    if st.button("• Tất cả hồ sơ", type="primary" if current_page == "Tất cả hồ sơ" else "secondary", use_container_width=True, key="btn_tat_ca"):
        st.session_state.current_page = "Tất cả hồ sơ"
        st.rerun()
    if st.button("• Hồ sơ của tôi (Maker)", type="primary" if current_page == "Hồ sơ của tôi" else "secondary", use_container_width=True, key="btn_maker"):
        st.session_state.current_page = "Hồ sơ của tôi"
        st.rerun()
    if st.button("• Sắp đến hạn", type="primary" if current_page == "Sắp đến hạn" else "secondary", use_container_width=True, key="btn_sla"):
        st.session_state.current_page = "Sắp đến hạn"
        st.rerun()

with st.sidebar.expander("🔍 Vấn tin tra soát", expanded=(current_page in group_van_tin)):
    if st.button("• Vấn tin tra soát", type="primary" if current_page == "Vấn tin tra soát" else "secondary", use_container_width=True, key="btn_vun_tin"):
        st.session_state.current_page = "Vấn tin tra soát"
        st.rerun()
    if st.button("• Quản lý chứng từ", type="primary" if current_page == "Quản lý chứng từ" else "secondary", use_container_width=True, key="btn_chung_tu"):
        st.session_state.current_page = "Quản lý chứng từ"
        st.rerun()

with st.sidebar.expander("📊 Báo cáo", expanded=(current_page in group_bao_cao)):
    if st.button("• Báo cáo thống kê TSKN", type="primary" if current_page == "Báo cáo thống kê TSKN" else "secondary", use_container_width=True, key="btn_bc"):
        st.session_state.current_page = "Báo cáo thống kê TSKN"
        st.rerun()
    if st.button("• Xuất file Excel/PDF", type="primary" if current_page == "Xuất file báo cáo" else "secondary", use_container_width=True, key="btn_xuat"):
        st.session_state.current_page = "Xuất file báo cáo"
        st.rerun()

# ==========================================
# 4. HIỂN THỊ NỘI DUNG CHÍNH TƯƠNG ỨNG
# ==========================================
if current_page == "Tạo tra soát đơn lẻ":
    st.header("📝 Tạo tra soát đơn lẻ")
    
    with st.form("form_don_le"):
        col1, col2, col3 = st.columns(3)
        with col1:
            doi_tuong = st.selectbox("Đối tượng tra soát", ["Chủ thẻ", "ĐVCNT", "MGDTĐ"])
        with col2:
            tu_ngay = st.date_input("Từ ngày", value=date.today(), format="DD/MM/YYYY")
        with col3:
            den_ngay = st.date_input("Đến ngày", value=date.today(), format="DD/MM/YYYY")
            
        cif_input = st.text_input("Mã CIF khách hàng", placeholder="Nhập CIF...")
        
        with st.expander("🔍 Bộ lọc tìm kiếm nâng cao (Số tiền, RRN, Số thẻ...)"):
            col_adv1, col_adv2, col_adv3 = st.columns(3)
            with col_adv1:
                adv_card = st.text_input("Số thẻ (4 số cuối hoặc đầy đủ)")
            with col_adv2:
                adv_rrn = st.text_input("Mã RRN / Số chuẩn chi")
            with col_adv3:
                adv_min_amount = st.number_input("Số tiền tối thiểu (VND)", min_value=0, value=0, step=100000)

        submitted = st.form_submit_button("🔎 Tìm kiếm giao dịch")
        
    if submitted or 'df_search' in st.session_state:
        if 'df_search' not in st.session_state:
            st.session_state.df_search = pd.DataFrame([
                {
                    "Chọn": False,
                    "Mã giao dịch": item["Mã tra soát"].replace("TS", "TX"),
                    "Ngày giao dịch": item["Ngày giao dịch"],
                    "Số thẻ": item["Số thẻ"],
                    "RRN": item["RRN"],
                    "Số tiền giao dịch": item["Số tiền giao dịch"],
                    "Số chuẩn chi": item["Số chuẩn chi"],
                    "Mã thiết bị": item["Mã thiết bị"]
                } for item in st.session_state.disputes_db[:10]
            ])
            
        edited_df = st.data_editor(
            st.session_state.df_search, 
            use_container_width=True, 
            hide_index=True,
            column_config={"Chọn": st.column_config.CheckboxColumn("☑️ Chọn", default=False)}
        )
        
        selected_row = edited_df[edited_df["Chọn"] == True]
        
        if len(selected_row) == 1:
            st.success(f"Đã chọn giao dịch mã: **{selected_row.iloc[0]['Mã giao dịch']}**")
            
            loai_giao_dich = st.selectbox("Loại giao dịch tra soát", ["ATM", "POS"])
            uploaded_files = st.file_uploader("📎 Đính kèm chứng từ (YCTS, biên lai...)", accept_multiple_files=True)
            
            if st.button("🚀 Gửi Tra soát", type="primary"):
                new_id = f"TS-2026-00{len(st.session_state.disputes_db) + 1}"
                
                st.session_state.disputes_db.append({
                    "Mã tra soát": new_id,
                    "Trạng thái tra soát": "Chờ phê duyệt",
                    "Trạng thái hạch toán": "Chưa hạch toán",
                    "CIF": cif_input if cif_input else "100999",
                    "Tên chủ thẻ": "Nguyễn Văn Test",
                    "Ngày giao dịch": selected_row.iloc[0]["Ngày giao dịch"],
                    "Số thẻ": selected_row.iloc[0]["Số thẻ"],
                    "RRN": selected_row.iloc[0]["RRN"],
                    "Loại giao dịch": loai_giao_dich,
                    "Số tiền giao dịch": selected_row.iloc[0]["Số tiền giao dịch"],
                    "Số chuẩn chi": selected_row.iloc[0]["Số chuẩn chi"],
                    "Mã thiết bị": selected_row.iloc[0]["Mã thiết bị"]
                })
                st.success(f"Đã tạo thành công hồ sơ tra soát **{new_id}**!")


elif current_page == "Tạo tra soát theo lô":
    st.header("📦 Tạo tra soát theo lô (Batch Processing)")
    st.info("💡 **Hướng dẫn:** Tải file template mẫu, điền dữ liệu, sau đó tải lên để hệ thống kiểm tra, phân loại giao dịch thành công/lỗi, đính kèm chứng từ và tạo tra soát.")

    # 1. Tải Template mẫu
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.markdown("Tải file mẫu định dạng Excel/CSV để nhập danh sách giao dịch tra soát theo đúng quy chuẩn.")
    with col_t2:
        if st.button("📥 Tải Template Mẫu (.xlsx)"):
            st.toast("Đã tải xuống file template mẫu thành công!", icon="📁")

    st.markdown("---")
    
    # 2. Upload file
    uploaded_batch_file = st.file_uploader("📂 Tải lên file danh sách giao dịch (Excel, CSV)", type=["xlsx", "csv"])
    
    batch_reason = st.selectbox("Lý do tra soát chung cho cả lô", [
        "Lỗi hệ thống trừ tiền hàng loạt", 
        "Giao dịch giả mạo diện rộng", 
        "Trừ tiền trùng lặp định kỳ",
        "Khác"
    ])

    if uploaded_batch_file is not None or st.checkbox("Sử dụng dữ liệu file mẫu giả lập để kiểm thử", value=True):
        st.markdown("### 📊 Kết quả kiểm tra file lô")
        
        # Thống kê kết quả kiểm tra
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("✅ Giao dịch hợp lệ (Thành công)", "4 giao dịch")
        col_m2.metric("❌ Giao dịch lỗi (Cần chỉnh sửa)", "1 giao dịch")

        # Hiển thị chia tab thành công / lỗi
        tab_success, tab_error = st.tabs(["Giao dịch thành công (Hợp lệ)", "Giao dịch lỗi (Không hợp lệ)"])

        with tab_success:
            st.markdown("Tích chọn các giao dịch hợp lệ bạn muốn đưa vào hồ sơ tra soát lô:")
            if 'df_batch_success' not in st.session_state:
                st.session_state.df_batch_success = pd.DataFrame({
                    "Chọn": [True, True, True, True],
                    "Mã GD": ["TX-B01", "TX-B02", "TX-B03", "TX-B04"],
                    "Ngày GD": ["01/06/2026", "01/06/2026", "02/06/2026", "02/06/2026"],
                    "CIF": ["100111", "100222", "100333", "100444"],
                    "Số tiền": ["500,000 VND", "1,200,000 VND", "300,000 VND", "4,500,000 VND"],
                    "Nội dung": ["Thanh toán POS", "Chuyển khoản lỗi", "Rút tiền ATM", "Mua sắm Online"]
                })

            edited_success_df = st.data_editor(
                st.session_state.df_batch_success,
                use_container_width=True,
                hide_index=True,
                column_config={"Chọn": st.column_config.CheckboxColumn("☑️ Đánh dấu / Chọn giao dịch")}
            )

        with tab_error:
            st.markdown("Danh sách các dòng dữ liệu bị lỗi định dạng hoặc thiếu thông tin từ file tải lên:")
            df_err_demo = pd.DataFrame({
                "Dòng": [5],
                "Mã GD": ["TX-ERR-99"],
                "Ngày GD": ["31/02/2026"],
                "CIF": ["-"],
                "Số tiền": ["abc_vnd"],
                "Chi tiết lỗi": ["Sai định dạng ngày tháng & Thiếu mã CIF khách hàng"]
            })
            st.dataframe(df_err_demo, use_container_width=True)
            st.warning("⚠️ Vui lòng sửa lại các lỗi trên ở file nguồn và tải lại lên nếu cần bổ sung.")

        # Lọc các dòng được đánh dấu chọn thành công
        selected_success_rows = edited_success_df[edited_success_df["Chọn"] == True]

        if not selected_success_rows.empty:
            st.markdown("---")
            st.subheader("📎 Đính kèm chứng từ chung cho lô tra soát")
            batch_uploaded_files = st.file_uploader(
                "Tải lên công văn, bảng kê hoặc biên lai tổng hợp (PDF, Ảnh, Excel)", 
                type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx"], 
                accept_multiple_files=True,
                key="batch_files_main"
            )

            batch_note = st.text_area("Ghi chú bổ sung cho hồ sơ tra soát theo lô:")

            if st.button("🚀 Tạo hồ sơ tra soát theo lô chính thức", type="primary"):
                file_names = [f.name for f in batch_uploaded_files] if batch_uploaded_files else []
                new_id = f"TS-BATCH-2026-00{len(st.session_state.disputes_db) + 1}"

                st.session_state.disputes_db.append({
                    "Mã tra soát": new_id,
                    "Trạng thái tra soát": "Chờ phê duyệt",
                    "Trạng thái hạch toán": "Chưa hạch toán",
                    "CIF": "Lô nhiều CIF",
                    "Tên chủ thẻ": f"Lô KH ({len(selected_success_rows)} giao dịch)",
                    "Ngày giao dịch": "01/06/2026",
                    "Số thẻ": "N/A (Lô)",
                    "RRN": "N/A",
                    "Loại giao dịch": batch_reason,
                    "Số tiền giao dịch": f"{len(selected_success_rows)} giao dịch thành công",
                    "Số chuẩn chi": "N/A",
                    "Mã thiết bị": "N/A"
                })
                st.success(f"🎉 Đã tạo thành công hồ sơ tra soát theo lô **{new_id}** gồm {len(selected_success_rows)} giao dịch được chọn và {len(file_names)} chứng từ đính kèm!")
        else:
            st.warning("⚠️ Vui lòng đánh dấu chọn ít nhất một giao dịch thành công để tiếp tục tạo tra soát.")


elif current_page == "Tất cả hồ sơ":
    st.header("⏳ Tra soát chờ xử lý - Tất cả hồ sơ")
    df_db = pd.DataFrame(st.session_state.disputes_db)
    st.dataframe(df_db, use_container_width=True)


elif current_page == "Hồ sơ của tôi":
    st.header("👤 Hồ sơ của tôi (Maker & Phê duyệt)")
    
    # Bộ lọc tìm kiếm & vấn tin giống phần Vấn tin tra soát
    with st.form("form_my_records_query"):
        st.subheader("Bộ lọc tìm kiếm hồ sơ của tôi")
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            q_id = st.text_input("Mã tra soát", placeholder="VD: TS-2026-001")
        with col_q2:
            q_cif = st.text_input("Mã CIF", placeholder="Nhập CIF...")
        with col_q3:
            q_name = st.text_input("Tên chủ thẻ", placeholder="Nhập tên...")

        with st.expander("⚙️ Bộ lọc mở rộng (Trạng thái, Loại giao dịch)"):
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                q_status = st.selectbox("Trạng thái tra soát", ["Tất cả", "Chờ phê duyệt", "Đang xử lý", "Từ chối xử lý", "Hoàn thành"])
            with col_ex2:
                q_type = st.selectbox("Loại giao dịch", ["Tất cả", "ATM", "POS"])

        submitted_my_query = st.form_submit_button("🔎 Lọc và tìm kiếm hồ sơ", use_container_width=True)

    # Lọc dữ liệu từ database
    df_my_result = pd.DataFrame(st.session_state.disputes_db)

    # Mặc định có thể lọc các hồ sơ liên quan hoặc hiển thị toàn bộ dựa trên điều kiện lọc
    if submitted_my_query:
        if q_id:
            df_my_result = df_my_result[df_my_result["Mã tra soát"].str.contains(q_id, case=False, na=False)]
        if q_cif:
            df_my_result = df_my_result[df_my_result["CIF"].str.contains(q_cif, case=False, na=False)]
        if q_name:
            df_my_result = df_my_result[df_my_result["Tên chủ thẻ"].str.contains(q_name, case=False, na=False)]
        if q_status != "Tất cả":
            df_my_result = df_my_result[df_my_result["Trạng thái tra soát"] == q_status]
        if q_type != "Tất cả":
            df_my_result = df_my_result[df_my_result["Loại giao dịch"] == q_type]

    st.markdown(f"### Danh sách kết quả ({len(df_my_result)} bản ghi)")
    st.dataframe(df_my_result, use_container_width=True)
    
    # Phần thao tác phê duyệt nhanh bên dưới bảng (nếu có hồ sơ chờ duyệt)
    pending_items = [d for d in st.session_state.disputes_db if d["Trạng thái tra soát"] == "Chờ phê duyệt"]
    if pending_items:
        with st.expander("⚡ Thao tác phê duyệt nhanh cho các hồ sơ Chờ phê duyệt"):
            for item in pending_items:
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.write(f"**{item['Mã tra soát']}** - {item['Tên chủ thẻ']} ({item['Loại giao dịch']})")
                with cols[1]:
                    if st.button(f"✅ Duyệt {item['Mã tra soát']}", key=f"quick_app_{item['Mã tra soát']}"):
                        item["Trạng thái tra soát"] = "Đang xử lý"
                        item["Trạng thái hạch toán"] = "Hạch toán thành công"
                        st.rerun()
                with cols[2]:
                    if st.button(f"❌ Từ chối", key=f"quick_rej_{item['Mã tra soát']}"):
                        item["Trạng thái tra soát"] = "Từ chối xử lý"
                        st.rerun()


elif current_page == "Sắp đến hạn":
    st.header("⚠️ Danh sách Tra soát sắp đến hạn SLA")
    sla_data = pd.DataFrame({
        "Mã Tra soát": ["TS-2026-001", "TS-2026-003"],
        "Hạn chót SLA": ["2026-06-05 16:00", "2026-06-06 12:00"],
        "Nội dung": ["ATM - Rút tiền không thành công", "POS - Thanh toán trùng lặp"],
        "Độ khẩn": ["Khẩn cấp", "Bình thường"]
    })
    st.dataframe(sla_data, use_container_width=True)


elif current_page == "Vấn tin tra soát":
    st.header("🔍 Vấn tin chi tiết tra soát")
    search_id = st.text_input("Nhập Mã tra cứu (VD: TS-2026-001):")
    if search_id:
        found = next((d for d in st.session_state.disputes_db if d["Mã tra soát"].lower() == search_id.lower()), None)
        if found:
            st.success(f"Đã tìm thấy thông tin cho mã: **{found['Mã tra soát']}**")
            st.json(found)
        else:
            st.error("Không tìm thấy mã tra soát phù hợp!")


elif current_page == "Quản lý chứng từ":
    st.header("📁 Kho quản lý chứng từ đính kèm")
    st.info("Khu vực kiểm tra, xem trước và lưu trữ toàn bộ biên lai, công văn tra soát.")


elif current_page == "Báo cáo thống kê TSKN":
    st.header("📊 Báo cáo thống kê tổng quan hiệu suất")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Tổng số hồ sơ", len(st.session_state.disputes_db))
    col_m2.metric("Chờ phê duyệt", len([d for d in st.session_state.disputes_db if d["Trạng thái tra soát"] == "Chờ phê duyệt"]))
    col_m3.metric("Đang xử lý", len([d for d in st.session_state.disputes_db if d["Trạng thái tra soát"] == "Đang xử lý"]))


elif current_page == "Xuất file báo cáo":
    st.header("📥 Xuất dữ liệu báo cáo hệ thống")
    if st.button("📥 Tải xuống báo cáo định dạng Excel", type="primary"):
        st.success("Đã xuất và tải file Excel thành công!")