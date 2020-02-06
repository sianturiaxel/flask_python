import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Tempat Menyimpan Pin Dan No Pin
pins = {
   23 : {'pin_nama' : 'GPIO 23', 'state' : GPIO.HIGH},
   24 : {'pin_nama' : 'GPIO 24', 'state' : GPIO.HIGH},
   25 : {'pin_nama' : 'GPIO 25', 'state' : GPIO.HIGH}
   }

# Atur Pin Yang menjadi Outputnya
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   
   templateData = {
      'pins' : pins
      }
   # Verifikasi data yang akan di desktipsikan pada main.html
   return render_template('main.html', **templateData)

# Berikut Merupakan Fungsi Url yang diakses dan perintah yang akan diberikan
@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['pin_nama']
   if action == "open":
      # Set untuk pin higt
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " Open."
   if action == "close":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " Close."

   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)


   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)

