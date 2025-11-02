# Fedora Silverblue Setup Guide

This guide covers the essential steps for setting up **Fedora Silverblue**.  
Including the operating system installation, layering system drivers and installing applications.

## 📥 Download and Install Fedora

1. **Download the ISO**  
    Obtain the latest [Fedora Silverblue ISO](https://fedoraproject.org/atomic-desktops/silverblue/download) image from the the official website.

1. **Verify and Create Installation Media**  
    - Verify the downloaded image checksum and signature to ensure its authenticity.
    - Use [Fedora Media Writer](https://docs.fedoraproject.org/en-US/fedora/latest/preparing-boot-media/#_fedora_media_writer) or a similar tool to create a bootable USB drive.

1. **Boot and Install**  
    - **Boot Mode**:  
     Boot the system in **UEFI mode**. If Secure Boot is enabled, note that third-party drivers such as the NVIDIA proprietary driver may require disabling Secure Boot or manually signing kernel modules.
    - **Partitioning**:  
     The Fedora installer (Anaconda) provides guided partitioning.  
     Ensure that an **EFI System Partition** (ESP) is created.


## ⚙️ System Setup

1. **Upgrade Base System**  
    Fetch the latest base image and upgrade all core system packages. A new immutable deployment will be created.

    ```bash
    rpm-ostree upgrade
    ```

    Reboot the system to apply the new deployment.

    ```bash
    systemctl reboot
    ```

1. **Enable RPM Fusion Repositories**  
    [RPM Fusion](https://rpmfusion.org/) is a community-maintained, third-party repository for Fedora.  
    It provides additional software not included in Fedora due to licensing, patent or policy restrictions.  
    The repositories enable access to additional packages such as proprietary drivers (NVIDIA) and multimedia codecs.  

    Both **Free** and **Non-free** [repositories](https://rpmfusion.org/Configuration) are required for full hardware and codec support.

    ```bash
    rpm-ostree install \
        https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
        https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
    ```

    Reboot the system after installation.

    ```bash
    systemctl reboot
    ```

1. **Install GPU Drivers**  
 Provided that RPM Fusion Repositories are active, install the required hardware drivers.  
 There are two main packages required:  
 **OpenGL**: A mature, widely-supported graphics API suitable for general 3D rendering used by legacy applications.  
 **Vulkan**: A modern, low-level graphics API that gives applications direct access to GPU hardware. Enabling higher performance, better multi-threading and lower CPU overhead compared to OpenGL.  

    - **_AMD / Intel Drivers_**:  
     [Mesa 3D](https://mesa3d.org/) provides the open-source drivers for rendering interactive 3D graphics.  
     `mesa-vulkan-drivers` provides OpenGL and Vulkan support.  
     `mesa-va-drivers-freeworld` enables hardware-accelerated video decoding and encoding for patented codecs which are not included in the default Fedora distribution.

        ```bash
        # Expected to be pre-installed. Run the command to confirm.
        rpm-ostree install mesa-vulkan-drivers
        ```
        ```bash
        # Installed from RPM Fusion repository.
        rpm-ostree install mesa-va-drivers-freeworld
        ```
        
        Reboot the system after installation.

        ```bash
        systemctl reboot
        ```

    - **_NVIDIA Drivers_**:  
     Reference the official RPM Fusion website for full [How To Guide](https://rpmfusion.org/Howto/NVIDIA).  
     `akmod-nvidia` provides the proprietary NVIDIA driver. Including kernel modules, user-space libraries, OpenGL, Vulkan and hardware acceleration.  
     `xorg-x11-drv-nvidia-cuda` adds CUDA and NVDEC/NVENC support to the NVIDIA driver stack. This enables GPU computing and video encoding/decoding acceleration.  

        ```bash
        # This command will automatically blacklist the open-source 'nouveau' driver.
        rpm-ostree install akmod-nvidia xorg-x11-drv-nvidia-cuda
        ```
    
        Reboot the system after installation.
        
        ```bash
        systemctl reboot
        ```

        Quick GPU Driver Check.  
        After installing GPU drivers, especially with Secure Boot enabled. It is useful to confirm whether the kernel module has successfully loaded.

        ```bash
        lsmod | grep nvidia

        # If no output appears, the NVIDIA driver did not load, and the system is likely using the fallback 'nouveau' driver.
        lsmod | grep nouveau
        ```


## 📦 User Applications

1. **Enable the Flathub Repository**  
    Add the [Flathub](https://flathub.org/en) Repository. It is the primary source for Flatpak applications.

    ```bash
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    ```

1. **Update Existing Flatpak Applications**  
    Ensure all installed Flatpak applications are up to date.

    ```bash
    flatpak update -y
    ```

1. **Install Applications via Flatpak**  
    - Search for an application. (e.g Chrome)

        ```bash
        flatpak search chrome
        ```

    - Install the application. (e.g Chrome)

        ```bash
        flatpak install flathub com.google.Chrome
        ```

1. **Batch Install Flatpak Apps**  
    Maintain a list of preferred applications in `setup_guide_flatpak_apps.md` using the following format:  
    ```markdown
    - App Name: FlatpakID
    ```

    The following command installs all applications listed in that file:

    ```bash
    grep -oE ':[[:space:]]*\S+' setup_guide_flatpak_apps.md | 
        sed 's/^:[[:space:]]*//' | 
        xargs -r flatpak install -y flathub
    ```