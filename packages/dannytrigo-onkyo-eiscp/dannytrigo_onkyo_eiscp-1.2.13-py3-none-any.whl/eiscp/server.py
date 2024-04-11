import socket
import eiscp
import eiscp.core
import socketserver
import threading
import logging
import sys

__info_response__ = r"""<?xml version="1.0" encoding="utf-8"?><response status="ok"><device id="TX-NR8100"><brand>ONKYO</brand><category>AV Receiver</category><year>2021</year><model>TX-NR8100</model><destination>Dx</destination><productid>2020_Onkyo_9_Channel_Network_A_V_Receiver</productid><deviceserial>0009B060B053</deviceserial><macaddress>0009B060B053</macaddress><modeliconurl>http://10.10.10.10/icon/OAVR_120.jpg</modeliconurl><friendlyname></friendlyname><firmwareversion>R126-0711-0170-0031-0000</firmwareversion><ecosystemversion>200</ecosystemversion><tidaloauthversion>2</tidaloauthversion><netservicelist count="13"><netservice id="0e" value="1" name="TuneIn Radio" account="Username" password="Password" zone="07" enable="07" /><netservice id="04" value="1" name="Pandora" account="Email" password="Password" zone="07" enable="07" /><netservice id="0a" value="1" name="Spotify" zone="07" enable="07" /><netservice id="12" value="1" name="Deezer" account="Email address" password="Password" zone="07" enable="07" /><netservice id="44" value="1" name="AirPlay" zone="07" enable="07" /><netservice id="1b" value="1" name="TIDAL" account="Username" password="Password" zone="07" enable="07" multipage="1" /><netservice id="00" value="1" name="Music Server" zone="07" enable="07" addqueue="1" sort="1" /><netservice id="f0" value="1" name="USB" zone="07" enable="07" addqueue="1" /><netservice id="40" value="1" name="Chromecast built-in" zone="07" enable="01" /><netservice id="1d" value="1" name="Play Queue" zone="07" enable="07" /><netservice id="42" value="1" name="DTS Play-Fi" zone="07" enable="01" /><netservice id="1c" value="1" name="Amazon Music" account="Username" password="Password" zone="07" enable="07" multipage="1" /><netservice id="45" value="1" name="Amazon Alexa" zone="07" enable="01" /></netservicelist><zonelist count="4"><zone id="1" value="1" name="Main" volmax="82" volstep="0" src="0" dst="0" lrselect="0" /><zone id="2" value="1" name="Zone2" volmax="82" volstep="0" src="0" dst="0" lrselect="0" /><zone id="3" value="1" name="Zone3" volmax="82" volstep="0" src="0" dst="0" lrselect="0" /><zone id="4" value="0" name="Zone4" volmax="0" volstep="0" src="0" dst="0" lrselect="0" /></zonelist><selectorlist count="14"><selector id="10" value="1" name="BD/DVD" zone="07" iconid="10" /><selector id="02" value="1" name="GAME" zone="07" iconid="02" /><selector id="01" value="1" name="CBL/SAT" zone="07" iconid="01" /><selector id="11" value="1" name="STRM BOX" zone="07" iconid="11" /><selector id="05" value="1" name="PC" zone="01" iconid="05" /><selector id="03" value="1" name="AUX" zone="07" iconid="03" /><selector id="23" value="1" name="CD" zone="07" iconid="47" /><selector id="12" value="1" name="TV" zone="07" iconid="12" /><selector id="22" value="1" name="PHONO" zone="07" iconid="22" /><selector id="25" value="1" name="AM" zone="07" iconid="25" /><selector id="24" value="1" name="FM" zone="07" iconid="24" /><selector id="2b" value="1" name="NET" zone="07" iconid="2b" /><selector id="2e" value="2" name="BLUETOOTH" zone="07" iconid="2e" /><selector id="80" value="1" name="Source" zone="06" /></selectorlist><presetlist count="40"><preset id="01" band="0" freq="0" name="" /><preset id="02" band="0" freq="0" name="" /><preset id="03" band="0" freq="0" name="" /><preset id="04" band="0" freq="0" name="" /><preset id="05" band="0" freq="0" name="" /><preset id="06" band="0" freq="0" name="" /><preset id="07" band="0" freq="0" name="" /><preset id="08" band="0" freq="0" name="" /><preset id="09" band="0" freq="0" name="" /><preset id="0a" band="0" freq="0" name="" /><preset id="0b" band="0" freq="0" name="" /><preset id="0c" band="0" freq="0" name="" /><preset id="0d" band="0" freq="0" name="" /><preset id="0e" band="0" freq="0" name="" /><preset id="0f" band="0" freq="0" name="" /><preset id="10" band="0" freq="0" name="" /><preset id="11" band="0" freq="0" name="" /><preset id="12" band="0" freq="0" name="" /><preset id="13" band="0" freq="0" name="" /><preset id="14" band="0" freq="0" name="" /><preset id="15" band="0" freq="0" name="" /><preset id="16" band="0" freq="0" name="" /><preset id="17" band="0" freq="0" name="" /><preset id="18" band="0" freq="0" name="" /><preset id="19" band="0" freq="0" name="" /><preset id="1a" band="0" freq="0" name="" /><preset id="1b" band="0" freq="0" name="" /><preset id="1c" band="0" freq="0" name="" /><preset id="1d" band="0" freq="0" name="" /><preset id="1e" band="0" freq="0" name="" /><preset id="1f" band="0" freq="0" name="" /><preset id="20" band="0" freq="0" name="" /><preset id="21" band="0" freq="0" name="" /><preset id="22" band="0" freq="0" name="" /><preset id="23" band="0" freq="0" name="" /><preset id="24" band="0" freq="0" name="" /><preset id="25" band="0" freq="0" name="" /><preset id="26" band="0" freq="0" name="" /><preset id="27" band="0" freq="0" name="" /><preset id="28" band="0" freq="0" name="" /></presetlist><controllist count="69"><control id="Bass" value="1" zone="1" min="-10" max="10" step="1" /><control id="Treble" value="1" zone="1" min="-10" max="10" step="1" /><control id="Center Level" value="1" zone="1" min="-12" max="12" step="0" /><control id="Subwoofer Level" value="1" zone="1" min="-15" max="12" step="0" /><control id="Subwoofer1 Level" value="0" zone="1" min="-15" max="12" step="0" /><control id="Subwoofer2 Level" value="0" zone="1" min="-15" max="12" step="0" /><control id="Phase Matching Bass" value="0" /><control id="LMD Movie/TV" value="1" code="MOVIE" position="1" /><control id="LMD Music" value="1" code="MUSIC" position="2" /><control id="LMD Game" value="1" code="GAME" position="3" /><control id="LMD THX" value="1" code="04" position="4" /><control id="LMD Stereo" value="0" code="00" position="4" /><control id="LMD Direct" value="0" code="01" position="1" /><control id="LMD Pure Audio" value="0" code="11" position="2" /><control id="LMD Pure Direct" value="0" code="11" position="1" /><control id="LMD Auto/Direct" value="0" code="AUTO" position="2" /><control id="LMD Stereo G" value="0" code="STEREO" position="3" /><control id="LMD Surround" value="0" code="SURR" position="4" /><control id="TUNER Control" value="1" /><control id="TUNER Freq Control" value="0" /><control id="Info" value="1" /><control id="Cursor" value="1" /><control id="Home" value="0" code="HOME" position="2" /><control id="Setup" value="1" code="MENU" position="2" /><control id="Quick" value="1" code="QUICK" position="1" /><control id="Menu" value="0" code="MENU" position="1" /><control id="AMP Control(RI)" value="0" /><control id="CD Control(RI)" value="0" /><control id="CD Control" value="0" /><control id="BD Control(CEC)" value="1" /><control id="TV Control(CEC)" value="1" /><control id="NoPowerButton" value="0" /><control id="DownSample" value="0" /><control id="Dimmer" value="1" /><control id="time_hhmmss" value="1" /><control id="Zone2 Control(CEC)" value="0" /><control id="Sub Control(CEC)" value="0" /><control id="NoNetworkStandby" value="0" /><control id="NJAREQ" value="1" /><control id="Music Optimizer" value="1" /><control id="NoVideoInfo" value="0" /><control id="NoAudioInfo" value="0" /><control id="AV Adjust" value="0" /><control id="Audio Scalar" value="0" /><control id="Hi-Bit" value="0" /><control id="Upsampling" value="0" /><control id="Digital Filter" value="0" /><control id="DolbyAtmos" value="1" /><control id="DTS:X" value="1" /><control id="MCACC" value="0" /><control id="Dialog Enhance" value="0" /><control id="PQLS" value="0" /><control id="CD Control(NewRemote)" value="0" /><control id="NoVolume" value="0" /><control id="Auto Sound Retriever" value="0" /><control id="Lock Range Adjust" value="0" /><control id="P.BASS" value="0" /><control id="Tone Direct" value="0" /><control id="DetailedFileInfo" value="1" /><control id="NoDABPresetFunc" value="1" /><control id="S.BASS" value="0" /><control id="MyInput/PersonalPreset" value="0" max="0" /><control id="Vocal/Dialog" value="1" min="0" max="5" step="1" /><control id="StereoAssignMode" value="1" /><control id="CinemaDedicatedMode/AVDirectMode" value="0" /><control id="HDMIOUT Sub" value="1" /><control id="HDMIOUT Zone2" value="1" /><control id="UI Status" value="1" /><control id="Dirac" value="1" port="60229" /></controllist><functionlist count="11"><function id="UsbUpdate" value="0" /><function id="NetUpdate" value="1" /><function id="WebSetup" value="1" /><function id="WifiSetup" value="1" /><function id="Nettune" value="0" /><function id="Initialize" value="0" /><function id="Battery" value="0" /><function id="AutoStandbySetting" value="0" /><function id="e-onkyo" value="0" /><function id="UsbDabDongle" value="0" /><function id="PlayQueue" value="1" /></functionlist><tuners count="2"><tuner band="FM" min="87500" max="107900" step="200" /><tuner band="AM" min="530" max="1710" step="10" /></tuners></device></response>"""
__mdi_response__ = r"""<?xml version="1.0"?><mdi><deviceid>0009B060B053</deviceid><netstandby>1</netstandby><currentversion>0</currentversion><zonelist><zone id="1" groupid="0" ch="ST" role="none" roomname="" groupname="" powerstate="0" iconid="1" color="0" delay="21000"/><zone id="2" groupid="0" ch="ST" role="none" roomname="" groupname="" powerstate="0" iconid="15" color="0" delay="21000"/><zone id="3" groupid="0" ch="ST" role="none" roomname="" groupname="" powerstate="0" iconid="0" color="0" delay="21000"/><zone id="4" groupid="0" ch="ST" role="none" roomname="" groupname="" powerstate="0" iconid="0" color="0" delay="21000"/></zonelist></mdi>"""
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

class OnkyoServer:

    class Handler(socketserver.StreamRequestHandler):

        def handle(self):
            self.server.client.on_message = lambda msg: self.client_message(msg)
            print("Connection from {}".format(self.client_address[0]))
            print("Thread Name:{}".format(threading.current_thread().name))

            receive_buffer = eiscp.core.MessageBuffer(10 * 1024)

            while True:
                data = self.request.recv(receive_buffer.available)
                receive_buffer.recv(data)
                try:
                    msg = receive_buffer.get_message()
                    if msg:
                        self.handle_message(msg)
                except Exception as e:
                    print(f"Exception parsing message: {e}")

        def client_message(self, message):
            print(f"Got message from receiver: {message}")
            self.send_raw_message(message)

        def send_raw_message(self, message):
            packet = eiscp.core.eISCPPacket(eiscp.core.ISCPMessage(message)).get_raw()
            print(f"Sending: {packet}")
            self.request.sendall(packet)

        def handle_message(self, message):
            print(message)
            try:
                cmd_decoded = eiscp.core.iscp_to_command(message, True)
                print(cmd_decoded)
            except:
                cmd_decoded = None
            if message == 'NRIQSTN':
                response = f'NRI{__info_response__}'
                self.send_raw_message(response)
            elif message == 'MDIQSTN':
                response = f'MDI{__mdi_response__}'
                self.send_raw_message(response)
            # elif message in ('PWRQSTN', 'ZPWQSTN', 'PW3QSTN'):
            #     self.send_raw_message(message[:3] + '00')
            # elif message in ('SLIQSTN', 'SLZQSTN', 'SL3QSTN'):
            #     self.send_raw_message(message[:3] + '12')
            # elif message in ('MVLQSTN',):
            #     self.send_raw_message(message[:3] + '30')
            # elif message == 'PPSQSTN':
            #     self.send_raw_message(message[:3] + '111')
            # elif message == 'DUSQSTN':
            #     self.send_raw_message(message[:3] + 'NM--0')
            else:
                print(f"Send to receiver => {message}")
                self.server.client.raw(message)

    def __init__(self, client):
        self.client = client
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.bind(('0.0.0.0', eiscp.eISCP.ONKYO_PORT))

        self.server_socket = socketserver.ThreadingTCPServer(('0.0.0.0', eiscp.eISCP.ONKYO_PORT), OnkyoServer.Handler)
        self.server_socket.client = self.client
        server_thread = threading.Thread(target=self.server_socket.serve_forever)
        server_thread.daemon = True
        server_thread.start()




    def loop(self):
        while True:
            data, addr = self.broadcast_socket.recvfrom(1024)
            packet = eiscp.core.eISCPPacket.parse(data).strip()
            print(f'Received: {packet} from {addr}')
            magic_onkyo = '!xECNQSTN'
            magic_pioneer = '!pECNQSTN'
            print(f'Compare to: {magic_onkyo}/{magic_pioneer}')
            if packet == magic_onkyo or packet == magic_pioneer:
                response = eiscp.core.eISCPPacket("!1ECNTX-NR8100/60128/DX/0009B060B054")
                print(f"Sending back {response}")
                self.broadcast_socket.sendto(response.get_raw(), addr)
            else:
                print(f'{packet} != {magic_onkyo} or {magic_pioneer}')

def main():
    e = eiscp.core.Receiver("10.10.10.246")
    print(e.info)
    #e.on_message = lambda msg: print(msg)
    #e.command('dock.receiver-information=query')
    e.command('main.power=query')
    server = OnkyoServer(e)
    server.loop()

main()
    # info = re.match(r'''
    #     !
    #     (?P<device_category>\d)
    #     ECN
    #     (?P<model_name>[^/]*)/
    #     (?P<iscp_port>\d{5})/
    #     (?P<area_code>\w{2})/
    #     (?P<identifier>.{0,12})
    # ''', response.strip(), re.VERBOSE).groupdict()


