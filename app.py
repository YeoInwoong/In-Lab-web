import streamlit as st

reaction_db = {
    "Suzuki coupling": {
        "촉매": "Pd(PPh₃)₄ (3 mol%)",
        "용매": "THF/H₂O (3:1)",
        "염기": "K₂CO₃ (2 eq)",
        "온도": "80°C",
        "시간": "12시간",
        "분위기": "질소 (N₂)",
        "참고": "J. Org. Chem. 2005, 70, 2762–2769",
        "메커니즘": "Pd(0)가 aryl halide에 산화적 첨가 → transmetallation → 환원적 제거"
    },
    "Grignard reaction": {
        "촉매": "무촉매",
        "용매": "무수 Ether",
        "온도": "0~25°C",
        "시간": "1~2시간",
        "분위기": "무수 조건, 질소",
        "참고": "Org. Synth. 1931, 11, 36",
        "메커니즘": "R-MgX가 electrophile (예: ketone, ester)에 친핵성 첨가 → 알콜 생성"
    },
    "Heck reaction": {
        "촉매": "Pd(OAc)₂ + PPh₃",
        "용매": "DMF",
        "염기": "Et₃N 또는 Na₂CO₃",
        "온도": "120°C",
        "시간": "12~24시간",
        "분위기": "질소 또는 아르곤",
        "참고": "J. Org. Chem. 1982, 47, 4766",
        "메커니즘": "Pd(0)가 aryl halide에 산화적 첨가 → alkene과 삽입 → 베타 수소 제거"
    },
    "Amidation": {
        "촉매": "DCC 또는 EDC",
        "용매": "DCM 또는 DMF",
        "염기": "NEt₃",
        "온도": "RT 또는 0°C",
        "시간": "2~6시간",
        "분위기": "질소",
        "참고": "Tetrahedron Lett. 1997, 38, 5251",
        "메커니즘": "산(carboxylic acid)을 carbodiimide로 활성화 → amine이 공격 → amide 형성"
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
            if key != "메커니즘":
                st.markdown(f"**{key}**: {value}")

        st.subheader("⚙️ 반응 메커니즘")
        st.markdown(info.get("메커니즘", "메커니즘 정보 없음"))
    else:
        st.error("등록되지 않은 반응입니다.")
