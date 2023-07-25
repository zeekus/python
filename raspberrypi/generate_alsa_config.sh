#!/bin/bash
#generate_alsa_config.sh

# Get the card and device numbers for the USB microphone and USB speaker
#card 1: Mic [Samson Go Mic], device 0: USB Audio [USB Audio]
mic_card=$(aplay -l | grep "Mic \[.*\]" | awk -F':' '{print $1}' | cut -d' ' -f2)
mic_device=$(aplay -l | grep "Mic \[.*\]" | awk -F',' '{print $2}'| cut -d' ' -f3| sed 's/://' )

#speaker for us looks like this
#card 0: Device [USB2.0 Device], device 0: USB Audio [USB Audio]
#this gets 0 fo speaker card, and 0 for speaker device
speaker_card=$(aplay -l | grep "USB2.0" | awk -F',' '{print $1}' |cut -d' ' -f2| sed s/://g)
speaker_device=$(aplay -l | grep "USB2.0" | awk -F',' '{print $2}' |cut -d' ' -f3| sed s/://g)

# Generate the .asoundrc file
echo "pcm.!default {
  type asym
  playback.pcm \"hw:$speaker_card,$speaker_device\"
  capture.pcm \"hw:$mic_card,$mic_device\"
}" > ~/.asoundrc

echo "Generated .asoundrc file for USB microphone on card $mic_card device $mic_device and USB speaker on card $speaker_card device $speaker_device"

