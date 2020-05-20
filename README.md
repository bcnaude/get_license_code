An example of structured Python programming. My Python code to copy license files from a license server.

The license server contains thousands of license files, and this Python program makes it easy to copy specific license files from the server.

It checks if a connection to the license server has been established and if the network share has been mounted. If not, it gives the opportunity to mount the network share from within the Python program.

Once connection to the license server has been verified and the network share has been mounted, the license files can be copied from the license server to the user's desktop.

It saves, and sorts, each copied license file in a list, and displays all copied license files per session, when exiting the Python Program.
