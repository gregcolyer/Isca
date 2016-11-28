#Function to load interpolated data on pressure levels for multiple months
#Copied from RG on 29/03/16

import subprocess
import sys
import os

def plevel_call(nc_file_in,nc_file_out, var_names = '-a', p_levels='default'):

	check_gfdl_directories_set()

        interper = './plevel.sh'
        nc_file = ' -i '+nc_file_in
        out_file = ' -o '+nc_file_out
        if p_levels == 'model':
            plev = ' -p "2 9 18 38 71 125 206 319 471 665 904 1193 1532 1925 2375 2886 3464 4115 4850 5679 6615 7675 8877 10244 11801 13577 15607 17928 20585 23630 27119 31121 35711 40976 47016 53946 61898 71022 81491 93503" '
            command = interper + nc_file + out_file + plev + var_names
	elif p_levels=='default':
            command = interper + nc_file + out_file + ' ' + var_names
        else:
	    plev=p_levels
	    command = interper + nc_file + out_file + plev +' '+ var_names
        print command
        subprocess.call([command], shell=True)

def daily_average(nc_file_in, nc_file_out):
	subprocess.call('cdo daymean '+nc_file_in+' '+nc_file_out, shell=True)

def two_daily_average(nc_file_in, nc_file_out, avg_or_daily):
	if avg_or_daily=='daily':
		number_of_timesteps=2
	elif avg_or_daily=='6hourly':
		number_of_timesteps=8

	subprocess.call('cdo timselmean,'+str(number_of_timesteps)+' '+nc_file_in+' '+nc_file_out, shell=True)

def join_files(files_in, file_name_out):

	subprocess.call('cdo mergetime '+files_in+' '+file_name_out, shell=True)

def check_gfdl_directories_set():

	try:
	    GFDL_BASE = os.environ['GFDL_BASE']
	    GFDL_WORK = os.environ['GFDL_WORK']
	    GFDL_DATA = os.environ['GFDL_DATA']
	except Exception, e:
	    print('Exiting: Environment variables GFDL_BASE, GFDL_WORK, GFDL_DATA are not set')
	    sys.exit(0)