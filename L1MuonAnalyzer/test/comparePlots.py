from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1D, TEfficiency, TH2D
from ROOT import gROOT
from ROOT import gStyle
from ROOT import TLegend
from ROOT import kBlack, kBlue, kRed, kGreen, kMagenta, kCyan
from array import array

from ROOT import TDirectory
import os
import sys
    


def makeUniqueFileName(path, name):
    fn = os.path.join(path, name)
    if not os.path.exists(fn):
        return fn

    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s%d%s' % (name, i, ext))

    for i in xrange(2, sys.maxint):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

    return None
###########################################


gStyle.SetOptStat(0)
gStyle.SetOptTitle(0);


# leg -> SetHeader("here is a beautiful header")

#plotsDir = '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_11_x_x_l1tOfflinePhase2/CMSSW_11_1_3/src/usercode/L1MuonAnalyzer/test/'
#plotsDir = '/home/kbunkow/CMSSW/CMSSW_12_1_0_pre5/src/usercode/L1MuonAnalyzer/test/'
#plotsDir = '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_13_x_x/CMSSW_13_1_0/src/usercode/L1MuonAnalyzer/test/'
plotsDir = '/afs/cern.ch/work/k/kbunkow/public/CMSSW/cmssw_14_x_x/CMSSW_14_0_0_pre3/src/usercode/L1MuonAnalyzer/test/'

first = True

logScalePads = []
logScalePadNum = 0
effHistCopys = []

def drawEff(canvas, effFile, type, quality, ptCut, lineColor, legend, pTresh = "0.5") :
    global first
    doEff = True
    
    if not doEff :
        if type == "nn_omtf" :
            histName = type + "_q" + quality + "_pTresh_" + pTresh + "_efficiency_eta_0.82_1.24_qualityCut_" + quality + "_effOnPtCut_" + ptCut + "_GeV_1"
        else :
            histName = type + "_q" + quality + "_eta_0.82_1.24_qualityCut_" + quality + "_effOnPtCut_" + ptCut + "_GeV_1"
            #omtf_q12_eta_0.82_1.24_qualityCut_12_effOnPtCut_20_GeV_1
    else  :    
        if type == "nn_omtf" :
            histName = type + "_q" + quality + "_pTresh_" + pTresh + "_efficiency_eta_0_3_qualityCut_" + quality + "_ptCut_" + ptCut + "_GeV"
        elif type == "omtf_extrp" :
            #histName = type + "_q" + quality + "_pTresh_" + pTresh + "_efficiency_eta_0.82_1.24_qualityCut_" + quality + "_ptCut_" + ptCut + "_GeV"
            histName = "omtf" + "_q" + quality + "_pt_efficiency_eta_0_3_qualityCut_" + quality + "_ptCut_" + ptCut + "_GeV"    
        elif type == "omtf_v1" :
            histName = "omtf" + "_q" + quality + "_pt_efficiency_eta_0.82_1.24_qualityCut_" + quality + "_ptCut_" + ptCut + "_GeV" 
        else :
            histName = type + "_q" + quality + "_efficiency_eta_0.82_1.24_qualityCut_" + quality + "_ptCut_" + ptCut + "_GeV"    
            #omtf_q12_efficiency_eta_0.82_1.24_qualityCut_12_ptCut_18_GeV
                    
    print (effFile)    
    print (histName) 

    effHist = effFile.Get(histName)
    if effHist is None :
        print ("no histogram found: ", histName)
    else :
        print ("ploting histogram: ", histName)
        
    canvas.cd(1)       
    
    effHist.SetLineColor(lineColor)
    print ("first " + str(first) )
    if first :
        if not doEff :
            effHist.Draw("hist")
            effHist.GetXaxis().SetRangeUser(0, 200)
            effHist.GetYaxis().SetRangeUser(0, 1.00)
        else :    
            effHist.Draw("AEP")
            effHist.SetMarkerStyle(22)
            effHist.SetMarkerColor(lineColor)
            canvas.cd(2).Update()
            effHist.GetPaintedGraph().GetYaxis().SetRangeUser(0., 1.00)

    else:
        if not doEff :
            effHist.Draw("hist same")
        else :
            effHist.Draw("P same")       
        
    if legend :    
        legend.AddEntry(effHist)  # , "OMTF", "lep");
        
    effHist.SetLineColor(lineColor)
    
    canvas.cd(2)
    if doLogScale :
        canvas.cd(2).SetLogy()    
    print ("first " + str(first) )
    if first :
        if not doEff :
            effHistCopy = effHist.DrawCopy("hist")
        else :    
            effHistCopy = effHist.Clone(effHist.GetName() + "_log")
            effHistCopy.Draw("AE")     
            canvas.cd(2).Modified()         
            canvas.cd(2).Update()
            print ("printig ", effHistCopy.GetName() ) 
            if doLogScale :
                effHistCopy.GetPaintedGraph().GetXaxis().SetRangeUser(0, 25)
                effHistCopy.GetPaintedGraph().GetYaxis().SetRangeUser(0.001, 1.05)
            else :
                effHistCopy.GetPaintedGraph().GetYaxis().SetRangeUser(0.8, 1.00)  
    else:
        if not doEff :
            effHistCopy = effHist.Clone(effHist.GetName() + "_log")
            effHistCopy.DrawCopy("hist same")
        else :
            effHistCopy = effHist.Draw("E same")   
    
    canvas.cd(2).Update()        
    effHistCopys.append(effHistCopy)
    
#     if first :
#         pad = TPad('pad_' + str(logScalePads.__len__()), 'pad', 0.4,  0.27,  0.99,  0.75)
#         
#         pad.Draw()
#         pad.cd()
#         #pad.SetLogy()
#         pad.SetGridx()
#         pad.SetGridy()
#         pad.SetRightMargin(0.01)
#         pad.SetTopMargin(0.01)
#         pad.SetLeftMargin(0.1)
#         
#         #pad.SetLogx()
#         #pad.SetLogy()
#         if not doEff :
#         effHistCopy = effHist.DrawCopy("hist")
#         effHistCopy.GetXaxis().SetRangeUser(2, 20)
#         effHistCopy.GetYaxis().SetRangeUser(0.00, 0.1)
#         effHistCopy.GetYaxis().SetTitleOffset(1.5)
#         effHistCopys.append(effHistCopy)
#         logScalePads.append(pad)
#     else:
#         logScalePads[logScalePadNum].cd()
#         print("pad name " + logScalePads[logScalePadNum].GetName() )
#         effHistCopy = effHist.DrawCopy("hist same")    
#         effHistCopys.append(effHistCopy)
#         print ("line 84")
         
###################################################

effHists = []
firstEtaPlot = True
def drawEffVsEta(effFile, type, quality, lineColor, pTresh = "0.5") :
    global firstEtaPlot 
    
    #mtf_q12_efficiencyVsEta__qualityCut_12_ptGenCut_25
    
    if type == "nn_omtf" :
        effHistName = type + "_q" + quality + "_pTresh_" + pTresh + "_efficiencyVsEta__qualityCut_" + quality + "_ptGenCut_25"
    elif type == "omtf_extrp" :
        effHistName = "omtf" + "_q" + quality + "_efficiencyVsEta__qualityCut_" + quality + "_ptGenCut_25"
    elif type == "omtf_v1" :
        effHistName = "omtf" + "_q" + quality + "_efficiencyVsEta__qualityCut_" + quality + "_ptGenCut_25"
    else :
        effHistName = type + "_q" + quality + "_efficiencyVsEta__qualityCut_" + quality + "_ptGenCut_25"
        #omtf_q12_eta_0.82_1.24_qualityCut_12_effOnPtCut_20_GeV_1
       
    effHist = effFile.Get(effHistName)
    print ("line 109 ", effHistName, effHist)   
    if effHist :    
        effHist.SetLineColor(lineColor)
        print ("first " + str(first) )
        if firstEtaPlot :
            #effHist.GetPaintedGraph().GetYaxis().SetRangeUser(0.8, 1.05)
            effHist.Draw("AE")
            firstEtaPlot =  False
            print("11111afsafdsafdsagfdsgsdg")
        else:
            effHist.Draw("same")   
        
        effHists.append(effHist)

rateFiles = []
fillPat = 3002

rateHist = []
def drawRate(rateFileDir, type, label, quality, lineColor, pTresh = "0.5") :
    global first
    global fillPat

    rateFile = TFile(plotsDir + rateFileDir + 'ratePlots.root' )
    rateFiles.append(rateFile)
    print("rateFile.GetName()", rateFile.GetName()) 
    rateFile.ls()
    
    withTEff = "_copy_allEventsHist_clone_copy"
    if type == "nn_omtf" :
        effHist = rateFile.Get(type + "_q" + quality + "_pTresh_" + pTresh + "_rate__qualityCut_" + quality +"_"+ withTEff)
    else :
        effHist = rateFile.Get(type + "_q" + quality + "_rate_Pt__qualityCut_" + quality +"_" + withTEff)
        
    print("effHist", type + "_q" + quality + "_rate__qualityCut_" + quality +"_" + withTEff)    
   
    effHist = effHist.Clone(effHist.GetName() + "_" + label)
    effHist.SetTitle(label)
    
    print ("rateHist", effHist.GetName() )  
    
    rateHist.append(effHist)
    effHist.SetLineColor(lineColor)
    #effHist.SetFillColor(lineColor);
    #effHist.SetFillStyle(fillPat)
    fillPat += 1
    #effHist.SetFillColorAlpha(lineColor, 0.5)
   
    global first
    if first :
        effHist.GetXaxis().SetRangeUser(0, 70)
        effHist.GetYaxis().SetRangeUser(1, 200)
        if withTEff == "" :
            effHist.Draw("hist")
        else :
            effHist.Draw("APZ")
        
    else:
        if withTEff == "" :
            effHist.Draw("hist same")   
        else :
            effHist.Draw("PZ")
         
    legend.AddEntry(effHist)  # , "OMTF", "lep");
    first = False
##################################################

######################################
c1 = TCanvas('canvas_efficiency_1', 'canvas_efficiency', 200, 10, 950, 500)
c1.Divide(2, 1)
c1.cd(1)
c1.cd(1).SetGridx()
c1.cd(1).SetGridy()
c1.cd(1).cd()

c1.cd(2).SetGridx()
c1.cd(2).SetGridy()

c2 = TCanvas('canvas_efficiency_2', 'canvas_efficiency_2', 200, 510, 950, 500)
c2.Divide(2, 1)
c2.cd(1).SetGridx()
c2.cd(1).SetGridy()
c2.cd(1).cd()

c2.cd(2).SetGridx()
c2.cd(2).SetGridy()

c3 = TCanvas('canvas_efficiency_3', 'canvas_efficiency_3', 200, 510, 950, 500)
c3.Divide(2, 1)
c3.cd(1).SetGridx()
c3.cd(1).SetGridy()
c3.cd(1).cd()

c3.cd(2).SetGridx()
c3.cd(2).SetGridy()

c4 = TCanvas('canvas_efficiency_4', 'canvas_efficiency_4', 200, 510, 950, 500)
c4.Divide(2, 1)
c4.cd(1).SetGridx()
c4.cd(1).SetGridy()
c4.cd(1).cd()

c4.cd(2).SetGridx()
c4.cd(2).SetGridy()

c5 = TCanvas('canvas_efficiency_5', 'canvas_efficiency_5', 200, 510, 950, 500)
c5.Divide(2, 1)
c5.cd(1).SetGridx()
c5.cd(1).SetGridy()
c5.cd(1).cd()

c5.cd(2).SetGridx()
c5.cd(2).SetGridy()

canvas_rate = TCanvas('canvas_rate', 'canvas_rate', 200, 510, 950, 500)
canvas_rate.Divide(2, 1)
canvas_rate.cd(1).SetGridx()
canvas_rate.cd(1).SetGridy()

canvas_rate.cd(2).SetGridx()
canvas_rate.cd(2).SetGridy()

#legendEff1 = TLegend(0.06, 0.8, 0.57, 0.997)
legendEff1 = TLegend(0.06, 0.9, 0.5, 0.99)

#legend.SetHeader(header.c_str())
# leg -> SetBorderSize(0);
legendEff1.SetFillStyle(0)
legendEff1.SetBorderSize(0)
legendEff1.SetTextSize(0.03)
legendEff1.SetMargin(0.2)

legendEff2 = legendEff1.Clone()
legendEff3 = legendEff1.Clone()


# eff_c1.SetTopMargin(0.2)
# eff_c2.SetTopMargin(0.2)
# eff_c3.SetTopMargin(0.2)

effFiles = []

def drawEffs(fileDir, type, quality, lineColor, pTresh = "0.5" ) :
    global first
    global logScalePadNum
    print ("first " + str(first) )
    effFile = TFile(plotsDir + fileDir + 'efficiencyPlots.root' )
    effFiles.append(effFile)
    if type == "omtf" or type == "omtf_extrp" or type == "omtf_v1":
        print (c1.GetName() )
        logScalePadNum = 0
        drawEff(c1, effFile, type, quality, "20", lineColor, legendEff1)
        
        logScalePadNum = 1 
        drawEff(c2, effFile, type, quality, "22", lineColor, legendEff2)

        logScalePadNum = 2
        drawEff(c3, effFile, type, "12", "26", lineColor, legendEff3)
        
        #if "MuFlatPt_" in fileDir:
        logScalePadNum = 3
        if "0x0006" in fileDir:
            drawEff(c4, effFile, type, "12", "5", lineColor, None)
        else :
            drawEff(c4, effFile, type, "12", "5", lineColor, None)
            
        logScalePadNum = 4
        if "0x0006" in fileDir:
            drawEff(c5, effFile, type, "12", "10", lineColor, None)
        else :
            drawEff(c5, effFile, type, "12", "10", lineColor, None)    
        
        
    if type == "nn_omtf" :
        logScalePadNum = 0
        print (c1.GetName() )
        drawEff(c1, effFile, type, quality, "22", lineColor, legendEff1, pTresh)
        logScalePadNum = 1
        drawEff(c2, effFile, type, quality, "24", lineColor, legendEff2, pTresh)
        logScalePadNum = 2
        drawEff(c3, effFile, type, quality, "42", lineColor, legendEff3, pTresh)
        
        if "MuFlatPt_" in fileDir:
            logScalePadNum = 3
            drawEff(c4, effFile, type, "12", "10", lineColor, None)
    
    if type == "omtf_patsKB" :
        logScalePadNum = 0
        drawEff(c1, effFile, "omtf", "12", "18", lineColor, legendEff1)
        logScalePadNum = 1
        drawEff(c2, effFile, "omtf", "12", "20", lineColor, legendEff2)
        logScalePadNum = 2
        drawEff(c3, effFile, "omtf", "12", "24", lineColor, legendEff3)
        
        if "MuFlatPt_" in fileDir:
            logScalePadNum = 3
            drawEff(c4, effFile, type, "12", "10", lineColor, None)
        
        
    #c5.cd(2)
    canvas_rate.cd(2)
    if type == "omtf_patsKB" :
        drawEffVsEta(effFile, "omtf", quality, lineColor)
    else :    
        drawEffVsEta(effFile, type, quality, lineColor)
    c5.Update()
     
    first = False


doLogScale = False

drawEffs('t21a__Patterns_0x00012/', "omtf_v1", "12", kBlack)
drawEffs('t21a__Extrapl_Patterns_t17_gpFinalize10/', "omtf_v1", "12", kRed)
#drawEffs('t21a__Extrapl_Patterns_t17_gpFinalize11/', "omtf_v1", "12", kRed)
#drawEffs('t22__Extrapl_Patterns_t17_v0_gpFinalize10/', "omtf_v1", "12", kRed)
#drawEffs('t27__Patterns_0x00020_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kGreen)

#drawEffs('t27a__Patterns_0x00020_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kMagenta)
#drawEffs('t27a__Patterns_0x00021_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kMagenta)

#drawEffs('t27a__Patterns_0x00020_classProb20_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kBlue)
#drawEffs('t27a__Patterns_0x00021_classProb20_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kBlue)

#drawEffs('t27a__Patterns_0x00020_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kGreen)
#drawEffs('t27a__Patterns_0x00021_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kGreen)

#drawEffs('t27b__Patterns_0x00020_classProb21_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kGreen)
#drawEffs('t27b__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kBlue)


drawEffs('t27a__Patterns_0x00020_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kGreen)
drawEffs('t27a__Patterns_0x00021_classProb22_ExtraplMB1nadMB2SimplifiedFP_t27__mcWaw2023_OneOverPt_and_iPt2/', "omtf_v1", "12", kBlue)

#  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
doLogScale = False

c1.cd(1)
legendEff1.Draw()

c2.cd(1)
legendEff2.Draw()

c3.cd(1)
legendEff3.Draw()

# c1.cd(1).Modified()
# c1.cd(1).Update()
# 
# c1.cd(2).Modified()
# c1.cd(2).Update()

#################################
first = True
 
#c2 = TCanvas('canvas_rate_1', 'canvas_rate', 800, 100, 500, 500)

rate_c1 = canvas_rate.cd(1)

rate_c1.SetGridx()
rate_c1.SetGridy()
rate_c1.SetLogy()
#rate_c1.cd()
rate_c1.SetLeftMargin(0.15)

 
legendRate = TLegend(0.3, 0.65, 0.7, 0.8)

legend = legendRate

 #legend.SetHeader(header.c_str())
# leg -> SetBorderSize(0);
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.SetMargin(0.2)


#drawRate('t23_phase2_with_extrapolation_DTQ_2_2__MinBias_Phase2Spring23_PU140/', "omtf", "OMTF_DTQ_2_2", "12", kBlack)
#drawRate('t23_phase2_with_extrapolation_NN_FP_v217_DTQ_2_2__MinBias_Phase2Spring23_PU140/', "omtf", "NN_FP_v217_DTQ_2_2", "12", kRed)

legend.Draw()

c1.Modified()
c1.Update()
 
c2.Modified()
c2.Update()

c3.Modified()
c3.Update()

c4.Modified()
c4.Update()

c5.Modified()
c5.Update()

canvas_rate.Modified()
canvas_rate.Update()


if False :
    fileName = makeUniqueFileName("/eos/user/k/kbunkow/public/omtf_nn_plots/", "eff_1_.png")
    print ("saving as " + fileName)
    c1.SaveAs(fileName)
    c2.SaveAs(fileName.replace("eff_1_", "eff_2_"))
    c3.SaveAs(fileName.replace("eff_1_", "eff_3_"))
    c4.SaveAs(fileName.replace("eff_1_", "eff_4_"))
    c5.SaveAs(fileName.replace("eff_1_", "effVsEta_"))
    rate_c1.SaveAs(fileName.replace("eff_1_", "rate_"))

# c3 = TCanvas('canvas_efficiency_rate_1', 'canvas_efficiency_rate_1', 200, 10, 950, 500)
# c3.Divide(2, 1)
# c3.cd(1)
# c3.cd(1).SetGridx()
# c3.cd(1).SetGridy()
# c3.cd(1)
# 
# c3.Modified()
# c3.Update()

input("Press ENTER to exit")

#execfile('ratePlots.py')
