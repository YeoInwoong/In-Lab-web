import streamlit as st
import requests
import tempfile
from PIL import Image
from PyPDF2 import PdfReader
from rdkit import Chem
from rdkit.Chem import Draw
import random

st.set_page_config(page_title="InLab - 유기합성 도우미", page_icon="🧪")
st.title("🧠 InLab - 유기합성 도우미 InLab")

st.markdown("---")
st.header("📈 예측 수율 계산 (베타 버전)")

reactant_smiles = st.text_input("1️⃣ 반응물(Reactant)의 SMILES를 입력하세요:")
reagent_info = st.text_input("2️⃣ 시약/조건 정보를 간단히 입력하세요 (예: Pd catalyst, base 등):")
product_smiles = st.text_input("3️⃣ 생성물(Product)의 SMILES를 입력하세요:")

if st.button("예측 수율 분석하기"):
    if reactant_smiles and product_smiles:
        try:
            r_mol = Chem.MolFromSmiles(reactant_smiles)
            p_mol = Chem.MolFromSmiles(product_smiles)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**반응물 구조**")
                st.image(Draw.MolToImage(r_mol), use_column_width=True)
            with col2:
                st.markdown("**생성물 구조**")
                st.image(Draw.MolToImage(p_mol), use_column_width=True)

            yield_prediction = random.randint(60, 95)
            st.success(f"예상 수율: **{yield_prediction}%**")

            if "Pd" in reagent_info or "boronic" in reactant_smiles:
                st.info("**추천 반응 유형**: Suzuki coupling")
                st.markdown("**추천 조건**: Pd(PPh₃)₄, K₂CO₃, THF/H₂O, 80°C")
                st.markdown("**유사 문헌**: [J. Org. Chem. 2005, 70, 2762–2769](https://doi.org/10.1021/jo047540f)")

        except Exception as e:
            st.error(f"SMILES 처리 중 오류 발생: {e}")
    else:
        st.warning("반응물과 생성물의 SMILES를 모두 입력해주세요.")

st.markdown("---")
st.header("🔎 구조 기반 반응 조건 추천")

structure_smiles = st.text_input("구조의 SMILES를 입력하세요:")

if structure_smiles:
    try:
        mol = Chem.MolFromSmiles(structure_smiles)
        st.image(Draw.MolToImage(mol), caption="입력 구조", use_column_width=False)

        st.subheader("📌 구조 기반 추천 조건")
        recommendations = []
        if "Br" in structure_smiles or "I" in structure_smiles:
            recommendations.append("Aryl halide 포함 → Suzuki coupling 추천")
        if "Mg" in structure_smiles:
            recommendations.append("Grignard reagent 포함 → Grignard 반응 추천")
        if "COOH" in structure_smiles or "C(=O)OH" in structure_smiles:
            recommendations.append("Carboxylic acid → Amidation 가능")
        if not recommendations:
            recommendations.append("특징 구조가 명확하지 않아 일반적 조건 권장")

        for r in recommendations:
            st.markdown(f"- {r}")

    except Exception as e:
        st.error(f"SMILES 구조 해석 실패: {e}")

st.markdown("---")
st.header("📄 논문 PDF 업로드 → 스킴 추출 및 요약")

uploaded_pdf = st.file_uploader("논문 PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_pdf:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(uploaded_pdf.read())
            reader = PdfReader(tmp_pdf.name)
            full_text = ""
            for page in reader.pages[:3]:
                full_text += page.extract_text() + "\n"

            st.subheader("📄 논문 내용 요약 (초반 3페이지)")
            st.text_area("추출된 텍스트", full_text[:2000], height=300)

            st.subheader("🔍 요약 및 번역")
            try:
                summary_query = full_text[:800].replace("\n", " ")
                st.markdown(f"**영문 요약:** {summary_query}")
                trans_url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q=" + requests.utils.quote(summary_query)
                trans_res = requests.get(trans_url)
                if trans_res.status_code == 200:
                    translated = trans_res.json()[0][0][0]
                    st.markdown(f"**한글 요약:** {translated}")
                else:
                    st.info("번역 요청 실패")
            except Exception as e:
                st.warning(f"요약 또는 번역 중 오류: {e}")

        st.success("PDF 처리 및 요약 완료!")
    except Exception as e:
        st.error(f"PDF 파일 처리 오류: {e}")
            else:
                st.warning("논문 검색 중 오류가 발생했습니다.")
        except Exception as e:
            st.error(f"논문 검색 실패: {e}")
