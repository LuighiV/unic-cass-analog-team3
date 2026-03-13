Project template for analog flow
================================


This is based on the project template developed for Chipathon 2025 by Jianxun
Zhu. Here the files are adapted to the technology used in UNIC CASS 2025 which
is IHP.

Update repositories
-------------------

We have used several repositories as submodules. We need to initialize them:

```
git submodule update --init --recursive
```


Running using X-server (default, official)
------------------------------------------

To start working with it please run:

```
make start
```
Place an .env file in the root repository to setup the options. Could use the
following as example:

```
DOCKER_USER=isaiassh
DOCKER_TAG=1.0.7
```

Running using VNC server (under development)
--------------------------------------------

Use the following command:
```
make start-vnc
```

Place an .env file in the root repository to setup the options. Could use the
following as example:

```
DOCKER_USER=luighiv
ENABLE_GUI=1
WEBSERVER_PORT=80
VNC_PORT=5901
JUPYTER_PORT=8888
DOCKER_TAG=1.0.7_vnc
```

The shared directory is the subfolder `designs` so all the development is self
contained in the repository.

Setting up the workspace
------------------------

Need to copy the .bashrc to setup the environment:

```
cp .config/.bashrc ~/.bashrc
source .config/.bashrc
```

Launching the tools
-------------------

To launch the xschem we can use:

```
xschem &
```

To include support for IOs (developed by Manuel Monge @manuel-monge) we can
use:

```
MMIO=1 xschem &
```

To launch klayout we can use:


```
klayout &
```
