# Phoque2
This is an evolution of the [Phoque](https://github.com/Timst/Phoque) system, focused on decoupling various functionalities of the original one.

## Wait so what is this?
You can read the other's repo readme for more details, but the TL;DR is that this is a queuing system that I created for my Burning Man camp, Crêpiphany. At most camps, people have to line up and wait to receive a camp's offering, sometimes for hours on end. This is highly unpleasant. With Phoque, people can get a ticket, sit down, and wait to be called.

It works like this:
- Guests walk up to a big arcade push button, press it, and the system takes a picture and print it (along with a number) on a receipt printer
- When ready, we can call numbers by pressing another button on our side
- Meanwhile, a screen shows the current number and expected wait time

## So what was wrong with v1

Phoque v1 ran everything from the same RPI, which created some logistical headache: for example, we would have liked the guest button to be at the front of the camp, while the calling button are by the cooking station, but that just wasn't easily feasible. For the number screen, we used a wireless HDMI thing, but that was rickety as hell. And then the client/server model used for said screen was also ridiculous. This is an attempt to make this a cleaner, fully distributed system. Diagram:

<img src="./Phoque_schema.png" width="1200"/>

## Architecture

The new system is a **monorepo with 5 independent packages** that can be installed separately on different Raspberry Pis:

### Components

- **phoque-shared**: Shared types and models (minimal dependencies - just pydantic)
- **phoque-server**: REST API server with database and admin logic
- **phoque-button**: GPIO button + camera + printer client
- **phoque-backoffice**: Backoffice client for calling numbers and displaying the state of the line
- **phoque-display**: LED matrix display + audio announcements

### Installation

Each component can be installed independently:

```bash
# Install shared types first (required by all others)
pip install git+https://github.com/Timst/Phoque2.git#subdirectory=phoque-shared

# Install server on main Pi
pip install git+https://github.com/Timst/Phoque2.git#subdirectory=phoque-server

# Install button client on guest-facing Pi
pip install git+https://github.com/Timst/Phoque2.git#subdirectory=phoque-button

# Install backoffice on calling station Pi
pip install git+https://github.com/Timst/Phoque2.git#subdirectory=phoque-backoffice

# Install display on screen Pi
pip install git+https://github.com/Timst/Phoque2.git#subdirectory=phoque-display
```

### Running

Each component provides a CLI command:

```bash
phoque-server      # Start the REST API server
phoque-button      # Run button/camera/printer client
phoque-backoffice  # Run backoffice client
phoque-display     # Run display/audio client
```

### Development

For local development, install all packages in editable mode:

```bash
pip install -e ./phoque-shared -e ./phoque-server -e ./phoque-button -e ./phoque-backoffice -e ./phoque-display
```

The Pi units will be linked to one another with CAT6 cables, which will provide both power (using a PoE switch) and a data link.