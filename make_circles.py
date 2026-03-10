from PIL import Image, ImageDraw
import random
import math
import os

def generate_handdrawn_circles(output_dir="circles", count=50):
    # 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        # 60x60 픽셀의 투명한 배경 이미지 생성
        img_size = 60
        img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 중심점 및 반지름 설정 (약간의 타원형을 위해 rx, ry 다르게 설정 가능)
        cx, cy = img_size / 2, img_size / 2
        rx = random.uniform(16, 22)
        ry = random.uniform(16, 22)
        
        # 사람이 직접 그리는 느낌을 위해 시작 각도와 끝 각도를 랜덤하게 설정 (약간 덜 닫히거나 겹치게)
        start_angle = random.uniform(0, 2 * math.pi)
        end_angle = start_angle + 2 * math.pi + random.uniform(-0.3, 0.4)
        
        num_steps = 100
        points = []
        
        for step in range(num_steps):
            t = start_angle + (end_angle - start_angle) * (step / num_steps)
            
            # 펜의 미세한 떨림(노이즈) 추가
            noise_x = random.uniform(-1.0, 1.0)
            noise_y = random.uniform(-1.0, 1.0)
            
            x = cx + rx * math.cos(t) + noise_x
            y = cy + ry * math.sin(t) + noise_y
            points.append((x, y))
            
        # 선 굵기와 색상 (검은색, 투명도 200~255 사이) 설정
        line_width = random.choice([2, 3])
        alpha = random.randint(200, 255)
        
        # 계산된 점들을 이어 부드러운 곡선 그리기
        draw.line(points, fill=(0, 0, 0, alpha), width=line_width, joint="curve")
        
        # 파일 저장 (예: circle_01.png, circle_02.png ...)
        filename = f'circle_{i+1:02d}.png'
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        
    print(f"'{output_dir}' 폴더에 {count}개의 개별 동그라미 이미지가 성공적으로 생성되었습니다!")

# 함수 실행
generate_handdrawn_circles()