import pyshark
import os


pcap_file = 'output.pcap'


output_dir = 'udp_payloads'
os.makedirs(output_dir, exist_ok=True)


threshold_size = 1875

def save_payload(payload, index):
    file_path = os.path.join(output_dir, f'payload_{index}.bin')
    with open(file_path, 'wb') as f:
        f.write(payload)
    print(f"Saved payload to {file_path}")

def extract_large_udp_payloads(pcap_file):

    cap = pyshark.FileCapture(pcap_file, display_filter='udp')
    
    index = 0
    for packet in cap:
        try:

            if hasattr(packet.udp, 'payload'):
                payload_hex = packet.udp.payload.replace(':', '')
                payload = bytes.fromhex(payload_hex)


                if len(payload) > threshold_size:
                    save_payload(payload, index)
                    index += 1
        except Exception as e:
            print(f"Error processing packet: {e}")

    cap.close()

if __name__ == '__main__':
    extract_large_udp_payloads(pcap_file)
