import colored
import os
import shutil
import subprocess
import sys

from colored import fg, bg, attr

domainName = sys.argv[1]
confFile = domainName + '.conf'
virtualDirectory = '/var/www/' + domainName
sitesAvailableDir = '/etc/nginx/sites-available/'
sitesEnabledDir = '/etc/nginx/sites-enabled/'

# copy template to sites-available
confExists = os.path.isfile(sitesAvailableDir+confFile)

if confExists:
        print ('#1 Copy nginx vhost config file : %s FAILED %s' % (fg('red'), attr(0)))
else:
        subprocess.call(['clear'])
        shutil.copy ('template', sitesAvailableDir)
        print ('#1 Copy nginx vhost config file : %s DONE %s' % (fg('green'), attr(0)))

        # rename template
        os.rename(sitesAvailableDir+'template', sitesAvailableDir+confFile)
        print ('#2 Rename nginx vhost config file : %s DONE %s' % (fg('green'), attr(0)))

        #replace place holders with domain name
        with open(sitesAvailableDir+confFile) as f:
                newText=f.read().replace('domain.com', domainName)

        with open(sitesAvailableDir+confFile, "w") as f:
                f.write(newText)

        print ('#3 Replace placeholders in virtual host file : %s DONE %s' % (fg('green'), attr(0)))

        os.symlink (sitesAvailableDir+confFile, sitesEnabledDir+confFile)
        print ('#4 Create sites-enabled sym link : %s DONE %s' % (fg('green'), attr(0)))

        try:
                os.mkdir(virtualDirectory)
                print ('#5 Create nginx virtual directory : %s DONE %s' % (fg('green'), attr(0)))
        except FileExistsError:
                print ('#5 Create nginx virtual directory : %s FAILED %s' % (fg('red'), attr(0)))
                exit()

        try:
                shutil.chown(virtualDirectory, user='nginx', group='nginx')
                print ('#6 Chown nginx:nginx virtual directory : %s DONE %s' % (fg('green'), attr(0)))
        except:
                print ('#6 Chown nginx:nginx virtual directory : %s FAILED %s' % (fg('red'), attr(0)))

        try:
                file = open(virtualDirectory+'/index.html', "x")
                file.write (domainName)
                print ('#7 Create test index.html : %s DONE %s' % (fg('green'), attr(0)))
        except:
                print ('#7 Create test index.html : % FAILED %s' % (fg('red'), attr(0)))

        try:
                shutil.chown(virtualDirectory+'/index.html', user='nginx', group='nginx')
                print ('#8 Chown nginx:nginx index.html : %s DONE %s' % (fg('green'), attr(0)))
        except:
                print ('#8 Chown nginx:nginx index.html : %s FAILED %s' % (fg('red'), attr(0)))

        subprocess.call(['nginx','-t'])
        subprocess.call(['systemctl','reload','nginx'])
        subprocess.call(['systemctl','status','nginx'])
	
		print ('  ' + domainName +': %s DONE %s' % (fg('yellow'), attr(0)))
