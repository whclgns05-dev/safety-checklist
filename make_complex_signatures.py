import os
import random
from PIL import Image, ImageDraw

def smooth_line(points, iterations=4):
    """거친 기준점들을 연결하여 부드러운 펜글씨 곡선으로 만들어주는 함수"""
    for _ in range(iterations):
        smoothed = []
        smoothed.append(points[0])
        for i in range(len(points)-1):
            p0 = points[i]
            p1 = points[i+1]
            q = (0.75*p0[0] + 0.25*p1[0], 0.75*p0[1] + 0.25*p1[1])
            r = (0.25*p0[0] + 0.75*p1[0], 0.25*p0[1] + 0.75*p1[1])
            smoothed.extend([q, r])
        smoothed.append(points[-1])
        points = smoothed
    return points

def generate_complex_signatures(output_dir="signatures_complex", count=50):
    # 폴더 생성
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(count):
        img_size = 60
        # 투명 배경 캔버스
        img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 1. 서명 뼈대(몸통) 기준점 무작위 생성 (지그재그 후 아래로 큰 루프)
        body_anchors = [
            (random.uniform(5, 12), random.uniform(20, 28)),   # 시작점 (좌측 상단)
            (random.uniform(12, 18), random.uniform(28, 35)),  # 아래로 꺾임
            (random.uniform(15, 22), random.uniform(15, 22)),  # 위로 꺾임 (뾰족한 부분)
            (random.uniform(22, 28), random.uniform(22, 28)),  # 다시 아래로
            (random.uniform(18, 25), random.uniform(45, 55)),  # 큰 루프의 가장 아래쪽
            (random.uniform(32, 40), random.uniform(45, 52)),  # 큰 루프의 우측 하단
            (random.uniform(28, 35), random.uniform(28, 35))   # 루프가 끝나는 지점
        ]
        
        # 2. 서명 가로지르는 사선 기준점 무작위 생성
        slash_anchors = [
            (random.uniform(10, 18), random.uniform(35, 45)),  # 사선 시작 (좌측 하단)
            (random.uniform(30, 35), random.uniform(25, 30)),  # 사선 중간 (살짝 휘어짐)
            (random.uniform(48, 55), random.uniform(10, 18))   # 사선 끝 (우측 상단)
        ]
        
        # 3. 기준점들을 부드러운 곡선으로 변환
        body_points = smooth_line(body_anchors)
        slash_points = smooth_line(slash_anchors)
        
        # 4. 펜 속성 (굵기 및 잉크 농도 무작위)
        line_width = random.choice([2, 3])
        alpha = random.randint(180, 255)
        color = (0, 0, 0, alpha)
        
        # 5. 선 그리기
        draw.line(body_points, fill=color, width=line_width, joint="curve")
        draw.line(slash_points, fill=color, width=line_width, joint="curve")
        
        # 6. 파일 저장
        filename = f'signature_{i+1:02d}.png'
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        
    print(f"'{output_dir}' 폴더에 {count}개의 복잡한 형태의 서명 이미지가 생성되었습니다!")

# 실행
if __name__ == "__main__":
    generate_complex_signatures()