import cv2
import numpy as np
import serial
import time

# Mở cổng UART (thay đổi '/dev/ttyUSB0' thành cổng UART thích hợp trên máy tính của bạn)
ser = serial.Serial('COM5', baudrate=115200, timeout=0)

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Tọa độ ban đầu của hình vuông màu đỏ
square_x, square_y = 100, 100

# Biến để kiểm tra xem phím 'f' đã được nhấn hay chưa
draw_rectangle = False

while True:
    oke = False
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    
    # Chuyển đổi khung hình sang định dạng grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Áp dụng phép lọc Gaussian để làm mờ ảnh và loại bỏ nhiễu
    blurred_frame = cv2.GaussianBlur(binary_image, (5, 5), 0)

    # Sử dụng phương pháp HoughCircles để nhận diện các hình tròn trong khung hình
    circles = cv2.HoughCircles(blurred_frame, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=50)

    if circles is not None:
        # Chuyển đổi tọa độ và bán kính của các hình tròn sang số nguyên
        circles = np.round(circles[0, :]).astype("int")

        # Vẽ các hình tròn được nhận diện lên khung hình gốc
        for (x, y, r) in circles:
            # Kiểm tra kích thước bán kính của hình tròn, bỏ qua nếu nhỏ hơn một ngưỡng nào đó
            if r > 20:  # Thay đổi giá trị ngưỡng tùy theo yêu cầu của bạn
                #xác định là có hình tròn hợp lệ
                oke = True
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)  # Màu xanh lá cây, độ dày viền là 4
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)  # Vẽ điểm tâm
                
                # Tính toán tọa độ tâm của hình vuông màu đỏ
                square_center_x = square_x + 5
                square_center_y = square_y + 5

                # Tính toán khoảng cách giữa tâm hình tròn và tâm hình vuông
                distance_x = x - square_center_x
                distance_y = y - square_center_y

                 # Chuỗi khoảng cách để gửi đi
                distance_str = f"{distance_x}x{distance_y}\n"  # Ví dụ: "100,-50\n"

                 # Gửi chuỗi khoảng cách qua UART
                ser.write(distance_str.encode())

                # In ra màn hình khoảng cách giữa tâm hình tròn và tâm hình vuông
                # print("toa do hinh tron:", distance_str)

        if oke == False:
            print("khong nhan dien duoc")
            ser.write(b"no\n")

    # Vẽ hình vuông màu đỏ
    cv2.rectangle(frame, (square_x, square_y), (square_x + 10, square_y + 10), (0, 0, 255), -1)

    # Nếu phím 'f' được nhấn, vẽ một hình chữ nhật 200x200px từ tọa độ của hình vuông
    if draw_rectangle:
        cv2.rectangle(frame, (square_x, square_y), (square_x + 400, square_y + 400), (0, 0, 255), 2)

    # Hiển thị khung hình gốc và khung hình sau khi nhận diện hình tròn
    cv2.imshow("Camera", frame)

    # Đọc dữ liệu từ UART
    if ser.in_waiting > 0:
        uart_data = ser.readline().decode().strip()
        print("Received from Arduino:", uart_data)
    
    # Bắt sự kiện phím bấm
    key = cv2.waitKey(1)
    
    # Di chuyển hình vuông
    if key == ord('w'):
        square_y -= 5
    elif key == ord('s'):
        square_y += 5
    elif key == ord('a'):
        square_x -= 5
    elif key == ord('d'):
        square_x += 5
    
    # Nếu phím 'f' được nhấn, chuyển đổi trạng thái của biến draw_rectangle
    if key == ord('f'):
        draw_rectangle = not draw_rectangle
    
    # Thoát khỏi vòng lặp khi nhấn phím 'q'
    if key & 0xFF == ord('q'):
        break

# Đóng cổng UART khi không sử dụng nữa
ser.close()
# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
