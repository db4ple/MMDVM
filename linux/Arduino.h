#ifndef AXX
#define AXX

#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

typedef int16_t q15_t;
typedef int32_t q31_t;
typedef float float32_t;

struct arm_fir_instance_q15 {
int numTaps;
q15_t* pState;
q15_t* pCoeffs;

};

#define __INLINE inline



void arm_fir_fast_q15(const arm_fir_instance_q15*, q15_t*, q15_t*, unsigned int);

class serialPort
{
	int inFd;
	int outFd;
public:
	void begin(int);
	bool available();
	size_t write(const uint8_t *, size_t length);
	int16_t read();
	void flush();
};

extern serialPort Serial;
extern serialPort Serial2;
extern serialPort Serial3;

extern void digitalWrite(...);
extern int digitalRead(...);
extern void pinMode(...);
extern void pinMode(...);
extern int __SSAT(int,int);
extern void loop();
extern void setup();

#define LOW 0
#define HIGH 1
#define OUTPUT 1
#define INPUT 0 

#define PIN_LED 0
#endif
