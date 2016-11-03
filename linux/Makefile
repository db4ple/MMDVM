VPATH=..
SRCS=CalDMR.cpp      CalDStarTX.cpp  DMRDMORX.cpp  DMRIdleRX.cpp  DMRSlotRX.cpp    DMRTX.cpp    DStarTX.cpp  MMDVM.cpp  P25TX.cpp     SerialPort.cpp  Utils.cpp  YSFTX.cpp CalDStarRX.cpp  CWIdTX.cpp      DMRDMOTX.cpp  DMRRX.cpp      DMRSlotType.cpp  DStarRX.cpp  IO.cpp       P25RX.cpp  SampleRB.cpp  SerialRB.cpp    YSFRX.cpp MMDVM.cpp IOPc.cpp RSSIRB.cpp

OBJS=CalDMR.o      CalDStarTX.o  DMRDMORX.o  DMRIdleRX.o  DMRSlotRX.o    DMRTX.o    DStarTX.o  MMDVM.o  P25TX.o     SerialPort.o  Utils.o  YSFTX.o CalDStarRX.o  CWIdTX.o      DMRDMOTX.o  DMRRX.o      DMRSlotType.o  DStarRX.o  IO.o       P25RX.o  SampleRB.o  SerialRB.o    YSFRX.o main.o arm_fir_fast_q15.o IOPc.o RSSIRB.o SerialPC.o

CC=g++
CXXFLAGS=-I. -std=gnu++11 -D__PC__ -g
main: $(OBJS)


clean:
	@rm -f $(OBJS)
