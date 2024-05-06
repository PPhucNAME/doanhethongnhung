import cv2
import numpy as np

# Khởi tạo camera
cap = cv2.VideoCapture(0)

while True:
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    
    # Chuyển đổi khung hình sang định dạng grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp dụng phép lọc Gaussian để làm mờ ảnh và loại bỏ nhiễu
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Sử dụng phương pháp HoughCircles để nhận diện các hình tròn trong khung hình
    circles = cv2.HoughCircles(blurred_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=50)

    if circles is not None:
        # Chuyển đổi tọa độ và bán kính của các hình tròn sang số nguyên
        circles = np.round(circles[0, :]).astype("int")

        # Vẽ các hình tròn được nhận diện lên khung hình gốc
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)  # Màu xanh lá cây, độ dày viền là 4
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)  # Vẽ điểm tâm

    # Hiển thị khung hình gốc và khung hình sau khi nhận diện hình tròn
    cv2.imshow("Camera", frame)
    
    # Thoát khỏi vòng lặp khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
