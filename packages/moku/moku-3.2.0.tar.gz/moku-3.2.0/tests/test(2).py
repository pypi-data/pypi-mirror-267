


from moku.instruments import SpectrumAnalyzer


import matplotlib.pyplot as plt
import time
import numpy as np



def check_frame(frame, start, stop):
	frame_start = frame["frequency"][0]
	frame_stop  = frame["frequency"][-1]

	if abs(start - frame_start) > 0.01*start:
		return 1

	if abs(stop - frame_stop) > 0.01*stop:
		return 1

	return 0




for attempt in range(100):
	print("\nAttempt {}".format(attempt))
	i = SpectrumAnalyzer('10.1.120.32', force_connect = True)

	for ch in [1, 2, 3, 4]: i.set_frontend(ch, "50Ohm", "DC", "400mVpp")

	 

	 
	i.set_span(0, 300e6)  
	i.set_span(5e6, 5e6+10e6)  
	data = i.get_data(wait_reacquire=True)
	for j in range(4): plt.plot(data["frequency"], data["ch{}".format(j+1)])
	plt.savefig("test.png")
	print("Frequency span is {} to {}".format(data["frequency"][0], data["frequency"][-1]))

	if check_frame(data, 5e6, 5e6+10e6):
		print("Got issue")
		for d in data.keys():
			if d.startswith("ch"):
				print("{} {}".format(d, np.mean(data[d])))
			

		# Check if next frame is still bad
		print("Checking next frame")
		data = i.get_data(wait_reacquire=True)
		print("Next frame frequency span is {} to {}".format(data["frequency"][0], data["frequency"][-1]))

		if check_frame(data, 5e6, 5e6+10e6):
			print("Next frame also bad !!!")
		else:
			print("Next frame was OK")
		input("Enter to continue")

	print()
	time.sleep(2)
