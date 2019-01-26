import flask
import uuid
import os.path
import magic

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def pipeup():
  datastore = '/var/www/dh.ax/'
  post = flask.request.get_data()
  filetype = magic.from_buffer(post, mime=True).split("/",1)[1]
  if filetype in {'jpeg','png','webm'}:
    while True:
      uid = uuid.uuid4().hex[:6]
      filename = uid+"."+filetype
      path = os.path.join(datastore, filename)
      if not os.path.exists(path):
        break

    with open(path, "wb") as file:
      file.write(post)
    
#    if filetype in {'jpeg','png'}:
#      try:
#        subprocess.call(['/usr/bin/exiftool', '-overwrite_original', '-all=', path])
#      except (OSError, ValueError, CalledProcessError) as e:
#        flask.abort(500)
#    elif (filetype == 'webm'):
#      #do ffmpeg stuff

    return "https://dh.ax/"+filename+"\n"
  else:
   flask.abort(415) 
