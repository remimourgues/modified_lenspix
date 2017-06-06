import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from scipy import interpolate
import camb
import correlations #camb is not importing correlations properly, so do it manually
from savitzky_golay import *

#sim vs theory
#primary_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/ffp10_alm_from_scalCls.fits"
#phi_alm_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/may29_n2048_phi_restricted_alm.fits"
#lensed_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/may29_kappa_restricted_ffp10_scalCls_lensed.fits"
#kappa_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/cl_kappa_restricted.txt"
#primary_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/cls/ffp10_scalCls.dat"
#lensed_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/may29_theory_lensed.dat"
#lens_lmax = 2000

#nonlinear0 run
#primary_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/ffp10_unlensed_scl_cmb_000_alm.fits"
#phi_alm_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_nonlinear0_phi_for_julian_cmb.fits"
#lensed_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_nonlinear0_julian_cmb_lensed.fits"
#kappa_theory_cl_file = "/scratch2/r/rbond/engelen/peakpatch/data/cl_kappa_restricted_nonlinear0.txt"
#primary_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/cls/ffp10_scalCls.dat"
#lensed_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/jun1_nonlinear0_theory_lensed.dat"
#lens_lmax = 4000
#kappa_map_file = "/scratch2/r/rbond/phamloui/lenspix_files/kappa_maps/jun1_nonlinear0_kappa_for_julian_cmb.fits"

#nonlinear3 run
#primary_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/ffp10_unlensed_scl_cmb_000_alm.fits"
#phi_alm_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_nonlinear3_phi_for_julian_cmb.fits"
#lensed_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_nonlinear3_julian_cmb_lensed.fits"
#kappa_theory_cl_file = "/scratch2/r/rbond/engelen/peakpatch/data/cl_kappa_restricted_nonlinear3.txt"
#primary_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/cls/ffp10_scalCls.dat"
#lensed_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/jun1_nonlinear3_theory_lensed.dat"
#lens_lmax = 4000
#kappa_map_file = "/scratch2/r/rbond/phamloui/lenspix_files/kappa_maps/jun1_nonlinear3_kappa_for_julian_cmb.fits"

#only halofit full z
primary_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/ffp10_unlensed_scl_cmb_000_alm.fits"
phi_alm_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_all_z_phi_with_halofit.fits/"
lensed_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_all_z_halofit_julian_cmb_lensed.fits"
kappa_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/all_z_kappa_with_halofit.dat"
primary_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/cls/ffp10_scalCls.dat"
lensed_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/jun1_full_z_halofit_theory_lensed.dat"
lens_lmax = 4000
#kappa_map_file = "/scratch2/r/rbond/phamloui/lenspix_files/kappa_maps/all_z_kappa_with_halofit.fits"

#interp_factor = 2
#primary_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/ffp10_unlensed_scl_cmb_000_alm.fits"
#phi_alm_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_all_z_phi_with_halofit.fits/"
#lensed_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun6_camb_all_z_julian_cmb_lensed_interp_factor_2.fits"
#kappa_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/all_z_kappa_with_halofit.dat"
#primary_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/cls/ffp10_scalCls.dat"
#lensed_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/jun1_full_z_halofit_theory_lensed.dat"
#lens_lmax = 4000

#interp_factor = 3
#primary_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/ffp10_unlensed_scl_cmb_000_alm.fits"
#phi_alm_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_all_z_phi_with_halofit.fits/"
#lensed_file = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun6_camb_all_z_julian_cmb_lensed_interp_factor_3.fits"
#kappa_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/all_z_kappa_with_halofit.dat"
#primary_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/FromNERSC/cls/ffp10_scalCls.dat"
#lensed_theory_cl_file = "/scratch2/r/rbond/phamloui/lenspix_files/jun1_full_z_halofit_theory_lensed.dat"
#lens_lmax = 4000

print "Loading primary sim and theory..."
primary_alm = hp.read_alm(primary_file)
theory_TT_ell, theory_CL_TT = np.loadtxt(primary_theory_cl_file, usecols=(0,1), unpack=True) # l(l+1)/2 factor included

theory_TT_ell = np.insert(theory_TT_ell, 0, 1)
theory_TT_ell = np.insert(theory_TT_ell, 0, 0)
theory_CL_TT = np.insert(theory_CL_TT, 0, 0)
theory_CL_TT = np.insert(theory_CL_TT, 0, 0)
theory_CL_TT = theory_CL_TT / 1e12
#print theory_CL_TT
#print theory_CL_TT.shape
lmax = hp.Alm.getlmax(len(primary_alm)) if hp.Alm.getlmax(len(primary_alm)) < len(theory_TT_ell)-1 else len(theory_TT_ell)-1 #change this later
#print lmax
theory_TT_ell = theory_TT_ell[0:lmax+1]
theory_CL_TT = theory_CL_TT[0:lmax+1]

# load theoretical kappa from alex
#print "Loading kappa..."
#theory_KK_ell_raw, theory_CL_KK = np.loadtxt(kappa_theory_cl_file, usecols=(0,1), unpack=True)
#theory_KK_ell_interp = np.arange(0,lens_lmax+1)
#kappa_interp_func = interpolate.splrep(theory_KK_ell_raw, theory_CL_KK, s=0)
#theory_CL_KK_interp = interpolate.splev(theory_KK_ell_interp, kappa_interp_func, der=0)
#theory_CL_KK_interp = np.pad(theory_CL_KK_interp, (0, lmax-lens_lmax), 'constant', constant_values=(0,0)) #camb convolution needs equal lmax, so just pad with zeros
#theory_KK_ell_interp = np.arange(0, lmax+1)
##not actually kappa, values are stored as C_phi
#CMB_outputscale = 7.4311e12
##theory_KK_ell_interp = np.insert(theory_KK_ell, (0,0), (0,1)) #missing ell=0,1, add zeros
##theory_CL_KK_interp = np.insert(theory_CL_KK, (0,0), (0,0))
#theory_CL_KK_interp = theory_CL_KK_interp / (theory_KK_ell_interp**4) / CMB_outputscale #converts to C_L^phi
#theory_CL_KK_interp = theory_CL_KK_interp * (theory_KK_ell_interp*(theory_KK_ell_interp+1)/2.0)**2 #now its actually kappa
#theory_CL_KK_interp[0] = 0
#theory_CL_KK_interp[1] = 0
#theory_KK_ell = theory_KK_ell_interp[0:lmax+1]
#theory_CL_KK = theory_CL_KK_interp[0:lmax+1]

# get "theoretical" CL_KK by smoothing power spectrum from map
#print "Loading kappa map..."
#kappa_map = hp.read_map(kappa_map_file)
#kappa_cl = hp.anafast(kappa_map, lmax=lens_lmax)
#kappa_ell = np.arange(0, lmax+1)
#kappa_cl = savitzky_golay(kappa_cl,75,3) #smooth cl for theory approximation
#kappa_cl = np.pad(kappa_cl, (0, lmax-lens_lmax), 'constant', constant_values=(0,0))
#theory_KK_ell = kappa_ell #too lazy to refactor, just replace variables here
#theory_CL_KK = kappa_cl

# load already-made CL_KK file
theory_CL_KK = hp.read_cl(kappa_theory_cl_file)
theory_CL_KK = np.pad(theory_CL_KK, (0, lmax-lens_lmax), 'constant', constant_values=(0,0)) #camb convolution needs equal lmax, so just pad with zeros
theory_KK_ell = np.arange(0,lmax+1)

print "Loading lensed map (sim)..."
lensed_map = hp.read_map(lensed_file)
simulation_CL_TT_lensed = hp.anafast(lensed_map, lmax=lmax)
nside = hp.get_nside(lensed_map)
simulation_TT_ell = np.arange(0, lmax+1)

print "converting theory kappa to phi..." #for camb convolution
theory_CL_PP = theory_CL_KK / (theory_KK_ell*(theory_KK_ell+1)/2.0)**2
theory_PP_ell = np.arange(0, lmax+1)
print theory_CL_PP.shape
#kappa_theory_alm = hp.synalm(theory_CL_KK)
#theory_KK_ell, m = hp.Alm.getlm(hp.Alm.getlmax(len(kappa_theory_alm)))
#phi_theory_alm = kappa_theory_alm * (2.0 / (theory_KK_ell*(theory_KK_ell+1.0)))
#phi_theory_alm[theory_KK_ell==0] = 0
#theory_CL_PP = hp.alm2cl(phi_theory_alm)
#theory_PP_ell = np.arange(theory_CL_PP.size)

print "include ell factors..."
#theory_CL_TT = theory_TT_ell * (theory_TT_ell+1) * theory_CL_TT / (2*np.pi)
theory_CL_PP = (theory_PP_ell * (theory_PP_ell + 1))**2 * theory_CL_PP / (2*np.pi)
simulation_CL_TT_lensed = simulation_TT_ell * (simulation_TT_ell + 1) * simulation_CL_TT_lensed / (2*np.pi)# * (simulation_TT_ell*(simulation_TT_ell+1)/4.0)

#smooth the spectra
#primary_cl = savitzky_golay(primary_cl, 75, 3)
#phi_cl = savitzky_golay(phi_cl, 75, 3)
simulation_CL_TT_lensed = savitzky_golay(simulation_CL_TT_lensed, 75, 3)

#print theory_TT_ell
#print theory_CL_TT.shape

#fill EE,BB,TE with zeroes
TEB_cls = np.array([[theory_CL_TT[_l], 0, 0, 0] for _l in theory_TT_ell])
print TEB_cls.shape
#print "starting lensing convolution..."
#lensed_theory_TEB = correlations.lensed_cls(TEB_cls, theory_CL_PP)
#theory_CL_TT_lensed = np.array([_l[0] for _l in lensed_theory_TEB])
#print "writing camb cl..."
#hp.write_cl(lensed_theory_cl_file, theory_CL_TT_lensed)
print "reading theory cl..."
theory_CL_TT_lensed = hp.read_cl(lensed_theory_cl_file)
theory_TT_ell_lensed = np.arange(len(theory_CL_TT_lensed))

#fractional differences
print "calculating differences..."
lenspix_vs_primary = (simulation_CL_TT_lensed - theory_CL_TT) / theory_CL_TT
#camb_vs_lenspix = (simulation_CL_TT_lensed - theory_CL_TT_lensed) / theory_CL_TT_lensed
camb_vs_primary = (theory_CL_TT_lensed - theory_CL_TT) / theory_CL_TT

plt.figure()
plt.title("Theory vs Sim - Power Spectra", fontsize=18)
plt.xlabel(r'$l$', fontsize=30)
plt.ylabel(r'$l(l+1)*C_l / 2\pi$', fontsize=30)

plt.loglog(theory_TT_ell[1:], theory_CL_TT[1:], 'b', label="Unlensed")
plt.loglog(simulation_TT_ell[1:], simulation_CL_TT_lensed[1:], 'r', label="Simulation")
plt.loglog(theory_TT_ell_lensed[1:], theory_CL_TT_lensed[1:], 'g', label="Theory")

plt.grid()
legend2 = plt.legend(loc="lower left", shadow=True)
frame2 = legend2.get_frame()
frame2.set_facecolor('0.90')

plt.figure()
plt.subplot(211)
plt.title("Theory vs Sim - Fractional Differences", fontsize=18)
plt.xlabel(r"$l$", fontsize=30)
plt.ylabel(r'$\Delta C_l / C_l$', fontsize=30)
plt.plot(theory_TT_ell[1:], lenspix_vs_primary[1:], 'r', label="Simulation vs Unlensed")
plt.plot(theory_TT_ell[1:], camb_vs_primary[1:], 'g', label="Theory vs Unlensed")
#plt.ylim([-0.1, 0.1])
legend3 = plt.legend(loc="lower left", shadow=True)
frame3 = legend3.get_frame()
frame3.set_facecolor('0.90')
plt.grid()
plt.subplot(212)
plt.title("Theory vs Sim - Differences of Fractional Differences", fontsize=18)
plt.xlabel(r"$l$", fontsize=30)
plt.ylabel(r'$\Delta C_l / C_l$', fontsize=30)
plt.ylim([-0.1,0.1])
plt.plot(theory_TT_ell[1:], lenspix_vs_primary[1:]-camb_vs_primary[1:], 'r', label="Simulation vs Theory")
plt.grid()

plt.show()
