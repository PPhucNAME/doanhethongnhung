#include "ringbuffer.h"

void RingBuffer_Init(RingBuffer_Types *Queue, uint32_t *buffer, int size) {
    Queue->Front = -1;
    Queue->Rear = -1;
    Queue->Size = size;
    Queue->Queuearr = buffer;
}

uint8_t BufferIsFull(RingBuffer_Types *Queue) {
    return ((Queue->Front == Queue->Rear + 1) || (Queue->Front == 0 && Queue->Rear == Queue->Size - 1));
}

uint8_t BufferIsEmpty(RingBuffer_Types *Queue) {
    return (Queue->Front == -1);
}

void RingBuffer_Pushdata(RingBuffer_Types *Queue, int data) {
    if (!BufferIsFull(Queue)) {
        if (Queue->Front == -1) {
            Queue->Front = 0;
        }
        Queue->Rear = (Queue->Rear + 1) % Queue->Size;
        Queue->Queuearr[Queue->Rear] = data;
    }
}

uint32_t RingBuffer_Popdata(RingBuffer_Types *Queue) {
    uint32_t data_out = 0; // Mặc định trả về 0 nếu hàng đợi rỗng
    if (!BufferIsEmpty(Queue)) {
        data_out = Queue->Queuearr[Queue->Front];
        if (Queue->Front == Queue->Rear) {
            Queue->Front = -1;
            Queue->Rear = -1;
        } else {
            Queue->Front = (Queue->Front + 1) % Queue->Size;
        }
    }
    return data_out;
}
