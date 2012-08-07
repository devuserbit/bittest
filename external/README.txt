
To be able to use the HSMTemplate system you must first install this files in the following order:

	
	1. setuptools 0.6c11
	--------------------


	1.1 Installation Instructions - Windows
	---------------------------------------

		32-bit version of Python
		------------------------

		Install setuptools using the provided .exe installer.

		
		64-bit versions of Python
		-------------------------

		Download ez_setup.py and run it; it will download the appropriate .egg file and install it for you. 
		(Currently, the provided .exe installer does not support 64-bit versions of Python for Windows, 
		 due to a distutils installer compatibility issue)
			
		NOTE: Regardless of what sort of Python you're using, if you've previously installed older versions 
		of setuptools, please delete all setuptools*.egg and setuptools.pth files from your system's site-packages 
		directory (and any other sys.path directories) FIRST.

		If you are upgrading a previous version of setuptools that was installed using an .exe installer, 
		please be sure to also uninstall that older version via your system's "Add/Remove Programs" feature, 
		BEFORE installing the newer version.

		Once installation is complete, you will find an easy_install.exe program in your Python Scripts subdirectory. 
		Be sure to add this directory to your PATH environment variable, if you haven't already done so.


	
	2. Cheetah 2.4.4
	----------------


	2.1 Installation - Windows
	--------------------------

		To install Cheetah in your system-wide Python library:

		Login as a user with privileges to install system-wide Python packages. 
		On POSIX systems (AIX, Solaris, Linux, IRIX, etc.), the command is normally 'su root'. 
		On non-POSIX systems such as Windows NT, login as an administrator.
	
		Run 
		
			python setup.py install 
		
		at the command prompt.

		The setup program will install the wrapper script cheetah to wherever it usually puts 
		Python binaries ("/usr/bin/", "bin/" in the Python install directory, etc.)
		Cheetah's installation is managed by Python's Distribution Utilities ('distutils'). 
		There are many options for customization. Type ``python setup.py help'' for more information.

		To install Cheetah in an alternate location - someplace outside Python's site-packages/ directory, use one of these options:

    		python setup.py install --home /home/tavis 
    		python setup.py install --install-lib /home/tavis/lib/python

		Of course the installation folder must be in your Python path in order for Python to find Cheetah.


Have fun!