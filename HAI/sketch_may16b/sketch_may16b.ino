#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <ESP32Servo.h>
#include "ringbuffer.h"


#define BUFFER_SIZE 128

typedef struct {
    int x; 
    int y; 
} Position;

Position buffer[BUFFER_SIZE];
volatile uint8_t head = 0;
volatile uint8_t tail = 0;
volatile uint8_t size = 0;

Servo servo1;
Servo servo2;

TaskHandle_t UART; 
TaskHandle_t CONTROLL;  

void enqueue(Position pos) {
    buffer[head] = pos;
    head = (head + 1) % BUFFER_SIZE;

    if (size < BUFFER_SIZE) {
        size++;
    } else {
        tail = (tail + 1) % BUFFER_SIZE; // Ghi đè lên phần tử cũ nhất
    }
}

Position dequeue() {
    Position pos = {0, 0}; // Giá trị mặc định nếu buffer rỗng
    if (size > 0) {
        pos = buffer[tail];
        tail = (tail + 1) % BUFFER_SIZE;
        size--;
    }
    return pos;
}

void TaskUart(void * parameter);
void TaskControll(void * parameter);

void setup() 
{ 
    Serial.begin(115200); 
    pinMode(16, OUTPUT);
    pinMode(17, OUTPUT);  
    servo1.attach(16);
    servo2.attach(17);
    
    xTaskCreatePinnedToCore(TaskUart, "Task1", 10000, NULL, 1, &UART, 0);  
    delay(500);   
    xTaskCreatePinnedToCore(TaskControll, "Task2", 10000, NULL, 1, &CONTROLL, 1);  
    delay(500); 
}  

void TaskUart(void * parameter)
{
    while (1) {
        if (Serial.available() > 0) {
            String input = Serial.readStringUntil('\n');
            // Tách chuỗi thành phần x và y
            int separatorIndex = input.indexOf('x');
            if (separatorIndex != -1) { // Kiểm tra xem có ký tự phân tách 'x' trong chuỗi không
                String x_str = input.substring(0, separatorIndex); // Lấy phần từ đầu đến 'x'
                String y_str = input.substring(separatorIndex + 1); // Lấy phần sau 'x'
                Position pos;
                pos.x = x_str.toInt(); // Chuyển đổi phần x từ String sang int
                pos.y = y_str.toInt(); // Chuyển đổi phần y từ String sang int
                enqueue(pos); // Thêm dữ liệu vào buffer
                // In ra tọa độ x và y
                Serial.print("Toa do x: ");
                Serial.println(pos.x);
                Serial.print("Toa do y: ");
                Serial.println(pos.y);
            }
            vTaskDelay(100 / portTICK_PERIOD_MS); 
        }
    }
}

void TaskControll(void * parameter)
{ 
    while (1) { 

        }
        vTaskDelay(100 / portTICK_PERIOD_MS);  
    }
}  

void loop() 
{ 
    // Không cần xử lý gì trong hàm loop
}
