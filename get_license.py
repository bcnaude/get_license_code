#!/usr/bin/env python
#Change file extension from .py to .command to enable double click execution of code using the shebang.
#If needed, use py_compile.compile in Python to compile
#Be aware that the shebang won't work if .py code is compiled to .pyc


#Python code to copy license files from a license server.
#Access to software license files are needed by technical and IT support, as well as by sales and admin, to assist customers and troubleshoot certain software problems.
#The license server is accessible on the network via a VPN connection and contains thousands of license files.
#This Python program makes it easy to copy specific license files from the remote license server.
#The program checks if a network connection to the license server has been established and if the network share has been mounted on the OS.
#If the network share has not been mounted on the OS, it gives the opportunity to mount the network share from within the Python program.
#Once the connection to the license server has been verified and the network share has been mounted, license files can be copied from the license server to the user's desktop.
#It saves, and sorts, each copied license file in a list, and displays all copied license files per session, when exiting the Python Program.



import shutil, os, platform, sys, time


#Set static variables and ANSI escape codes.
server = 'LicenseServer'
new_license_path = 'NAV/ACTIVATION_CODE/'
old_license_path = 'NAV/Keys/acces'
ColourRED = '\033[91m'
ColourGREEN  = '\33[32m'
ColourBLUE="\033[0;34m"
ColourEND = '\033[0m'



def check_ping():
    #Check to see if the license server is responding.
    response = os.system("ping -c 1 " + server + " >/dev/null 2>&1")
    if response == 0:
        #license server can be reached on the network.    
        pingstatus = True
    else:
        #license server cannot be reached on the network.
        pingstatus = False
        print()
        print(ColourRED + 'Unable to connect to the server at ' + server + ColourEND)
        print(ColourRED + 'Check network connection. If VPN is needed make sure it is active.' + ColourEND)
        print()
        print('No network connection to server. Exiting program.')
        print()
        display_all_copied_licenses()
        sys.exit()
        
    return pingstatus



def mount_network_share(alt_mount,os_type):

        #Provide option to try and connect to server or to quit.
        print('You can use the OS to connect to ' + server + ' or try to connect from within this program.')
        print()
        want_to_mount = input('Do you want to try to connect to connect to the server now? (Y/N): ').lower()
        print()
        while want_to_mount != 'y' and want_to_mount != 'n':
            print('You have to enter y or n.')
            want_to_mount = input('Do you want to try to connect to connect to the server now? (Y/N): ').lower()
            print()
         
        #Create mount point folder on the OS if it does not exist already.
        if want_to_mount == 'y':
            if not os.path.exists(alt_mount):
                os.makedirs(alt_mount,0755)
                
            #Get login username for the license server.
            username = str(input('Please type your login username at ' + server + ': '))

            #Find out from what OS type you are trying to connect to the license server and mounts the network share.
            print('Attempting to connect to ' + server + '...')
            if os_type == 'Darwin':
                os.system('mount_smbfs //' + username + '@' + server +'/Common' + ' ' + alt_mount)
            elif os_type == 'Linux':
                os.system('sudo mount.cifs ' + '//' + server + '/Common/' + ' ' + alt_mount + ' -o user=' + username)
            elif os_type == 'Windows':
                os.system('net use z: \\' + server + '\Common')
            else:
                print(str(os_type) + ' not supported!')
			

            if not os.path.ismount(alt_mount):
                print(ColourRED + 'Unable to connect to the server.' + ColourEND)
                print()
                exit()
            elif os.path.ismount(alt_mount):
                print(ColourGREEN + 'Succesfully connected to ' + server + ' !' + ColourEND)
                print()
                
        elif want_to_mount == 'n':
            print('No network connection to server. Exiting program.')
            print()
            exit()  



def check_server_connected(default_mount, alt_mount):

    #Check if the license server is responding to a ping.
    check_ping()

    #Check to see if default mount points are found on the OS.
    if not os.path.ismount(default_mount) and not os.path.ismount(alt_mount):
        print()
        print(ColourRED + 'Could not find a connection to server ' + server + ' at default mount point ' + default_mount + ColourEND)
        print('Make sure that you are connected to server ' + server + ' before trying to download license files.')
        print()

        #If not connected to server, call the connect function.
        mount_network_share(alt_mount,os_type)

    else:
        print(ColourGREEN + 'You are connected to ' + server + ColourEND)
        print()



def display_all_copied_licenses():

    copied_licenses.sort()
    
    #Remove duplex license numbers.
    new_list = []
    
    for i in copied_licenses:
        if i not in new_list:
            new_list.append(i)
    
    #Display all copied licenses.
    print()
    print('License files copied in this session:')
    print()
    for j in new_list:
        print(j)
    print()
        


def function_copy_again():
    copy_again = input('Do you want to download another license? (Y/N): ').lower()
    print()
    while copy_again != 'y' and copy_again != 'n':
        print('You have to enter y or n.')
        copy_again = input('Do you want to download another license? (Y/N): ').lower()
        print()
    if copy_again == 'y':
        os.system('clear')
        copy_license(home_folder, local_mount_point)
        print()
    elif copy_again == 'n':
        display_all_copied_licenses()
        sys.exit()



def copy_license(home_folder, local_mount_point):

    #Request the access number to download.
    print()
    access_num = input('What is the Access Number? ').strip()

    #Check connection before attemting the copy as part of fault tolerance.
    check_ping()
    
    #Copy the license file.
    try:
        shutil.copy(local_mount_point + new_license_path + access_num + '.txt', home_folder + '/Desktop')
        print()
        print(ColourGREEN + '     -> License file ' + str(access_num) + '.txt copied to Desktop.' + ColourEND)
        print()
        #Add copied license number to list.
        copied_licenses.append(access_num)
        
    except:

        try:
            print()
            print('Could not find license file ' + access_num + '.txt. Searching for older license...')
            print()

            #Check connection before attemting the copy as part of fault tolerance.
            check_ping()
            
            shutil.copy(local_mount_point + old_license_path + access_num + '.txt.gz', home_folder + '/Desktop')
            print()
            print(ColourGREEN+ '     -> License file ' + str(access_num) + '.txt.gz copied to Desktop.' + ColourEND)
            print()
            #Add copied license number to list.
            copied_licenses.append(access_num)

        except Exception as error_message:
            
            print()
            print(ColourRED + 'An error occurred during file copy:' + ColourEND)
            print(ColourRED + str(error_message) + ColourEND)
            print()

            check_server_connected(default_mount_point, alt_mount_point)

    
    #Ask if another license is to be copied.
    function_copy_again()



                
#Program Start:

#Clear the terminal screen.
os.system('clear')
print(ColourBLUE + 'Program: get_license | Version: 1.0' + ColourEND)
time.sleep(.500)
os.system('clear')

#Create list to contain all downloaded license numbers in a session.
copied_licenses = []

#Find the home folder for the specific user.
home_folder = os.path.expanduser('~')

#Check OS type.
os_type = platform.system()

#Set default or alternative folders depending on OS type.
if os_type == 'Darwin':
    default_mount_point = '/Volumes/Common/'
    alt_mount_point = home_folder + '/Common/'
elif os_type == 'Linux':
    default_mount_point = '/mnt/Common/'
    alt_mount_point = home_folder + '/Common/'
elif os_type == 'Windows':
    default_mount_point = 'y:'
    alt_mount_point = home_folder + 'z:'

#Check if the server is connected.
check_server_connected(default_mount_point, alt_mount_point)

#Define local mount point.
if os.path.ismount(default_mount_point):
    local_mount_point = default_mount_point
if os.path.ismount(alt_mount_point):
    local_mount_point = alt_mount_point

#Copy the license.
copy_license(home_folder, local_mount_point)

#Ask if another license is to be copied.
function_copy_again
