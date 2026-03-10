import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import random
import calendar
from datetime import date
import holidays
import io

# -------------------------------------------------------------------------
# 1. 안전점검표 이미지 생성 및 글자 덮어쓰기 함수
# -------------------------------------------------------------------------
def create_monthly_checklist(year, month):
    base_image_path = "image_3e5ff8.png"  # 빈 양식 파일명
    # ---------------------------------------------------------
    # 📍 [필수 수정] 새로 추가된 텍스트 입력 좌표 (그림판/추출기로 찾아서 변경하세요!)
    # ---------------------------------------------------------
    coord_dept = (1049, 106) # '소속' 글자를 쓸 시작 X, Y 좌표 (예시)
    coord_lab = (1049, 125)  # '연구실명' 글자를 쓸 시작 X, Y 좌표 (예시)
    coord_loc = (1049, 144) # '위치' 글자를 쓸 시작 X, Y 좌표 (예시)
    # ---------------------------------------------------------
    
    # [좌표 설정부] 마우스 좌표 추출기로 직접 찾은 1~31일의 정확한 X좌표 31개
    circle_x_list = [
        506, 550, 598, 641, 685, 728, 766, 807, 841, 876, 
        916, 954, 988, 1027, 1062, 1097, 1133, 1174, 1210, 1246, 
        1282, 1317, 1355, 1389, 1428, 1464, 1504, 1538, 1579, 1611, 
        1653
    ]

    # 마우스 좌표 추출기로 직접 찾은 Y좌표
    circle_y_list = [
        216, 241, 265, 291, 316, 351, 371, 391, 
        421, 441, 466, 491, 516, 541, 566, 591, 
        616, 641, 666, 709, 741, 766, 791, 816, 841, 866
    ]
    sign_y_list = [994, 1030] # 994: 위쪽(점검자), 1030: 아래쪽(책임자)
    
    circle_size = (16, 16) 
    sign_size = (30, 30)   

    # 이번 달 평일 계산 (공휴일 제외)
    kr_holidays = holidays.KR(years=year)
    _, last_day = calendar.monthrange(year, month)
    
    valid_days = [
        day for day in range(1, last_day + 1)
        if date(year, month, day).weekday() < 5 and date(year, month, day) not in kr_holidays
    ]

    try:
        base_img = Image.open(base_image_path).convert("RGBA")
    except Exception as e:
        st.error(f"기본 양식 이미지를 찾을 수 없습니다: {e}")
        return None

    def load_images(folder, size):
        images = []
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(".png"):
                    img = Image.open(os.path.join(folder, file)).convert("RGBA")
                    img = img.resize(size, Image.Resampling.LANCZOS)
                    images.append(img)
        return images

    # 이미지 불러오기 (점검자용, 책임자용 서명 분리)
    circles = load_images("circles", circle_size)
    signs_inspector = load_images("signatures", sign_size)          # 위쪽: 단순 서명
    signs_manager = load_images("signatures_complex", sign_size)    # 아래쪽: 복잡한 서명

    if not circles or not signs_inspector or not signs_manager:
        st.error("오류: 'circles', 'signatures', 'signatures_complex' 폴더 중 이미지가 없는 곳이 있습니다.")
        return None

    result_img = base_img.copy()
    
    # ---------------------------------------------------------
    # 기존 연도/월 지우고 새 글자 쓰기
    # ---------------------------------------------------------
    draw = ImageDraw.Draw(result_img)
    
    draw.rectangle([(658, 47), (808, 88)], fill="white") # 연도 지우기 영역
    draw.rectangle([(827, 47), (897, 88)], fill="white") # 월 지우기 영역
    
    try:
        font = ImageFont.truetype("MALGUN.TTF", 36)
        font_info = ImageFont.truetype("MALGUN.TTF", 26)  # 소속/연구실명 폰트 (칸 크기에 맞춰 조절)
    except IOError:
        font = ImageFont.load_default()
        
    draw.text((668, 47), f"{year}년도", font=font, fill="black")
    draw.text((837, 47), f"{month}월", font=font, fill="black")
    # ---------------------------------------------------------

    # 평일에만 동그라미 및 서명 도장 찍기
    for day in valid_days:
        current_x = circle_x_list[day - 1]
        
        # 1. 점검 항목 동그라미
        for y in circle_y_list:
            circle_img = random.choice(circles)
            paste_x = current_x - (circle_size[0] // 2) + random.randint(-2, 2)
            paste_y = y - (circle_size[1] // 2) + random.randint(-2, 2)
            result_img.paste(circle_img, (paste_x, paste_y), circle_img)

        # 2. 위쪽 점검자 서명 (signatures 폴더)
        inspector_img = random.choice(signs_inspector) 
        paste_x_insp = current_x - (sign_size[0] // 2) + random.randint(-2, 2)
        paste_y_insp = sign_y_list[0] - (sign_size[1] // 2) + random.randint(-2, 2)
        result_img.paste(inspector_img, (paste_x_insp, paste_y_insp), inspector_img)

        # 3. 아래쪽 책임자 서명 (signatures_complex 폴더)
        manager_img = random.choice(signs_manager)
        paste_x_mgr = current_x - (sign_size[0] // 2) + random.randint(-2, 2)
        paste_y_mgr = sign_y_list[1] - (sign_size[1] // 2) + random.randint(-2, 2)
        result_img.paste(manager_img, (paste_x_mgr, paste_y_mgr), manager_img)

    # 최종 이미지 변환
    final_img = Image.new("RGB", result_img.size, (255, 255, 255))
    final_img.paste(result_img, mask=result_img.split()[3])
    
    return final_img

# -------------------------------------------------------------------------
# 2. Streamlit 웹 UI 구성
# -------------------------------------------------------------------------
st.set_page_config(page_title="연구실 안전관리 점검표 자동화", layout="centered")

st.title("📝 연구실 안전관리 일일점검표 자동 생성기")
st.write("담당자: **추부건** | 연도와 월을 선택하면 자동으로 평일 점검표가 완성됩니다.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox("연도 선택", range(2024, 2031), index=2) 
with col2:
    selected_month = st.selectbox("월 선택", range(1, 13), index=2)

if st.button("점검표 생성하기", type="primary", width="stretch"):
    with st.spinner('달력을 분석하고 문서를 작성 중입니다...'):
        generated_img = create_monthly_checklist(selected_year, selected_month)
        
        if generated_img:
            st.success(f"{selected_year}년 {selected_month}월 안전점검표가 성공적으로 생성되었습니다!")
            
            buf = io.BytesIO()
            generated_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.image(generated_img, caption=f"{selected_year}년 {selected_month}월 일일점검표", width="stretch")
            
            file_name = f"{selected_year}년_{selected_month}월_안전관리일일점검표_추부건.png"
            
            st.download_button(
                label="📥 완성된 점검표 다운로드 (PNG)",
                data=byte_im,
                file_name=file_name,
                mime="image/png",
                width="stretch"

            )

