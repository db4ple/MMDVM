#include <Arduino.h>

int xmain()
{
	setup();
	while (1)
	{
		loop();
	}
}


bool serialPort::available()
{
	fd_set fds;
	FD_ZERO(&fds);
	FD_SET(inFd, &fds);

	int n;
	struct timeval tv;
	tv.tv_sec  = 0;
	tv.tv_usec = 400;

	n = ::select(inFd + 1, &fds, NULL, NULL, &tv);
	if (n > 0)
	{
		return 1;
	} else {
		return 0;
	}
}


	void serialPort::begin(int) { inFd = ::open("/tmp/serialIn", O_RDONLY); outFd = ::open("/tmp/serialOut", O_WRONLY); }
	size_t serialPort::write(const uint8_t* data, size_t length) { return ::write(outFd,data,length); }
	int16_t serialPort::read()
	{ 
		char c; 
		int16_t res = ::read(inFd,&c,1);
		if (res > 0)
		{
			res = c;
		}
		else
		{
			res = -1;
		}
	} 
	void serialPort::flush() {}

serialPort Serial;
serialPort Serial3;

void digitalWrite(...) {}
int digitalRead(...) { return 0; }
void pinMode(...) {}
int __SSAT(int v,int w) 
{
	int max;
	if (w<31)
	{
	 	if (v>=(1<<w))
		{
			v = (1<<w)-1;
		} else if (v<=-(1<<w)) {
			v = -(1<<w);
		}	
	}
	return v; 
}
