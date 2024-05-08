import cv2
import numpy as np
''' 
import serial.serialutil  # Import module serialutil từ thư viện serial
import time

# Thiết lập thông số UART
ser = serial.serialutil.Serial('COM1', 9600) 
time.sleep(2)  # Đợi một chút để UART kết nối

# Gửi tọa độ hình tròn màu vàng qua UART
def send_yellow_circle_coord(x, y):
    data = f"X:{x},Y:{y}\n"  # Chuỗi dữ liệu có thể được định dạng theo ý muốn của bạn
    ser.write(data.encode())

'''
# Mở camera
cap = cv2.VideoCapture(0)

while True:
    # Đọc frame từ camera
    ret, frame = cap.read()

    # Chuyển đổi sang không gian màu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Định hình ngưỡng cho màu vàng
    lower_yellow = np.array([20, 150, 150])
    upper_yellow = np.array([30, 255, 255])

    # Tạo mask cho màu vàng
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Làm trơn mask để giảm nhiễu
    mask_yellow = cv2.GaussianBlur(mask_yellow, (15, 15), 0)

    # Tìm các contour trong mask màu vàng
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Biến kiểm tra có hình tròn màu vàng được phát hiện hay không
    yellow_circle_detected = False

    # Duyệt qua các contour màu vàng
    for contour in contours_yellow:
        # Tính toán moment của contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            # Tính tọa độ trung tâm của contour
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Vẽ hình tròn và tâm
            cv2.drawContours(frame, [contour], -1, (0, 255, 255), 2)
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(frame, f"({cX}, {cY})", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # In ra tọa độ trung tâm của hình tròn màu vàng
            print("Tọa độ trung tâm của hình tròn màu vàng:", (cX, cY))

            # Gửi tọa độ qua UART
            #send_yellow_circle_coord(cX, cY)

            # Đánh dấu đã phát hiện hình tròn màu vàng
            yellow_circle_detected = True

    # Nếu không phát hiện hình tròn màu vàng, in ra thông báo
    if not yellow_circle_detected:
        print("Không tìm thấy hình tròn màu vàng.")

    # Hiển thị frame
    cv2.imshow('Camera', frame)

    # Thoát khỏi vòng lặp nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()

# Đóng kết nối UART khi kết thúc
#ser.close()
