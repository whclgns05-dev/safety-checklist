import tkinter as tk
from PIL import Image, ImageTk

print("==================================================")
print("이미지 창이 열리면, 점검표 칸의 '정중앙'을 클릭하세요!")
print("클릭할 때마다 터미널에 X, Y 좌표가 출력됩니다.")
print("==================================================\n")

def on_click(event):
    x, y = event.x, event.y
    print(f"📍 클릭한 좌표 -> X: {x}, Y: {y}")
    # 클릭한 위치에 빨간 점을 찍어 시각적으로 확인
    canvas.create_oval(x-3, y-3, x+3, y+3, fill='red', outline='red')

# 프로그램 창 생성
root = tk.Tk()
root.title("안전점검표 좌표 추출기 (원하는 곳을 클릭하세요)")

# 이미지 파일 불러오기 (이름이 다르면 수정하세요)
image_path = "image_3e5ff8.png" 
try:
    img = Image.open(image_path)
except Exception as e:
    print(f"이미지를 찾을 수 없습니다: {e}")
    root.destroy()
    exit()

tk_image = ImageTk.PhotoImage(img)

# 캔버스(도화지) 설정 및 이미지 배치
canvas = tk.Canvas(root, width=img.width, height=img.height)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=tk_image)

# 마우스 왼쪽 버튼 클릭 시 on_click 함수 실행
canvas.bind("<Button-1>", on_click)

root.mainloop()