# Updated version of https://hub.docker.com/r/vtajzich/ipxe using Alpine Linux
#
# Create demo.ipxe file with the following lines:
#   #!ipxe
#   dhcp
#   chain http://boot.ipxe.org/demo/boot.php
#
# Create a custom undionly.kpxe image by running the following command:
#   docker run -it -v $(pwd):/custom-pxe -e PXE_FILE=demo.ipxe ipxe-alpine
#
# Source: https://ipxe.org/scripting
#

# https://hub.docker.com/_/alpine
FROM ubuntu:focal

# https://github.com/ipxe/ipxe/tags
ENV IPXE="v1.21.1"

WORKDIR /opt

# Install APK Packages
# Source: https://ipxe.org/download
ARG DEBIAN_FRONTEND=noninteractive
#ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y \
    build-essential \
    binutils \
    make \
    perl \
    liblzma-dev \
    mtools \
    genisoimage \ 
    isolinux \
    git

# Download latest iPXE software and compile
RUN git config --global advice.detachedHead false
RUN git clone --depth 1 --branch $IPXE git://git.ipxe.org/ipxe.git

# Add more menu items and features
# Source: https://ericdraken.com/cluster-computer-gotchas/#ipxe-menu
RUN cd ipxe/src && echo "\
\n#define DOWNLOAD_PROTO_HTTPS\
\n#define IMAGE_TRUST_CMD\
\n\
\n#undef  NET_PROTO_IPV6\
" >> config/local/general.h

# Disable iPXE USB since we are booting over the Network
# Source: https://ericdraken.com/cluster-computer-gotchas/#ipxe-usb
RUN cd ipxe/src && echo "\
\n#undef  USB_HCD_XHCI\
\n#undef  USB_HCD_EHCI\
\n#undef  USB_HCD_UHCI\
\n#undef  USB_KEYBOARD\
\n#undef  USB_BLOCK\
\n#undef  USB_EFI\
" >> config/local/usb.h

# Shorten the watchdog timeout from 5 minutes to 1 minute
# interface/efi/efi_watchdog.c
# #define WATCHDOG_TIMEOUT_SECS ( 5 * 60 )
# Source: https://ericdraken.com/cluster-computer-gotchas/#watchdog
RUN cd ipxe/src && sed -i -E 's|^#define\s+WATCHDOG_TIMEOUT_SECS.+$|#define WATCHDOG_TIMEOUT_SECS 60|' interface/efi/efi_watchdog.c &&\
    grep -q -E '^#define WATCHDOG_TIMEOUT_SECS 60' interface/efi/efi_watchdog.c

RUN cd ipxe/src && make

# Create undionly.kpxe files using the docker run command 
RUN mkdir /custom-pxe
COPY make-undionly.sh .
RUN chmod +x make-undionly.sh
CMD ["/opt/make-undionly.sh"]
