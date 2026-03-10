import os
import random
from PIL import Image, ImageDraw

def generate_signatures(output_dir="signatures", count=50):
    # 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        img_size = 60
        # 투명한 배경의 캔버스 생성
        img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 1. 포인트 설정 (첨부된 이미지의 위로 뻗는 사선 형태 참고)
        # 시작점 (좌측 하단)
        x0 = random.uniform(15, 25)
        y0 = random.uniform(40, 50)
        
        # 끝점 (우측 상단)
        x2 = random.uniform(35, 45)
        y2 = random.uniform(10, 20)
        
        # 제어점 (곡선의 휘어짐 방향과 정도를 결정 - 살짝 아래쪽으로 휘게 설정)
        x1 = random.uniform(25, 35)
        y1 = random.uniform(30, 45)
        
        points = []
        num_steps = 30 # 곡선을 얼마나 부드럽게 그릴지 결정
        
        for step in range(num_steps + 1):
            t = step / num_steps
            
            # 2차 베지에 곡선(Quadratic Bezier Curve) 공식 적용
            bx = (1 - t)**2 * x0 + 2 * (1 - t) * t * x1 + t**2 * x2
            by = (1 - t)**2 * y0 + 2 * (1 - t) * t * y1 + t**2 * y2
            
            # 자연스러운 펜의 미세한 떨림(노이즈) 추가
            noise_x = random.uniform(-0.5, 0.5)
            noise_y = random.uniform(-0.5, 0.5)
            
            points.append((bx + noise_x, by + noise_y))
            
        # 2. 펜 속성 설정
        line_width = random.choice([2, 3]) # 펜 굵기 무작위
        alpha = random.randint(180, 255)   # 잉크 농도(투명도) 무작위
        
        # 3. 선 그리기
        draw.line(points, fill=(0, 0, 0, alpha), width=line_width, joint="curve")
        
        # 4. 파일 저장
        filename = f'signature_{i+1:02d}.png'
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        
    print(f"'{output_dir}' 폴더에 {count}개의 서명 이미지가 성공적으로 생성되었습니다!")

# 함수 실행
generate_signatures()