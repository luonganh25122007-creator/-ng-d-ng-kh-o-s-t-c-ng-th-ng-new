"""Ứng dụng khảo sát và phân tích mức độ căng thẳng của học sinh."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st


# Tất cả dữ liệu được lưu cục bộ cạnh ứng dụng.
DATA_FILE = Path(__file__).with_name("stress_data.csv")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "").strip()

QUESTIONS = [
    "Em cảm thấy áp lực vì khối lượng bài tập hoặc lịch học.",
    "Em lo lắng về điểm số, bài kiểm tra hoặc kết quả học tập.",
    "Em thường cảm thấy thiếu ngủ hoặc mệt mỏi vì việc học.",
    "Em khó tập trung hoặc khó thư giãn do lo nghĩ chuyện học.",
    "Em cảm thấy căng thẳng trong mối quan hệ với bạn bè.",
    "Em cảm thấy căng thẳng khi giao tiếp với thầy cô.",
]

LIKERT_LABELS = {
    1: "Không bao giờ",
    2: "Hiếm khi",
    3: "Thỉnh thoảng",
    4: "Thường xuyên",
    5: "Gần như luôn luôn",
}

DATA_COLUMNS = [
    "Thời gian khảo sát",
    "Họ tên hoặc mã số",
    "Lớp",
    *QUESTIONS,
    "Tổng điểm",
    "Mức độ",
]

LEVELS = [
    (11, "Thấp"),
    (17, "Trung bình"),
    (23, "Cao"),
    (30, "Báo động"),
]

RECOMMENDATIONS = {
    "Thấp": [
        "Duy trì giờ ngủ đều đặn, nghỉ giải lao và các hoạt động em yêu thích.",
        "Ghi lại việc cần làm; chia bài tập thành các phần nhỏ để dễ bắt đầu.",
        "Thử Pomodoro: học tập trung 25 phút, nghỉ 5 phút; điều chỉnh cho phù hợp.",
    ],
    "Trung bình": [
        "Lập danh sách việc theo mức độ ưu tiên và chia nhiệm vụ lớn thành bước nhỏ.",
        "Thử Pomodoro: tập trung 25 phút, nghỉ 5 phút; sau 4 lượt nghỉ dài hơn.",
        "Thử hít vào nhẹ nhàng 4 nhịp, thở ra 6 nhịp trong vài phút; dừng lại nếu khó chịu.",
        "Trao đổi với người thân, giáo viên hoặc người em tin tưởng về điều đang gây áp lực.",
    ],
    "Cao": [
        "Tạm chia nhỏ việc học và ưu tiên ngủ, ăn uống, vận động; tránh cố học liên tục.",
        "Thử thở chậm, thả lỏng vai và nghỉ ngắn ở nơi yên tĩnh nếu thấy phù hợp.",
        "Chủ động trao đổi sớm với cha mẹ/người giám hộ, giáo viên chủ nhiệm hoặc tư vấn học đường.",
        "Cùng người lớn đáng tin cậy rà soát lịch học để giảm tải và tìm hỗ trợ phù hợp.",
    ],
    "Báo động": [
        "Hãy báo ngay với cha mẹ/người giám hộ, giáo viên đáng tin cậy hoặc nhân viên tư vấn học đường.",
        "Nhờ người lớn hỗ trợ sắp xếp gặp chuyên gia sức khỏe tinh thần; em không cần tự giải quyết một mình.",
        "Nếu em đang không an toàn hoặc có ý nghĩ làm hại bản thân, hãy nói ngay với người lớn ở gần và liên hệ dịch vụ khẩn cấp tại địa phương.",
    ],
}


def classify_score(score: int) -> str:
    """Phân loại tổng điểm của 6 câu hỏi theo bốn mức."""
    for upper_bound, level in LEVELS:
        if score <= upper_bound:
            return level
    raise ValueError("Tổng điểm phải nằm trong khoảng từ 6 đến 30.")


def load_data() -> pd.DataFrame:
    """Đọc CSV; trả về bảng rỗng nếu tệp chưa tồn tại hoặc chưa có dữ liệu."""
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=DATA_COLUMNS)

    try:
        data = pd.read_csv(DATA_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=DATA_COLUMNS)

    missing_columns = [column for column in DATA_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(
            "Tệp dữ liệu thiếu các cột bắt buộc: " + ", ".join(missing_columns)
        )
    return data[DATA_COLUMNS]


def save_response(response: dict[str, Any]) -> None:
    """Ghi một phản hồi khảo sát vào cuối tệp CSV."""
    pd.DataFrame([response], columns=DATA_COLUMNS).to_csv(
        DATA_FILE,
        mode="a",
        header=not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0,
        index=False,
        encoding="utf-8-sig",
    )


def show_recommendations(level: str) -> None:
    """Hiển thị lời khuyên ứng với mức điểm vừa nhận."""
    for recommendation in RECOMMENDATIONS[level]:
        st.markdown(f"- {recommendation}")


def render_home() -> None:
    """Giới thiệu mục đích và lưu ý của khảo sát."""
    st.title("Ứng dụng Khảo sát và Phân tích Mức độ Căng thẳng của Học sinh")
    st.subheader("Lắng nghe để học tập cân bằng hơn")
    st.write(
        "Ứng dụng giúp học sinh tự nhìn nhận một số áp lực thường gặp trong học tập "
        "và sinh hoạt, từ đó tham khảo gợi ý chăm sóc bản thân và tìm kiếm hỗ trợ."
    )
    st.info(
        "Khảo sát chỉ mang tính tham khảo, không phải công cụ chẩn đoán hay thay thế "
        "tư vấn chuyên môn. Nếu em đang gặp khó khăn, hãy chia sẻ với người lớn "
        "đáng tin cậy hoặc nhân viên tư vấn học đường."
    )
    st.markdown(
        """
        **Cách sử dụng**
        1. Trả lời 6 câu hỏi trong tab **Khảo sát** theo cảm nhận gần đây.
        2. Xem điểm, biểu đồ và gợi ý trong tab **Kết quả & Đề xuất**.
        3. Giáo viên/cán bộ được cấp quyền có thể xem thống kê trong tab **Quản lý**.

        Mỗi câu được chấm từ **1 (Không bao giờ)** đến **5 (Gần như luôn luôn)**.
        Điểm cao hơn thể hiện nhiều dấu hiệu căng thẳng được ghi nhận hơn.
        """
    )


def render_survey() -> None:
    """Hiển thị biểu mẫu và kiểm tra dữ liệu trước khi lưu."""
    st.header("Khảo sát mức độ căng thẳng")
    st.caption("Các câu trả lời được lưu trong tệp cục bộ stress_data.csv.")

    with st.form("stress_survey"):
        student_id = st.text_input(
            "Họ tên hoặc mã số học sinh",
            max_chars=100,
            help="Chỉ nhập thông tin cần thiết theo hướng dẫn của nhà trường.",
        )
        class_name = st.text_input("Lớp", max_chars=50)
        answers: dict[str, int | None] = {}

        st.markdown("#### Trong thời gian gần đây, em...")
        for index, question in enumerate(QUESTIONS):
            answers[question] = st.selectbox(
                question,
                options=[None, *LIKERT_LABELS.keys()],
                format_func=lambda value: (
                    "Chọn mức độ" if value is None else f"{value} - {LIKERT_LABELS[value]}"
                ),
                key=f"answer_{index}",
            )

        submitted = st.form_submit_button(
            "Gửi kết quả và Phân tích", type="primary", width="stretch"
        )

    if not submitted:
        return
    if not student_id.strip() or not class_name.strip():
        st.error("Vui lòng nhập họ tên/mã số học sinh và lớp.")
        return
    if any(answer is None for answer in answers.values()):
        st.error("Vui lòng chọn mức độ cho tất cả câu hỏi.")
        return

    scores = {question: int(answer) for question, answer in answers.items()}
    total = sum(scores.values())
    level = classify_score(total)
    response: dict[str, Any] = {
        "Thời gian khảo sát": datetime.now().astimezone().isoformat(timespec="seconds"),
        "Họ tên hoặc mã số": student_id.strip(),
        "Lớp": class_name.strip(),
        **scores,
        "Tổng điểm": total,
        "Mức độ": level,
    }

    try:
        save_response(response)
    except OSError as error:
        st.error(f"Không thể lưu kết quả vào {DATA_FILE.name}: {error}")
        return

    st.session_state["latest_result"] = response
    st.success("Đã lưu kết quả khảo sát. Mở tab **Kết quả & Đề xuất** để xem phân tích.")


def render_results() -> None:
    """Hiển thị kết quả cá nhân gần nhất trong phiên hiện tại."""
    st.header("Kết quả & Đề xuất")
    result = st.session_state.get("latest_result")
    if not result:
        st.info("Em hãy hoàn thành khảo sát để xem kết quả tại đây.")
        return

    total = int(result["Tổng điểm"])
    level = str(result["Mức độ"])
    st.metric("Tổng điểm căng thẳng", f"{total}/30", level)
    st.caption(
        "Mức điểm chỉ phản ánh câu trả lời tại thời điểm khảo sát, "
        "không phải kết luận y khoa."
    )

    chart_data = pd.DataFrame(
        {
            "Khía cạnh": QUESTIONS,
            "Điểm (1–5)": [int(result[question]) for question in QUESTIONS],
        }
    )
    chart = px.bar(
        chart_data,
        x="Điểm (1–5)",
        y="Khía cạnh",
        orientation="h",
        range_x=[0, 5],
        text="Điểm (1–5)",
        title="Các khía cạnh em đã tự đánh giá",
    )
    chart.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(chart, width="stretch")

    st.subheader(f"Gợi ý dành cho mức độ {level.lower()}")
    show_recommendations(level)


def render_admin() -> None:
    """Hiển thị thống kê tổng hợp sau khi xác thực mật khẩu quản trị."""
    st.header("Quản lý dữ liệu khảo sát")
    st.warning(
        "Dữ liệu có thể chứa thông tin cá nhân và chỉ nên được xem bởi người có thẩm quyền. "
        "Tệp CSV được lưu trên máy chạy ứng dụng."
    )
    if not ADMIN_PASSWORD:
        st.info(
            "Tab quản lý đang khóa. Quản trị viên cần đặt biến môi trường "
            "ADMIN_PASSWORD trước khi chạy ứng dụng; xem README.md."
        )
        return

    entered_password = st.text_input(
        "Mật khẩu quản trị", type="password", key="admin_password"
    )
    if not entered_password:
        st.info("Nhập mật khẩu quản trị để xem thống kê.")
        return
    if entered_password != ADMIN_PASSWORD:
        st.error("Mật khẩu quản trị không chính xác.")
        return

    try:
        data = load_data()
    except (OSError, ValueError, pd.errors.ParserError) as error:
        st.error(f"Không thể đọc dữ liệu khảo sát: {error}")
        return

    if data.empty:
        st.info("Chưa có dữ liệu khảo sát.")
        return

    data["Tổng điểm"] = pd.to_numeric(data["Tổng điểm"], errors="coerce")
    data = data.dropna(subset=["Tổng điểm"])
    if data.empty:
        st.info("Tệp chưa có điểm khảo sát hợp lệ.")
        return

    metric_col, average_col = st.columns(2)
    metric_col.metric("Số lượt khảo sát", len(data))
    average_col.metric("Điểm trung bình", f"{data['Tổng điểm'].mean():.1f}/30")

    class_summary = (
        data.groupby("Lớp", dropna=False)["Tổng điểm"]
        .agg(["count", "mean"])
        .rename(columns={"count": "Số lượt khảo sát", "mean": "Điểm trung bình"})
        .reset_index()
    )
    class_summary["Điểm trung bình"] = class_summary["Điểm trung bình"].round(1)
    st.subheader("Thống kê theo lớp")
    st.dataframe(class_summary, width="stretch", hide_index=True)

    st.download_button(
        "Tải dữ liệu CSV",
        data=data.to_csv(index=False).encode("utf-8-sig"),
        file_name="stress_data.csv",
        mime="text/csv",
    )


def main() -> None:
    """Cấu hình giao diện và điều hướng các khu vực của ứng dụng."""
    st.set_page_config(
        page_title="Khảo sát căng thẳng học sinh",
        page_icon="📚",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .block-container {max-width: 1100px; padding-top: 2rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    home_tab, survey_tab, results_tab, admin_tab = st.tabs(
        ["Giới thiệu", "Khảo sát", "Kết quả & Đề xuất", "Quản lý"]
    )
    with home_tab:
        render_home()
    with survey_tab:
        render_survey()
    with results_tab:
        render_results()
    with admin_tab:
        render_admin()


if __name__ == "__main__":
    main()
