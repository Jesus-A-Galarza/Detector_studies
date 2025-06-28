import ROOT
import os
from array import array

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# files
files = [
    ("output/IDEA_0.5T_Zuu_ecm91p2.root", 0.5),
    ("output/IDEA_1.0T_Zuu_ecm91p2.root", 1.0),
    ("output/IDEA_1.5T_Zuu_ecm91p2.root", 1.5),
    ("output/IDEA_2.0T_Zuu_ecm91p2.root", 2.0),
    ("output/IDEA_2.5T_Zuu_ecm91p2.root", 2.5),
    ("output/IDEA_3.0T_Zuu_ecm91p2.root", 3.0),
]

bfields = []
means = []
rmss = []

for path, bfield in files:
    file = ROOT.TFile.Open(path)
    hist = file.Get("qq_res")

    hist.Rebin(50)
    mean = hist.GetMean()
    rms = hist.GetRMS()

    bfields.append(bfield)
    means.append(mean)
    rmss.append(rms)

    file.Close()

bfields_array = array("d", bfields)
means_array = array("d", means)
rmss_array = array("d", rmss)

# create graphs
graph_mean = ROOT.TGraph(len(bfields), bfields_array, means_array)
graph_rms = ROOT.TGraph(len(bfields), bfields_array, rmss_array)

# mean
graph_mean.SetTitle("Mean of qq_res in IDEA vs Magnetic Field;B-field (T);Mean of IDEA")
graph_mean.SetMarkerStyle(20)
graph_mean.SetMarkerColor(ROOT.kBlue)
graph_mean.SetLineColor(ROOT.kBlue)

c1 = ROOT.TCanvas("c1", "Mean vs B-field", 800, 600)
graph_mean.Draw("APL")
os.makedirs("plots", exist_ok=True)
c1.SaveAs("plots/qq_res_mean_vs_bfield_IDEA.png")
c1.SaveAs("plots/qq_res_mean_vs_bfield_IDEA.pdf")

# RMS
graph_rms.SetTitle("RMS of qq_res in IDEA vs Magnetic Field;B-field (T);RMS of IDEA")
graph_rms.SetMarkerStyle(21)
graph_rms.SetMarkerColor(ROOT.kRed)
graph_rms.SetLineColor(ROOT.kRed)

c2 = ROOT.TCanvas("c2", "RMS vs B-field", 800, 600)
graph_rms.Draw("APL")
c2.SaveAs("plots/qq_res_rms_vs_bfield_IDEA.png")
c2.SaveAs("plots/qq_res_rms_vs_bfield_IDEA.pdf")
