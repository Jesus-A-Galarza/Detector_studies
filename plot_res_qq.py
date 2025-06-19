import sys, array, ROOT, math, os, copy
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

def compute_res(input_file, hist_name, output_name, plotGauss=True):
    fIn = ROOT.TFile(input_file)
    hist = fIn.Get(hist_name)

    rebin = 1
    hist = hist.Rebin(rebin)

    probabilities = np.array([0.001, 0.999, 0.84, 0.16], dtype='d')
    quantiles = np.array([0.0, 0.0, 0.0, 0.0], dtype='d')
    hist.GetQuantiles(4, quantiles, probabilities)
    xMin, xMax = min([quantiles[0], -quantiles[1]]), max([-quantiles[0], quantiles[1]])
    res = 100. * 0.5 * (quantiles[2] - quantiles[3])

    rms, rms_err = hist.GetRMS() * 100., hist.GetRMSError() * 100.

    gauss = ROOT.TF1("gauss2", "gaus", xMin, xMax)
    gauss.SetParameter(0, hist.Integral())
    gauss.SetParameter(1, hist.GetMean())
    gauss.SetParameter(2, hist.GetRMS())
    hist.Fit("gauss2", "RQ")

    sigma, sigma_err = gauss.GetParameter(2) * 100., gauss.GetParError(2) * 100.
    gauss.SetLineColor(ROOT.kRed)
    gauss.SetLineWidth(3)

    yMin, yMax = 0, 1.3 * hist.GetMaximum()
    canvas = ROOT.TCanvas("canvas", "", 1000, 1000)
    canvas.SetTopMargin(0.055)
    canvas.SetRightMargin(0.05)
    canvas.SetLeftMargin(0.15)
    canvas.SetBottomMargin(0.11)

    dummy = ROOT.TH1D("h", "h", 1, xMin, xMax)
    dummy.GetXaxis().SetTitle("(p_{reco} #minus p_{gen})/p_{gen}")
    dummy.GetYaxis().SetTitle("Events / bin")
    dummy.SetMaximum(yMax)
    dummy.SetMinimum(yMin)

    # Axis styling
    for axis in [dummy.GetXaxis(), dummy.GetYaxis()]:
        axis.SetTitleFont(43)
        axis.SetTitleSize(40)
        axis.SetLabelFont(43)
        axis.SetLabelSize(20)
    dummy.GetXaxis().SetTitleOffset(1.6)
    dummy.GetYaxis().SetTitleOffset(2.0)

    dummy.Draw("HIST")
    hist.Draw("SAME HIST")
    if plotGauss:
        gauss.Draw("SAME")

    canvas.SetGrid()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    ROOT.gPad.RedrawAxis()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.DrawLatex(0.2, 0.9, f"Mean/RMS(#times 100) = {hist.GetMean():.4f}/{rms:.4f}")
    latex.DrawLatex(0.2, 0.85, f"Resolution = {res:.4f} %")
    if plotGauss:
        latex.DrawLatex(0.2, 0.80, f"Gauss #mu/#sigma(#times 100) = {gauss.GetParameter(1):.4f}/{sigma:.4f}")

    canvas.SaveAs(f"{output_name}.png")
    canvas.SaveAs(f"{output_name}.pdf")
    canvas.Close()

    return rms, rms_err, sigma, sigma_err, res


if __name__ == "__main__":

    input_file = "output/IDEA_1.0T_Zuu_ecm91p2.root"

    # --- Plot for resolution ---
    compute_res(
        input_file=input_file,
        hist_name="qq_res",
        output_name="resolution_IDEA_1.0T_Zuu_ecm91p2"
    )
