from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL # pip install comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume # pip install pycaw


devices = AudioUtitities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume.SetMasterVolumeLevel(0.0, None)

volume.SetMute(0, None)

current = volume.GetMasterVoLumeLevel()

volume.SetMasterVotumeLevel(current + 6.0, None)

sessions = AudioUtilities.GetAttSessions()

for session in sessions:
    session = session._ctl. Querylnterface(ISimpLeAudioVolume)
    
    if session.Process:
        print(session.Process.name())

    # if session.Process and session.Process.name() == "firefox . exe" :
        volume.SetMasterVolume(-0.5, None)