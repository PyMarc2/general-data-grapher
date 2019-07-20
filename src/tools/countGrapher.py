from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import scipy.misc
import numpy as np
import math
import os
import argparse


def countOccurences(File, separator):
    occ = {}
    with open(File, 'r') as file:
        data = file.read()
        dataList = sorted(list(map(int, data.split(separator))))
        print(dataList)
        for element in dataList:
            if element not in occ:
                occ[int(element)] = 0

        tempDataList = dataList
        for key in occ:
            occ[key] = tempDataList.count(key)
            #print(occ)
            for times in range(occ[key]):
                tempDataList.remove(key)
            #print(tempDataList)
        print("xvalues = ", list(occ.keys()))
        print("yvalues = ", list(occ.values()))
    return list(occ.keys()), list(occ.values())


def plotDataModel(figure, xlist, ylist, xfit=None, yfit=None, xaxis=None, yaxis=None, modelLabel=None, infos=0):

    n = len(figure.axes)
    for i in range(n):
        figure.axes[i].change_geometry(n + 1, 1, i + 1)

    ax = figure.add_subplot(n + 1, 1, n + 1)
    ax.plot(xlist, ylist, 'ok', markersize=3)
    plt.subplots_adjust(hspace=0.5)

    if xaxis is not None:
        ax.set_xlabel(xaxis)

    if yaxis is not None:
        ax.set_ylabel(yaxis)

    if infos is not None:
        pass

    if xfit is not None and yfit is not None:
        ax.plot(xfit, yfit, '-', markersize=3, label=modelLabel)
        ax.legend()


def fitData(xlist, ylist, model):
    popt, pcov = curve_fit(model, xlist, ylist)
    xfit = np.linspace(min(xlist), max(xlist), 100)
    yfit = []
    for i in range(len(xfit)):
        yfit.append(model(xfit[i], *popt))
    return xfit, yfit, popt


# ====== REGRESSION MODELS FOR DATA FITTING ======== #
def gaussian(x, a, mu, sigma):
    return a * np.exp(-((x - mu) / sigma) ** 2)

def gamma(x, l, a):
    return a**l/scipy.special.factorial(a-1) * x**(a - 1) * np.exp(-l*x)

def expo(x, l):
    return l * np.exp(-l*x)

def linear(x, m, b):
    return m*x + b


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Count and plot numerical data distributions in the CSV form")
    parser.add_argument('datafile', metavar='F', help="data file that will be analysed")
    args = parser.parse_args()
    print(args.datafile)
    data = countOccurences(os.path.abspath(os.path.dirname(__file__))+'/'+args.datafile, ',')

    datax, datay = countOccurences(os.path.abspath(os.path.dirname(__file__)) + '/' + 'dataTest.txt', ',')
    xGaussFit, yGaussFit, coeff = fitData(datax, datay, gaussian)
    xGammaFit, yGammaFit, coeff2 = fitData(datax, datay, gamma)
    xExpoFit, yExpoFit, coeff3 = fitData(datax, datay, expo)
    xLinearFit, yLinearFit, coeff4 = fitData(datax, datay, linear)

    fig = plt.figure()

    plotDataModel(fig, datax, datay, xGaussFit, yGaussFit, 'Hurricanes/year', 'Amount', 'Gaussian fitting')
    plotDataModel(fig, datax, datay, xGammaFit, yGammaFit, 'Hurricanes/year', 'Amount', 'Gamma fitting')
    plotDataModel(fig, datax, datay, xExpoFit, yExpoFit, 'Hurricanes/year', 'Amount', 'Exponential fitting')
    plotDataModel(fig, datax, datay, xLinearFit, yLinearFit, 'Hurricanes/year', 'Amount', 'Linear fitting')

    print(coeff)
    print(coeff2)
    print(coeff3)

    plt.show()




