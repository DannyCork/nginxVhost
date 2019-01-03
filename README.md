# nginxVhost
A python script to create Nginx virtual hosts on linux

  - creates a vhost config file and moves it to sites-available
  - creates a symbolic link in sites-enable to the vhost config file.
  - makes a directory in /var/www
  - adds a test index.html file
  - reloads nginx
