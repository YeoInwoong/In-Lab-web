import streamlit as st
import requests
import tempfile
from PIL import Image

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

        st.subheader("📚 관련 논문 검색 결과")
        try:
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={reaction_name}&limit=3&fields=title,authors,url,year"
            response = requests.get(url)
            if response.status_code == 200:
                papers = response.json().get("data", [])
                if papers:
                    for paper in papers:
                        st.markdown(f"- **{paper['title']}** ({paper['year']})")
                        st.markdown(f"  - [🔗 링크]({paper['url']})")
                else:
                    st.info("논문 검색 결과가 없습니다.")
            else:
                st.warning("논문 검색 중 오류가 발생했습니다.")
        except Exception as e:
            st.error(f"논문 검색 실패: {e}")
    else:
        st.error("등록되지 않은 반응입니다.")

st.markdown("---")
st.header("🔍 최종 화합물 구조 이미지로 문헌 검색하기")

uploaded_image = st.file_uploader("최종 화합물 구조 이미지를 업로드하세요 (jpg, png)", type=["jpg", "png"])

if uploaded_image:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_image.read())
        st.image(Image.open(tmp_file.name), caption="업로드한 구조 이미지", use_column_width=True)
        st.info("⚠️ 현재는 이미지 파일명 기반 키워드로 논문 검색이 진행됩니다. (OCR/구조인식은 추후 추가 예정)")

        keyword = uploaded_image.name.split(".")[0]  # 파일명에서 확장자 제거

        st.subheader("📚 구조 기반 논문 검색 결과")
        try:
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={keyword}&limit=3&fields=title,authors,url,year"
            response = requests.get(url)
            if response.status_code == 200:
                papers = response.json().get("data", [])
                if papers:
                    for paper in papers:
                        st.markdown(f"- **{paper['title']}** ({paper['year']})")
                        st.markdown(f"  - [🔗 링크]({paper['url']})")
                else:
                    st.info("논문 검색 결과가 없습니다.")
            else:
                st.warning("논문 검색 중 오류가 발생했습니다.")
        except Exception as e:
            st.error(f"논문 검색 실패: {e}")
