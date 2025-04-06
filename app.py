
import streamlit as st

reaction_db = {
    "Suzuki coupling": {
        "촉매": "Pd(PPh₃)₄ (3 mol%)",
        "용매": "THF/H₂O (3:1)",
        "염기": "K₂CO₃ (2 eq)",
        "온도": "80°C",
        "시간": "12시간",
        "분위기": "질소 (N₂)",
        "참고": "J. Org. Chem. 2005, 70, 2762–2769"
    },
    "Grignard reaction": {
        "촉매": "무촉매",
        "용매": "무수 Ether",
        "온도": "0~25°C",
        "시간": "1~2시간",
        "분위기": "무수 조건, 질소",
        "참고": "Org. Synth. 1931, 11, 36"
    }
}

st.set_page_config(page_title="InLab - 반응 조건 추천기", page_icon="🧪")
st.title("🧠 InLab - 유기합성 반응 조건 추천기")

reaction_name = st.selectbox("반응을 선택하세요:", list(reaction_db.keys()))

if st.button("조건 추천 받기"):
    info = reaction_db.get(reaction_name)
    if info:
        st.subheader(f"🔬 [ {reaction_name} 추천 조건 ]")
        for key, value in info.items():
            st.markdown(f"**{key}**: {value}")
    else:
        st.error("등록되지 않은 반응입니다.")
        