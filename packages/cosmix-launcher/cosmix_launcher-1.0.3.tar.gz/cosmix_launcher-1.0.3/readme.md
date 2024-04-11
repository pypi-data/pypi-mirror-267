# Cosmix

A dead simple CLI-based launcher for Cosmic Reach and Cosmic Quilt.

## Installation

```sh
# Install from PyPI (recommended)
python3 -m pip install cosmix-launcher

# Install from source
git clone https://codeberg.org/emmathemartian/cosmix && cd cosmix
python3 -m pip install -r requirements.txt
python3 -m build
python3 -m pip install ./dist/*.whl

# Test to make sure it's downloaded
python3 -m cosmix version
```

I recommend making an alias to `python3 -m cosmix`. In Zsh you can do this by adding the following to your `.zshrc`:
```zsh
alias cosmix="python3 -m cosmix"
```

On windows download the cosmix.bat file and put it in ```C:\Windows\System32```

**Arch Linux:**
> Arch Linux and it's derivatives may complain with this `error: externally-managed-environment`
>
> To get around this, use the `--user --break-system-packages` options with `pip install`
>
> Obviously this has a chance of breaking something, but in my testing I have yet to have that happen. Though be aware and know that I am not responsible if you break your system.

You may also need to install Maven. On Arch Linux this is just `pacman -S maven`.

## Usage

```
cosmix version
    prints the current installed cosmix version

cosmix debug
    prints a lot of debug information related to cosmix

cosmix add [instance]
    adds and downloads a new instance
    options:
    --version -v VERSION        specify a Cosmic Reach version to use. defaults to "latest"
    --quilt-version -q VERSION  specify a Cosmic Quilt version to use. defaults to "none"
    --display-name -n NAME      optionally specify a display name for the instance

cosmix update [instance]
    updates an existing version
    options:
    --version -v VERSION        specify a Cosimc Reach version to use. defaults to "latest"
    --quilt-version -q VERSION  specify a Cosmic Quilt version to use. defaults to "none"

cosmix instances
    lists all instances

cosmix launch [instance]
    launches an instance

cosmix info [instance]
    prints info about an instance

cosmix add-mod [instance] [path to mod jar]
    adds a mod jar to an instance

cosmix add-crm1-mod [instance] [mod id]
    adds a mod to an instance via CRM-1. To add repos, see ~/.local/share/cosmix/config.hjson

cosmix trash [instance]
    moves an instance to the system's trash folder
```

**Examples**
```sh
# Create an unmodded instance named `vanilla` on the latest CR version
    cosmix add vanilla
# Create a Cosmic Quilt instance named `my-quilt` on the latest CR version with Cosmic Quilt 1.2.7
    cosmix add my-quilt --quilt-version 1.2.7
# Create a vanilla instance named `old-version` on CR 0.0.1
    cosmix add old-version -v 0.0.1
# Install the latest version of Flux API available on JoJoJux's autorepo to the instance `test`
    cosmix add-crm1-mod test dev.crmodders.flux
# Update the `latest` instance to the latest available versions of Cosmic Reach and Cosmic Quilt
    cosmix update latest -v latest -q latest
```

## Folder Structure

Cosmix stores all of its data in your `XDG_DATA_HOME` (typically `~/.local/share/`) on Linux and `%appdata%` on Windows and in the `cosmix` folder.

This folder will contain the following extra folders:
```
cosmix/
    deps/
        cosmic-reach/
            Contains JARs for each downloaded Cosmic Reach version.
    instances/
        example-instance/
            config.json  - Configs for the instance.
    config.hjson - Configs for Cosmix
```
