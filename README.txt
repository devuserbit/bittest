

Before all things please take a look under external/ and read the README.txt file!

To scaffold a HSM call the hsm_template.py script with the path to your hsm description XML file.
To see a example of putting together a decent XML file take a peek at the default_hsm.xml

All other errors will be hopefully recognised by the script and prevent you from doing something stupid.

You can also create a default_hsm.xml in the desired folder so you don't start from scratch. For that pass the -n flag when 
calling the hsm_template.py script. 

	Usage:


        	hsm_template.py [-n,-v] path

                path          Path to the folder in which the HSM Servie should be created
                -n            Create default hsm description xml in the given folder path
                -v            Verbose

Be good and have fun!