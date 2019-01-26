import flask
import uuid
import os.path
import magic
import hashlib
import binascii
import config

datastore = config.datastore
salt = config.salt
url = config.url

app = flask.Flask(__name__)

def hash(filename):
  hash = hashlib.pbkdf2_hmac('sha256', bytes(filename, encoding='ascii'), bytes(salt, encoding='ascii'), 100000)
  hexhash = binascii.hexlify(hash).decode()
  return hexhash

@app.route('/', methods=['POST'])
def post():
  post = flask.request.get_data()
  filetype = magic.from_buffer(post, mime=True).split("/",1)[1]
  if filetype in {'jpeg','png','webm'}:
    while True:
      uid = uuid.uuid4().hex[:6]
      filename = uid+"."+filetype
      path = os.path.join(datastore, filename)
      if not os.path.exists(path):
        break

    with open(path, 'wb') as file:
      file.write(post)
    
#    if filetype in {'jpeg','png'}:
#      try:
#        subprocess.call(['/usr/bin/exiftool', '-overwrite_original', '-all=', path])
#      except (OSError, ValueError, CalledProcessError) as e:
#        flask.abort(500)
#    elif (filetype == 'webm'):
#      #do ffmpeg stuff

    # give back the url and a secret proving the user uploaded the file

    return url+filename+"\n"+hash(filename)
  else:
    flask.abort(415)

@app.route('/<filename>', methods=['DELETE'])
def delete(filename):
  path = os.path.join(datastore, filename)
  header = flask.request.headers.get('X-image-hash')
  if not os.path.exists(path) or os.stat(path).st_size == 0:
    flask.abort(404)
  elif header is None or len(header) != 64:
    flask.abort(400)
  elif hash(filename) == header:
    with open(path, 'w'):
      pass
    return ('', 204)
  else:
    flask.abort(403)
