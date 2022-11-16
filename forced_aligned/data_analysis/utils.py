from matplotlib import pyplot as mp
from scipy.stats import skew
import numpy as np

def getBoundariesList(list):
	"""

	:param list:
	:return:
	"""
	d_list = []
	for idx in range(0, len(list)):
		_, st, en = list[idx]
		if idx == 0:
			d_list.append(abs(st))
			d_list.append(abs(en))
		else:
			d_list.append(abs(en))
	return d_list

def print_dataPointAmount(all_deviations):
	pho2amount = dict()
	for pho, _, _ in all_deviations:
		if not pho in pho2amount.keys():
			pho2amount[pho] = 1
		else:
			pho2amount[pho] += 1
	print(pho2amount)

def print_overallTransAccuracy(allWFresults):
	'''
	print the mean accuracy score (based on Schiel) for all utterances
	also print the skewness

	@author: FK
	'''
	all_accuracies = []
	for length, subs, dels, ins in allWFresults:
		all_accuracies.append(measureTransAccuracy(length, subs, dels, ins))
	print("Overall, for " + str(len(allWFresults)) + " utterances")
	print("\tthe mean accuracy score (based on Schiel) is " + str(sum(all_accuracies)/len(all_accuracies)))
	print("\tthe skew of this accuracy is " + str(skew(all_accuracies)))


def print_DelInsSub(allWFresults, amount_all_phonemes):
	'''
	print the amount of all Deletions, Insertions and Substitutions

	@author: FK
	'''
	all_dels = 0
	all_ins = 0
	all_subs = 0
	for _, subs, dels, ins in allWFresults:
		all_dels += dels
		all_ins += ins
		all_subs += subs
	print("overall, for " + str(amount_all_phonemes) + " utterances there are")
	print('\t' + str(all_dels) + '/' + str(amount_all_phonemes) + " deletions")
	print('\t' + str(all_ins) + '/' + str(amount_all_phonemes) + " insertions")
	print('\t' + str(all_subs) + '/' + str(amount_all_phonemes) + " substitutions")

def getAverage(diff_list: list):
	"""

	:param diff_list:
	:return:
	"""
	start = 0.0
	end = 0.0
	counter = 0
	for idx in range(0, len(diff_list)):
		*_, s, e = diff_list[idx]
		if idx == 0:
			start += abs(s)
			end += abs(e)
		else:
			end += abs(e)
		counter += 1

	return (round(start, 4) + round(end, 4)) / (counter + 1)

def measureTransAccuracy(refLen, n_subs, n_dels, n_ins):
	"""
	Outputs transcription accuracy
	based on Schiel paper
	:param refLen:
	:param n_subs:
	:param n_dels:
	:param n_ins:
	:return:
	"""
	#print("Accuracy value is: " + str(round((refLen - n_subs - n_ins - n_dels) / refLen, 2)))
	return round((refLen - n_subs - n_ins - n_dels) / refLen, 2)

def ecdf_function(data):
	x = []
	for index in range(len(data)):
		_, s, e = data[index]
		if index == 0 and abs(s) < 0.05:
			x.append(abs(s))
		if abs(e) < 0.05:
			x.append(abs(e))
	x_sorted = np.sort(x)
	y = np.arange(1,(len(x) + 1)) / len(x)
	return x_sorted, y


def prepare_phonemClasses(all_deviations, phonem_classes):
	pho2devs = dict()
	for key in phonem_classes.keys():
		pho2devs[key] = []
	for label, devs in all_deviations.items():
		for class_name, phonemes in phonem_classes.items():
			if label in phonemes:
				pho2devs[class_name] = pho2devs[class_name] + [dev for dev in devs]
	return pho2devs

############
###### plots
############

def plotHistogram(data, savePath="data_analysis/results/histogram.png"):
	"""
	Plots histogram of *all* deviations, not seperated by phone
	:param data:
	:return:
	"""
	# change the data structure
	all_boundary_deviations = []
	for index in range(len(data)):
		_, s, e = data[index]
		if index == 0:
			all_boundary_deviations.append(abs(s))
		all_boundary_deviations.append(abs(e))

	fig, ax = mp.subplots()
	mp.style.use('ggplot')
	ax.hist([boundary for (boundary) in all_boundary_deviations if boundary<=0.05], bins=15)
	#ax.hist(all_boundary_deviations, bins=40)
	ax.set_xlabel("Time deviation (s)")
	ax.set_ylabel("Number of time points")
	#ax.set_title("Deviation from reference (s)")
	#ax.set_xlim([0, 0.5])
	#mp.show()
	fig.savefig(savePath, dpi=200)

def drawBoxPlot(dev_values, dev_labels, savePath="data_analysis/results/boxplot.png"):
	"""
	Plots boxplot
	:param data:
	:return:
	"""
	#new_vals = []
	#for v in dev_values:
	#	new_vals.append([abs(val) for val in v])
	#dev_values = new_vals
	
	mp.style.use('ggplot')
	
	fig1, ax1 = mp.subplots()
	fig1.set_figwidth(10)
	fig1.set_figheight(7)
	ax1.boxplot(dev_values, labels=dev_labels, showfliers=False)

	ax2 = mp.twiny()
	mp.xlim(0, 1)
	ax2.get_xaxis().set_visible(False)
	ax2.get_yaxis().set_visible(False)
	y = [-0.35, 0.35]
	ax2.plot([0.448, 0.448], y, [0.51, 0.51], y, [0.695, 0.695], y, [0.756, 0.756], y, [0.898, 0.898], y, [0.96, 0.96], y, color="orange")
	ax1.set_ylabel("Deviation (s)")
	ax1.set_xlabel("Phone (sorted by class)")
	#ax1.set_title("Deviation per phone (s)")
	#mp.show()
	fig1.savefig(savePath, bbox_inches="tight", dpi=200)

def plotECDF (x_data, y_data, savePath="data_analysis/results/ecdf_plot.png"):
	mp.style.use('ggplot')
	fig2, ax2 = mp.subplots()
	ax2.plot(x_data, y_data, marker = '.', linestyle = 'none')
	ax2.set_ylabel(("Fraction of values"))
	ax2.set_xlabel("Deviation (s)")
	#ax2.set_title("ECDF plot")
	#mp.show()
	fig2.savefig(savePath, dpi=200)

def plotPhonemClasses(class2devs, savePath="data_analysis/results/classes.png"):
	mp.style.use("ggplot")
	fig, ax = mp.subplots()
	ax.boxplot([v for (_, v) in class2devs.items()], labels=[k for (k, _) in class2devs.items()], showfliers=False)
	ax.set_ylabel("Deviation (s)")
	ax.set_xlabel("Phoneme class")
	#ax.set_title("Deviation per phoneme class (s)")
	fig.savefig(savePath, dpi=200)
