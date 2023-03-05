# Adding New IR Components

OpenRemoteHub uses lirc to send out IR signals to devices.  To add a new device you will need to provide an lirc configuration for that device.  lirc has an extensive set of conf files that can be searched using the included scripts/irdb-get.  For instance:

``` terminal
% scripts/irdb-get find xbox
microsoft/Xbox_PG-8012.lircd.conf
```

In the above example a `find` for xbox returns a single entry.  Download the condifiguration using the below command:

``` terminal
% scripts/irdb-get download microsoft/Xbox_PG-8012.lircd.conf
Downloaded https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/microsoft/Xbox_PG-8012.lircd.conf as Xbox_PG-8012.lircd.conf
% ls *.conf
Xbox_PG-8012.lircd.conf
```

Copy the conf file with `sudo cp  Xbox_PG-8012.lircd.conf /etc/lirc/lircd.d.conf/` and then restart lirc (`sudo systemctl restart lircd`) to pick up the new configuration.  You can test it by using the `irsend` command like below:

```terminal
% irsend SEND_ONCE xbox DISPLAY
```

The above would send the DISPLAY IR code to the xbox.  Your device will have different commands to use.

Once the above is done you will need to update the activity jsons to call the new device.  Please refer to json/example* files for how to format the new commands as well as documentation/json_formate.md.
