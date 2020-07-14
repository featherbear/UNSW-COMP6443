#linux x64
#python 2.7 dependencies:
#certifi==2019.6.16
#chardet==3.0.4
#Click==7.0
#Flask==1.1.1
#gunicorn==19.9.0
#idna==2.8
#itsdangerous==1.1.0
#Jinja2==2.10.1
#MarkupSafe==1.1.1
#requests==2.22.0
#urllib3==1.25.3
#uuid==1.30
#Werkzeug==0.15.5
#setuptools==41.0.1

from flask import Flask, Response, request, make_response, render_template
import requests
import uuid
from subprocess import Popen, PIPE
from itsdangerous import Signer, BadSignature
import helpers
import os

app = Flask(__name__)


@app.route('/letter.pdf', methods=['POST'])
def format():
  if os.getuid() == 0:
    os.setgroups([])
    os.setgid(1000)
    os.setuid(1000)
  md = request.form.get("text", "you didnt put anything so this is default doc")
  user = helpers.get_user()
  handle = user["username"].split("@")[0]
  usernames = user["displayname"].split()
  filename = '/tmp/' + handle + '_' + str(uuid.uuid4())
  dbg_option = request.form.get("debug", "")
  template = """
    \\documentclass[11pt,a4paper,roman]{moderncv}      
    \\usepackage[english]{babel}
    \\usepackage{ragged2e}
    \\usepackage{float}
    \\usepackage{graphicx}
    \\usepackage[utf8]{inputenc}   
    
    \\moderncvstyle{classic}                            
    
    \\usepackage[scale=0.8]{geometry} 
    
    \\name{%s}{%s}
    \\address{K17 UNSW Sydney, Kensington}{Sydney NSW 2052, Australia}
    \\homepage{www.quoccabank.com}                 
    \\email{%s@quoccabank.com}
    
    \\begin{document}
    
    \\begin{minipage}[t]{\\textwidth}
    \\includegraphics[width=0.60\\textwidth]{/quoccabank.png}
    \\end{minipage}
    
    
    \\recipient{To Whom It May Concern:}{}
    \\opening{\\vspace*{-2em}}
    \\closing{Sincerely,}{\\vspace*{-2em}}
    \\enclosure[QuoccaBank]{Your Cyber-Friendly Bank, Confidential and Proprietary}
    \\makelettertitle
    
    \\justifying
    
    $body$
    
    \\vspace{0.5cm}
    
    \\makeletterclosing
    
    \\end{document}
  """ % (usernames[0], usernames[-1], handle)

  if dbg_option != "":
    # this makes us super safe
    with open("/key", "r") as key_file:
      skey = key_file.read().strip()
    s = Signer(skey)
    try:
      dbg_option = s.unsign(dbg_option).decode('utf-8')
    except BadSignature:
      return helpers.error_page(
          403,
          "Forbidden",
          "You don't have access",
          publicDebug="debug option is not signed correctly")

  with open(filename + ".md", "w") as text_file:
    text_file.write(md)
  with open(filename + "_template.tex", "w") as text_file:
    text_file.write(template)
  try:
    p = Popen(
        ('timeout', '5', 'pandoc', '--template=' + filename + "_template.tex",
         '--from=markdown', '-s', '-o', filename + '.pdf', '--latex-engine-opt',
         dbg_option, filename + '.md'),
        stdout=PIPE,
        stderr=PIPE)
    out, err = p.communicate()
    exitcode = p.returncode
    if exitcode != 0:
      return helpers.error_page(
          500,
          "Internal Error",
          "Something went wrong while typesetting",
          publicDebug="%s\n%s\nexited with error code %d" %
          (out, err, exitcode))
      rsp.headers['Content-type'] = 'text/plain'
      return rsp
    try:
      with open(filename + '.pdf', mode='rb') as pdf_file:
        rsp = make_response(pdf_file.read())
        rsp.headers['Content-type'] = "application/pdf"
      return rsp
    except FileNotFoundError:
      return helpers.error_page(
          500,
          "Internal Error",
          "Something went wrong while typesetting",
          publicDebug="%s\n%s\nNo response PDF generated" % (out, err))
  except Exception as e:
    return helpers.error_page(
        500,
        "Internal Error",
        "Something went wrong while typesetting",
        publicDebug=str(e))


@app.route('/source')
def viewsource():
  fp = __file__
  if fp.endswith(".pyc"):
    fp = fp[:-1]
  with open(fp) as f:
    rsp = make_response(f.read())
    rsp.headers['Content-type'] = 'text/plain'
  return rsp


@app.route('/healthz')
def health():
  return "ok"


@app.route('/flag')
def getflag():
  if helpers.get_user()["username"] != "admin@quoccabank.com":
    return helpers.error_page(403, "Forbidden", "I'll have to report this!")
  return open("/flag").read()


@app.route('/')
def index():
  return render_template("index.html")


if __name__ == '__main__':
  app.run(debug=False, host='0.0.0.0', port=80)
