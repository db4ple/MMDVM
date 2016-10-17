/*
 *   Copyright (C) 2015,2016 by Jonathan Naylor G4KLX
 *   Copyright (C) 2015 by Jim Mclaughlin KI6ZUM
 *   Copyright (C) 2016 by Colin Durbridge G4EML
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include "Config.h"
#include "Globals.h"
#include "IO.h"

#if defined(__PC__)
#include "Arduino.h"
#include <sys/ioctl.h>
#include <unistd.h>
#include <fcntl.h>

#define PIN_COS                0  // D5
#define PIN_PTT                1  // D7
#define PIN_COSLED             2 // D6
#define PIN_ADC                3  // A0
#define PIN_DAC                4  // A2
#define PIN_DSTAR 5
#define PIN_DMR 6
#define PIN_YSF 7
#define PIN_P25 8

const uint16_t DC_OFFSET = 2048U;

int sampTxFd;
int sampRxFd;
fd_set m_txFds;
fd_set m_rxFds;
struct timeval m_txTv;
struct timeval m_rxTv;


extern "C" {
  void ADC_Handler()
  {
      // io.interrupt();
  }
}

void CIO::initInt()
{
  int pipeSize = 4096;

  sampTxFd = ::open("/opt/dmr/sampTX",O_WRONLY|O_CREAT,0666);
  sampRxFd = ::open("/opt/dmr/sampRX",O_RDONLY);

  fcntl(sampTxFd,F_SETPIPE_SZ,pipeSize); 
  fcntl(sampRxFd,F_SETPIPE_SZ,pipeSize); 

  // remove too much data from pipe
  {
    int nBytes = 0;
    ioctl(sampRxFd, FIONREAD, &nBytes);  
    if (nBytes > 2048)
    {
	printf("Too much data in pipe: %d\n",nBytes);
	char dummy[nBytes];
	size_t readBytes = nBytes - 2048; 
	size_t done;
	while ((done = read(sampRxFd,dummy,readBytes))>0) 
	{ 
		readBytes -= done; 
		if (readBytes == 0) break; 
	}
    }
  }
  fcntl(sampRxFd,F_SETPIPE_SZ,pipeSize); 

  // Set up the TX, COS and LED pins
  pinMode(PIN_PTT,    OUTPUT);
  pinMode(PIN_COSLED, OUTPUT);
  pinMode(PIN_LED,    OUTPUT);
  pinMode(PIN_COS,    INPUT);

#if defined(ARDUINO_MODE_PINS)
  // Set up the mode output pins
  pinMode(PIN_DSTAR,  OUTPUT);
  pinMode(PIN_DMR,    OUTPUT);
  pinMode(PIN_YSF,    OUTPUT);
  pinMode(PIN_P25,    OUTPUT);
#endif
}

void CIO::startInt()
{

  digitalWrite(PIN_PTT, m_pttInvert ? HIGH : LOW);
  digitalWrite(PIN_COSLED, LOW);
  digitalWrite(PIN_LED,    HIGH);
}

void CIO::interrupt()
{
  uint8_t control = MARK_NONE;
  int16_t sample = DC_OFFSET;

  m_txBuffer.get((uint16_t&)sample, control);

  FD_ZERO(&m_txFds);
  FD_SET(sampTxFd, &m_txFds);

  m_txTv.tv_sec  = 0;
  m_txTv.tv_usec = 0;
   if (1 || m_tx)
   {
	sample -= DC_OFFSET;
   	// if  (::select(sampTxFd + 1, NULL, &m_txFds, NULL, &m_txTv) > 0)
        {
		::write(sampTxFd,&sample,2);
        }
   }
  FD_ZERO(&m_rxFds);
  FD_SET(sampRxFd, &m_rxFds);

  m_rxTv.tv_sec  = 0;
  m_rxTv.tv_usec = 0;
	static int32_t accu = 0;
        static int counter = 0;
        static bool first_read = true;
   sample = 0;
   if  (::select(sampRxFd + 1, &m_rxFds, NULL, NULL, &m_rxTv) > 0)
   {
	// printf("seek 0\n");
   	int res = ::read(sampRxFd,&sample,2);
	// printf("seek 1\n");
   	if (res < 2) 
   	{
		// printf("seek 0\n");
		// ::lseek(sampRxFd, 0, SEEK_SET);
		// simple loop to the back;
		sample = 0;
   	}
	if (first_read && sample != 0)
	{
		first_read = false;
	}

   } 
   accu += sample;
   counter++;
   if (counter == 24000) 
   {
	printf("avg: %d\n",accu/24000);	
	accu = counter = 0;
   }
   if (m_tx)  
   {
	// since we have separate receiver at same frequency, we kill the signal here
	sample = 0;
   }
   sample += DC_OFFSET;

  if (!first_read)
  {
      m_rxBuffer.put(sample, control);
  }

  m_rssiBuffer.put(0U);

  m_watchdog++;
}

bool CIO::getCOSInt()
{
  return digitalRead(PIN_COS) == HIGH;
}

void CIO::setLEDInt(bool on)
{
  digitalWrite(PIN_LED, on ? HIGH : LOW);
}

void CIO::setPTTInt(bool on)
{
  digitalWrite(PIN_PTT, on ? HIGH : LOW);
}

void CIO::setCOSInt(bool on)
{
  digitalWrite(PIN_COSLED, on ? HIGH : LOW);
}

void CIO::setDStarInt(bool on)
{
  digitalWrite(PIN_DSTAR, on ? HIGH : LOW);
}

void CIO::setDMRInt(bool on) 
{
  digitalWrite(PIN_DMR, on ? HIGH : LOW);
}

void CIO::setYSFInt(bool on)
{
  digitalWrite(PIN_YSF, on ? HIGH : LOW);
}

void CIO::setP25Int(bool on) 
{
  digitalWrite(PIN_P25, on ? HIGH : LOW);
}

#endif

