# This is the port of MMDVM to Linux

In order to play with this very experimental software:

Clone also my github with the modified MMDVM branch "no_due" and build it as usual

Install gnuradio 3.7 and gr-osmosdr



Connect your RTLSDR and HackRF, the code uses 431.875000 Mhz, configure your handheld.

Adjust the HackRF Id to your Id in linux/grc/dmr_trx_rtl_hackrf.py , otherwise transmit may not work.

Modify your MMDVM.ini to use "/opt/dmr/serialIn" as modem port !

# Create 4 Fifos

mkdir -p /opt/dmr
mkfifo /opt/dmr/sampRX
mkfifo /opt/dmr/sampTX
mkfifo /opt/dmr/serialIn
mkfifo /opt/dmr/serialOut

#build the linux port

cd linux
make

# Now start the components in the order shown below
# Best use 3 terminals  (path is "<MMDVMGitDir>/linux" in all terminals)

# Terminal 1
python grc/dmr_trx_rtl_hackrf.py 

#Terminal 2
./main 

#Terminal 3
../../MMDVMHost <whereisthechanged MMDVM.ini>


If you are lucky, you should be able to transmit and MMDVM sees your transmission
If you are even more lucky, you will here the response from the network.
For the first test with DMR I recommend to try RX without a connection to the network
Anything but DMR is not tested. 

Have fun, Danilo DB4PLE
