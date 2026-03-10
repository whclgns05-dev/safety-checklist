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
def create_monthly_checklist(year, month, dept, lab, loc):
    base_image_path = "image_3e5ff8.png"  
    
    # ---------------------------------------------------------
    # 📍 [필수 수정] 새로 추가된 텍스트 입력 좌표 (찾으신 좌표로 변경하세요!)
    # ---------------------------------------------------------
    coord_dept = (1049, 105) # '소속' 글자를 쓸 시작 X, Y 좌표 
    coord_lab = (1049, 125)  # '연구실명' 글자를 쓸 시작 X, Y 좌표 
    coord_loc = (1049, 144) # '위치' 글자를 쓸 시작 X, Y 좌표 
    # ---------------------------------------------------------

    circle_x_list = [
        506, 550, 598, 641, 685, 728, 766, 807, 841, 876, 
        916, 954, 988, 1027, 1062, 1097, 1133, 1174, 1210, 1246, 
        1282, 1317, 1355, 1389, 1428, 1464, 1504, 1538, 1579, 1611, 
        1653
    ]

    circle_y_list = [
        216, 241, 265, 291, 316, 351, 371, 391, 
        421, 441, 466, 491, 516, 541, 566, 591, 
        616, 641, 666, 709, 741, 766, 791, 816, 841, 866
    ]
    sign_y_list = [994, 1030] 
    
    circle_size = (16, 16) 
    sign_size = (30, 30)   

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

    circles = load_images("circles", circle_size)
    signs_inspector = load_images("signatures", sign_size)          
    signs_manager = load_images("signatures_complex", sign_size)    

    if not circles or not signs_inspector or not signs_manager:
        st.error("오류: 서명 또는 동그라미 폴더의 이미지를 찾을 수 없습니다.")
        return None

    result_img = base_img.copy()
    draw = ImageDraw.Draw(result_img)
    
    # 기존 연도/월 지우기 영역
    draw.rectangle([(658, 47), (808, 88)], fill="white") 
    draw.rectangle([(827, 47), (897, 88)], fill="white") 
    draw.rectangle([(1049, 105), (1400, 161)], fill="white") 
    
    # 폰트 설정
    try:
        font_title = ImageFont.truetype("MALGUN.TTF", 36) # 연도/월 폰트
        font_info = ImageFont.truetype("MALGUN.TTF", 10)  # 소속/연구실명 폰트 
    except IOError:
        font_title = ImageFont.load_default()
        font_info = ImageFont.load_default()
        
    # 1. 연도/월 쓰기
    draw.text((668, 47), f"{year}년도", font=font_title, fill="black")
    draw.text((837, 47), f"{month}월", font=font_title, fill="black")
    
    # 2. 웹에서 입력받은 소속, 연구실명, 위치 쓰기
    draw.text(coord_dept, dept, font=font_info, fill="black")
    draw.text(coord_lab, lab, font=font_info, fill="black")
    draw.text(coord_loc, loc, font=font_info, fill="black")

    # 평일에만 동그라미 및 서명 찍기
    for day in valid_days:
        current_x = circle_x_list[day - 1]
        
        for y in circle_y_list:
            circle_img = random.choice(circles)
            paste_x = current_x - (circle_size[0] // 2) + random.randint(-2, 2)
            paste_y = y - (circle_size[1] // 2) + random.randint(-2, 2)
            result_img.paste(circle_img, (paste_x, paste_y), circle_img)

        inspector_img = random.choice(signs_inspector)
        paste_x_insp = current_x - (sign_size[0] // 2) + random.randint(-2, 2)
        paste_y_insp = sign_y_list[0] - (sign_size[1] // 2) + random.randint(-2, 2)
        result_img.paste(inspector_img, (paste_x_insp, paste_y_insp), inspector_img)

        manager_img = random.choice(signs_manager)
        paste_x_mgr = current_x - (sign_size[0] // 2) + random.randint(-2, 2)
        paste_y_mgr = sign_y_list[1] - (sign_size[1] // 2) + random.randint(-2, 2)
        result_img.paste(manager_img, (paste_x_mgr, paste_y_mgr), manager_img)

    final_img = Image.new("RGB", result_img.size, (255, 255, 255))
    final_img.paste(result_img, mask=result_img.split()[3])
    
    return final_img

# -------------------------------------------------------------------------
# 2. Streamlit 웹 UI 구성
# -------------------------------------------------------------------------
st.set_page_config(page_title="연구실 안전관리 점검표 자동화", layout="centered")

st.title("📝 연구실 안전관리 일일점검표 자동 생성기")
st.write("담당자: **추부건** | 문서 정보와 날짜를 입력하면 점검표가 자동으로 완성됩니다.")
st.markdown("---")

# 연구실 정보 입력 칸 
st.subheader("🏢 연구실 정보 입력")
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    input_dept = st.text_input("소속", value="양자변환연구단")
with col_info2:
    input_lab = st.text_input("연구실명", value="111-1")
with col_info3:
    input_loc = st.text_input("위치", value="중앙기기연구소")

st.markdown("---")

# 연도/월 선택 칸 
st.subheader("📅 점검 일자 선택")
col_date1, col_date2 = st.columns(2)
with col_date1:
    selected_year = st.selectbox("연도 선택", range(2024, 2031), index=2) 
with col_date2:
    selected_month = st.selectbox("월 선택", range(1, 13), index=2)

if st.button("점검표 생성하기", type="primary", width="stretch"):
    with st.spinner('달력을 분석하고 문서를 작성 중입니다...'):
        generated_img = create_monthly_checklist(selected_year, selected_month, input_dept, input_lab, input_loc)
        
        if generated_img:
            st.success("안전점검표가 성공적으로 생성되었습니다!")
            
            buf = io.BytesIO()
            generated_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.image(generated_img, caption="완성된 일일점검표", width="stretch")
            
            file_name = f"{selected_year}년_{selected_month}월_{input_lab}_안전점검표_추부건.png"
            
            st.download_button(
                label="📥 완성된 점검표 다운로드 (PNG)",
                data=byte_im,
                file_name=file_name,
                mime="image/png",
                width="stretch"
            )



