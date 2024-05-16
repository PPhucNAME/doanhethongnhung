#ifndef _RING_BUFFER_H_
#define _RING_BUFFER_H_

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    int8_t Front, Rear, Size;
    uint32_t *Queuearr;
} RingBuffer_Types;

void RingBuffer_Init(RingBuffer_Types *Queue, uint32_t *buffer, int size);
uint8_t BufferIsFull(RingBuffer_Types *Queue);
uint8_t BufferIsEmpty(RingBuffer_Types *Queue);
void RingBuffer_Pushdata(RingBuffer_Types *Queue, int data);
uint32_t RingBuffer_Popdata(RingBuffer_Types *Queue);

#endif /* _RING_BUFFER_H_ */
