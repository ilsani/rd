#!/env/python
#
# Extract all sessions from a PCAP file.
#
import sys

from scapy.all import *

def main():
    try:

        if len(sys.argv) != 3:
            usage()
            sys.exit(-1)

        pcap_file = sys.argv[1]
        out_dir = sys.argv[2]
        
        pcap = rdpcap(pcap_file)

        sessions = pcap.sessions()
        for session_id, packets in sessions.iteritems():

            filename = session_id.replace(" ", "_")
            filename = filename.replace(">", "to")
            filename = filename.replace(":", "-")
            output_file = "%s/%s.pcap" %(out_dir, filename)

            wrpcap(output_file, packets)
        
    except Exception, e:
        print str(e)

def usage():
    print "%s <pcap> <output_dir>" %(sys.argv[0])

if __name__ == "__main__":
    main()
