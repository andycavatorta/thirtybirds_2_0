scripts = {
    "0.01":[
        "sudo apt-get update",
        "sudo apt-get dist-upgrade -y",
        "sudo python /home/pi/RBK/common/configuremojo.py -v -n -d=/dev/mojo -i=/home/pi/RBK/fpga/mojo-base-project-master-sig-gen/syn/mojo_top.bin"
    ],
    "0.02":[
        "echo running upgrade scripts for version 0.02"
    ],
    "0.03":[
        "sudo apt-get update",
        "sudo apt-get install build-essential python-pip python-dev python-smbus git",
        "git clone https://github.com/adafruit/Adafruit_Python_GPIO.git",
        "cd Adafruit_Python_GPIO",
        "sudo python setup.py install"
    ]
}
