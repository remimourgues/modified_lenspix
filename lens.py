from kappa2phi import kap2phi
import numpy as np
import healpy as hp
from astropy.io import fits
import subprocess
import argparse

def checkFitsType(fileName):
    '''
    Check if FITS file is a map or alm.
    '''
    hdulist = fits.open(fileName)
    try:
        nside = hdulist[1].header['NSIDE']
        fitsType = 'map'
    except KeyError:
        #assume alm
        fitsType = 'alm'
    except Exception:
        raise
    hdulist.close()
    return fitsType

def appendToFilename(filename, newStr):
    return "{0}_{2}.{1}".format(*filename.rsplit('.', 1) + [newStr])

#at simlens step, will need a phi and primary alm -- check inputs here
parser = argparse.ArgumentParser(description='Lens CMB primary.')
parser.add_argument('input_field_kappa', help='filename of the field kappa file (pref. HEALPix map)')
#parser.add_argument('input_halo_kappa', help='filename of the halo kappa file (HEALPix map)')
parser.add_argument('input_primary', help='filename of the unlensed primary file (pref. HEALPix alm)')
parser.add_argument('output_phi', help='filename of the outputted phi file (HEALPix alm)')
parser.add_argument('output_lensed', help='filename of the outputted lensed file (HEALPix map)')
parser.add_argument('-ol', '--output_lmax', help='new lmax for the lensed map')
parser.add_argument('-np', '--num_processes', help='-np from job submission')
args = parser.parse_args()

genericParams = 'generic_params.ini'
specificParams = '/scratch2/r/rbond/phamloui/lenspix_files/output/specific_params.ini' #cant save to home directory when running this script as a job
outFileRoot = "/scratch2/r/rbond/phamloui/lenspix_files/output/jun1_julian_cmb" #used mainly for power spectra files - in the future just append _power to filenames from arguments?

if args.num_processes:
    numProc = args.num_processes
else:
    numProc = '1'

#input filenames
#fieldKappaFile = "/scratch2/r/rbond/phamloui/lenspix/kappa_maps/8Gpc_n2048_nb23_nt18_kap_halo.fits"
#haloKappaFile = "/scratch2/r/rbond/phamloui/lenspix/kappa_maps/8Gpc_n2048_nb23_nt18_kap_halo.fits"
#nlensedPrimaryFile = "/scratch2/r/rbond/phamloui/lenspix/kappa_maps/cib_fullsky_ns2048_zmin0.0_zmax1.245_nu217_13579_normalized_alm.fits"
fieldKappaFile = args.input_field_kappa
#haloKappaFile = args.input_halo_kappa
unlensedPrimaryFile = args.input_primary

#output filenames                                                                                    
#combKappaFile = outFileRoot + "8Gpc_n2048_nb23_nt18_kap_comb.fits"             
#phiAlmFile = outFileRoot + "_n2048_phi_alm.fits"                                
#phiMapFile = outFileRoot + "_n2048_phi_map.fits"                                 
phiAlmFile = args.output_phi
lensedFile = args.output_lensed

#get nside
hdulist = fits.open(fieldKappaFile)
nside = hdulist[1].header['NSIDE']
hdulist.close()

print "Creating zero map..."
zeroMapFile = "/scratch2/r/rbond/phamloui/lenspix_files/zeros_%s.fits" % (nside)
zeroMap = np.zeros(12 * (nside**2)) #create a zero map and use that in place of halo kappa, since we only have field kappa now
hp.write_map(zeroMapFile, zeroMap)
haloKappaFile = zeroMapFile

#load maps
print "Loading maps..."
fieldKappaType = checkFitsType(fieldKappaFile)
primaryType = checkFitsType(unlensedPrimaryFile)
print "Loading field kappa..."
fieldKappa = hp.read_map(fieldKappaFile)
print "Loading halo kappa..."
haloKappa = hp.read_map(haloKappaFile)
if primaryType != 'alm':
    print "Primary is map - converting to alm..."
    unlensedPrimaryMap = hp.read_map(unlensedPrimaryFile)
    unlensedPrimary = hp.map2alm(unlensedPrimaryMap)
    unlensedPrimaryFile = appendToFilename(unlensedPrimaryFile, "alm")
    hp.write_alm(unlensedPrimaryFile, unlensedPrimary)
    print "Saved new primary alm to", unlensedPrimaryFile
else:
    print "Loading primary..."
    unlensedPrimary = hp.read_alm(unlensedPrimaryFile)
#get lmax and create phi alm
lmax = kap2phi(fieldKappa, haloKappa, unlensedPrimary, phiAlmFile)
#lmax = kap2phi(fieldKappaFile, haloKappaFile, unlensedPrimaryFile, phiAlmFile)
print 'Obtained parameters NSIDE:', nside, 'and LMAX:', lmax

print 'Creating params file...'
if args.output_lmax:
    outputLmax = args.output_lmax
    print 'Output lmax set to', str(outputLmax) + '.'
else:
    outputLmax = lmax
    print 'Output lmax defaulted to input lmax', str(outputLmax) + '.'

subprocess.call(['cp', genericParams, specificParams])
#commas are used as delimiters for sed commands to avoid escaping (back)slashes -- this assumes there's no commas in the filenames
subprocess.call(['sed', '-i', 's,__NSIDEREPLACE__,' + str(nside) + ',g', specificParams])
subprocess.call(['sed', '-i', 's,__LMAXREPLACE__,' + str(lmax) + ',g', specificParams])
subprocess.call(['sed', '-i', 's,__OUTFILEROOTREPLACE__,' + outFileRoot + ',g', specificParams])
subprocess.call(['sed', '-i', 's,__OUTPUTLMAXREPLACE__,' + str(outputLmax) + ',g', specificParams])
subprocess.call(['sed', '-i', 's,__PRIMARYFILEREPLACE__,' + unlensedPrimaryFile + ',g', specificParams])
subprocess.call(['sed', '-i', 's,__PHIFILEREPLACE__,' + phiAlmFile + ',g', specificParams])
subprocess.call(['sed', '-i', 's,__LENSEDFILEREPLACE__,' + lensedFile + ',g', specificParams])
print 'Params file created.'

print 'Running simlens...'
print 'Running "mpirun -np %s ./simlens %s"' % (numProc, specificParams)
subprocess.call(['mpirun', '-np', str(numProc), './simlens', specificParams])
print 'Simlens complete.'
