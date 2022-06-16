import subprocess
from flask import Flask
app = Flask(__name__)

@app.route("/cmd01/<c1>")
def cmd_flask_nobrackets1(c1):
    output=subprocess.check_output(c1) #true positive to start with
    return output.decode()

@app.route("/cmd02/<c1>")
def cmd_flask_brackets1(c1):
    output=subprocess.check_output([c1]) #false negative
    subprocess.run([c1]) #just trying different variations..
    subprocess.Popen([c1]) #all of which are false negative..
    return output.decode()

import shlex
@app.route("/cmd03/<cmd>")
def cmd_flask_imported_shlex(cmd):
    split=shlex.split(cmd)
    output=subprocess.check_output(split) #false negative
    return output.decode()

@app.route("/cmd04/<c1>/<c2>/<c3>")
def cmd_flask_inbrackets3(c1,c2,c3):
    output=subprocess.check_output([c1,c2,c3])# false negative
    return output.decode()

@app.route("/cmd06/<c1>/<c2>/<c3>")
def cmd_flask_nobrackets3_static_first(c1,c2,c3):
    output=subprocess.check_output("foo",c1,c2,c3) #true negative, since this doesnt work
    return output.decode()#but interesting in showing that it only cares about the first param


@app.route("/cmd06/<c1>/<c2>/<c3>") #one last bonus
def cmd_flask_varargs(**cmd):  #does snyk not support kwargs?
    output=subprocess.check_output(cmd['c1'])
    output+=subprocess.check_output(list(cmd.values())) 
    output+=subprocess.check_output(list(cmd.values())[0]) 
    return output.decode() #even xss doesn't get caught on this one

if __name__ == '__main__':
    app.run()