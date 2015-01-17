# SQUIRT #
Squirt started as an attempt to provide a simple way of maintain frequently used simple FTP scripts. The FTP functionality is far from complete but I have expanded the scope a little with the aim of developing a simple mechanism for managing scripts across a variety of protocols. In the longer term, I have also been thinking in terms of coming up with a mechanism for piping these scripts together.

## An incomplete list of dependencies ##
Squirt requires Python3 and includes the following dependencies:
- SQLite
- ftplib
- smtplib

## Using Squirt ##
Everything is done via the `squirt` command. Full help should be provided and can be accessed by entering `squirt [command] --help`

The core of this is pretty straightforward. You use `squirt build` to define (build) a communication script, using the available options to specify whatever details need to be saved. Once this is done you can use `squirt exec` to execute the script. The `exec` command allows for the same options as `build` - all of these are optional and, if used, will allow you temporarily override the values defined in `build`.

A `copy` command is also available. This will create a new script (ct = copy to) based on an existing script (cf = copy from). Again, this command allows for the same options as `build` - if entered, these will be applied to the new script.
 
## Currently supported FTP Actions ##
The --do option on the build and exec commands defines the action to be performed. At present, the following actions are supported:
- chmod-xxx   Changes the access permissions of the file.
              This action is in two parts, split by a single -
              The first part of the command is the chmod
              The second part is the access permissions to apply
- del         Delete files matching the pattern described by `--files`
- get         Retrieves files matching the pattern described by `--files`. 
- ls          List files matching the pattern described by `--files`
- put         Puts files matching the pattern described by `--files` to server. 
- tree        Returns a directory starting at the `--remote` folder

More will be added as and when I get around to it.

## Currently supported SMTP Action ##
There is only one SMTP action - sending email - so SMTP scripts ignore the --do option. Files matching the pattern described by `--files` are sent to the `--mailto` address.
