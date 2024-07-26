import IPython.display as ipd
import numpy as np
import scipy.io.wavfile as wavfile
from io import BytesIO
from google.colab import output
from base64 import b64decode
from google.colab import files
from IPython.display import HTML
from base64 import b64encode

RECORD_HTML = """
<script>
var my_div = document.createElement("DIV");
var my_p = document.createElement("P");
var my_btn = document.createElement("BUTTON");
var t = document.createTextNode("Press to start recording");
my_btn.appendChild(t);
my_div.appendChild(my_p);
my_div.appendChild(my_btn);
document.body.appendChild(my_div);

var base64data = 0;
var reader;
var recorder, gumStream;

var handleSuccess = function(stream) {
  gumStream = stream;
  var options = {
    mimeType : 'audio/webm;codecs=opus'
  };          
  recorder = new MediaRecorder(stream, options);
  recorder.ondataavailable = function(e) {
    var url = URL.createObjectURL(e.data);
    var preview = document.createElement('audio');
    preview.controls = true;
    preview.src = url;
    document.body.appendChild(preview);
    reader = new FileReader();
    reader.readAsDataURL(e.data); 
    reader.onloadend = function() {
      base64data = reader.result;
      google.colab.kernel.invokeFunction('notebook.recorder', [base64data], {});
    }
  };
  recorder.start();
  my_btn.innerText = "Recording... press to stop";
  recorder.onstop = function() {
    gumStream.getAudioTracks()[0].stop();
    my_btn.innerText = "Press to start recording";
  };
};

my_btn.onclick = function() {
  if (recorder && recorder.state == "recording") {
    recorder.stop();
  } else {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(handleSuccess);
  }
}
</script>
"""

def get_audio():
    display(ipd.HTML(RECORD_HTML))
    audio_string = output.eval_js('google.colab.kernel.invokeFunction')
    audio_bytes = b64decode(audio_string.split(',')[1])
    process_wav = BytesIO(audio_bytes)
    rate, data = wavfile.read(process_wav)
    return rate, data

def upload_video():
    uploaded = files.upload()

def process_video():
    os.system('cd Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "/content/sample_data/input_video.mp4" --audio "/content/sample_data/input_audio.wav"')
    files.download('/content/Wav2Lip/results/result_voice.mp4')
    mp4 = open('/content/Wav2Lip/results/result_voice.mp4','rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    display(HTML(f"""
    <video width="50%" height="50%" controls>
          <source src="{data_url}" type="video/mp4">
    </video>
    """))
