void setup() {
  // Khởi tạo cổng Serial với tốc độ baudrate 115200
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) { // Kiểm tra xem có dữ liệu nào được gửi từ máy tính không
    String input = Serial.readStringUntil('\n'); // Đọc chuỗi từ Serial cho đến khi gặp ký tự newline (\n)
    
    // Tách chuỗi thành phần x và y
    int separatorIndex = input.indexOf('x');
    if (separatorIndex != -1) { // Kiểm tra xem có ký tự phân tách 'x' trong chuỗi không
      String x_str = input.substring(0, separatorIndex); // Lấy phần từ đầu đến 'x'
      String y_str = input.substring(separatorIndex + 1); // Lấy phần sau 'x'
      
      int x = x_str.toInt(); // Chuyển đổi phần x từ String sang int
      int y = y_str.toInt(); // Chuyển đổi phần y từ String sang int

      // In ra tọa độ x và y
      Serial.print("Toa do x: ");
      Serial.println(x);
      Serial.print("Toa do y: ");
      Serial.println(y);
    }
  }
}
