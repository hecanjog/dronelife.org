# dronelife.org

The new dronelife.org forums

## Installation

### Database setup

First, install postgresql
    
Switch to the postgres user (this will be created when postgres is installed)

    $ sudo su - postgres

As the postgres user, create a new 'dronelife' user:

    [postgres]$ createuser --interactive --pwprompt
    Enter the name of role to add: dronelife
    Enter password for new role:
    Enter it again:
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) y
    Shall the new role be allowed to create more new roles? (y/n) n

Exit the postgres user shell

    [postgres]$ exit

Create a new 'dronelife' database giving read/write permission to the dronelife user:

    $ createdb dronelife -U dronelife

Set the sqlalchemy connection uri environment variable by adding the following to your .bashrc (replacing password with the password you set for your user!)

    export DRONELIFE_SQLALCHEMY_DATABASE_URI='postgresql://dronelife:password@localhost/dronelife'

### Application setup

First, make sure you have python 2.7 and pip installed

To install dronelife globally, from the src directory run:

    sudo python setup.py develop

Which will install dronelife in 'develop' mode, which lets you hack on the code without having to reinstall the module on every change.
In production, `install` should be used instead of `develop`.

To run the app (don't do this in production) just:

    python run.py

Which will start a local server. The site will be accessable from `http://127.0.0.1:5000`

