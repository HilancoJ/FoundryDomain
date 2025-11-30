# Fedora Silverblue Setup Guide

This guide covers the essential steps for setting up **Fedora Silverblue**.  
Including the operating system installation, layering system drivers and installing applications.


## 📜 Table of Contents
- Download and Installation
- GPU Configurations
  - AMD/Intel
  - NVIDIA (Secure Boot Off)
  - NVIDIA (Secure Boot On)
- User Applications


## 📥 Download and Install Fedora Silverblue

1. **Download the ISO:**  
    The latest [Fedora Silverblue ISO](https://fedoraproject.org/atomic-desktops/silverblue/download) image can be downloaded from the official website.

1. **Verify and Create Installation Media:**  
    - Verify the downloaded image [checksum](https://fedoraproject.org/security) and signature to ensure its authenticity.
        - Linux:
            ```bash
            sha256sum Fedora-Silverblue-ostree-*.iso
            ```
        - Windows (Command Prompt):
            ```bash
            certutil -hashfile "Fedora-Silverblue-ostree-*.iso" SHA256
        - Windows (PowerShell):
            ```bash
            Get-FileHash "Fedora-Silverblue-ostree-*.iso" -Algorithm SHA256
            ```
    - Use [Fedora Media Writer](https://docs.fedoraproject.org/en-US/fedora/latest/preparing-boot-media/#_fedora_media_writer) or a similar tool to create a bootable USB drive.

1. **Boot and Install:**  
    - **Boot Mode:** Boot the system in **UEFI mode**. 
    - **Partitioning:** The Fedora installer (Anaconda) provides guided partitioning. Ensure that an **EFI System Partition** (ESP) is created.

1. **Upgrade Base System:**  
    Fetch the latest base image and upgrade all core system packages. A new immutable deployment will be created.
    ```bash
    rpm-ostree upgrade
    ```

1. **Reboot the system to apply the new deployment:**
    ```bash
    systemctl reboot
    ```


## 🚀 GPU Configurations
This section is only required if enhanced GPU capabilities are needed.  
The default GPU drivers are sufficient for most practical purposes. 

1. **Enable RPM Fusion Repositories:**  
    [RPM Fusion](https://rpmfusion.org/) is a community-maintained third-party repository that provides additional software not included in Fedora due to licensing, patent or policy restrictions.  

    Both **Free** and **Non-Free** [repositories](https://rpmfusion.org/Configuration) are required for full codec and hardware support.

    1. **Install RPM Fusion Repositories:**
        ```bash
        rpm-ostree install \
            https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
            https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
        ```

    1. **Reboot the system after installation:**
        ```bash
        systemctl reboot
        ```

1. **Install GPU Drivers:**  
    There are two main graphics stacks required:  
    - **OpenGL:** A mature, widely-supported graphics API suitable for general 3D rendering used by legacy applications.  
    - **Vulkan:** A modern, low-level graphics API that gives applications direct access to GPU hardware. Enabling higher performance, better multi-threading and lower CPU overhead compared to OpenGL.  

    The instructions differ depending on the GPU vendor.

    ---

    - **_AMD / Intel Drivers_:**  
        [Mesa 3D](https://mesa3d.org/) provides the open-source drivers for rendering interactive 3D graphics.  
        - `mesa-dri-drivers` → Provides OpenGL support.  
        - `mesa-vulkan-drivers` → Provides Vulkan support.  
        - `mesa-va-drivers-freeworld` → Enables hardware-accelerated video decoding and encoding for patented codecs.

        Secure Boot is fully compatible because Fedora signs these drivers.

        1. **Install the drivers:**  
            ```bash
            rpm-ostree install mesa-dri-drivers                 # Typically pre-installed.
            ```
            ```bash
            rpm-ostree install mesa-vulkan-drivers              # Typically pre-installed.
            ```
            ```bash
            rpm-ostree install mesa-va-drivers-freeworld
            ```  
        
        1. **Reboot the system after installation:**
            ```bash
            systemctl reboot
            ```

    ---

    - **_NVIDIA Drivers_:**  
        Reference the official RPM Fusion documentation for a full [How To Guide](https://rpmfusion.org/Howto/NVIDIA).  
        - `akmod-nvidia` → Provides the proprietary NVIDIA driver. Including kernel modules, user-space libraries, OpenGL, Vulkan and hardware acceleration.  
        - `xorg-x11-drv-nvidia-cuda` → Adds CUDA and NVDEC/NVENC support. This enables GPU computing and video encoding/decoding acceleration.  

        ⚠️ With Secure Boot enabled, Fedora Silverblue will not load the NVIDIA driver because its kernel module is not signed with a key trusted by the System Firmware (UEFI).  
        The user must do one of the following:
        - Disable Secure Boot
        - Manually sign all NVIDIA kernel modules
        
        Secure Boot enforces that only verified kernel code may run. Protecting against rootkits and persistent kernel-level malware.  
        Although the signing workflow requires additional steps, it is the safer and **recommended** method.

        ---

        - **_NVIDIA: Secure Boot Disabled_:**   
            Simplest method.
            1. **Reboot into UEFI / BIOS settings.**

            2. **Disable Secure Boot in Firmware (UEFI) settings.**

            3. **Boot into Fedora Silverblue.**

            4. **Install the drivers:**  
                ```bash
                # This command will automatically blacklist the open-source 'nouveau' driver.
                rpm-ostree install akmod-nvidia xorg-x11-drv-nvidia-cuda
                ```

            5. **Reboot the system after installation:**  
                ```bash
                systemctl reboot
                ```

        ---

        - **_NVIDIA: Secure Boot Enabled_:** (**💯** recommended)  
            High-level Workflow:   
            1. Install Signing Tools
            1. Generate the Key (`kmodgenca`)
            1. Enroll the Key (`mokutil`)
            1. Install NVIDIA Drivers
            1. Build and Sign Modules (`akmods`)
            1. Verify the Signed Module
            1. Reboot  

            The process is based on the [RPM Fusion Secure Boot](https://rpmfusion.org/Howto/Secure%20Boot) guide.  
            The following packages are required:
            - `akmods` → (Automatic Kernel Module) automatically rebuilds and signs kernel modules when a new kernel is installed. 
            - `kmodgenca` → Automatically generates private key and public certificate pairs used for signing. It is provided by the `akmods` package. 
            - `kmodtool` → Helps create the directory structure, metadata and specification files used for building kernel modules. It is an internal helper used by `akmods`. 
            - `mokutil` → Manages Machine Owner Keys (MOK) for Secure Boot. It allows importing custom keys that the UEFI Firmware will trust. Enabling the system to load signed kernel modules.
            - `openssl` → Provides cryptographic utilities used for generating and managing private keys and certificates. Internal helper used by `kmodgenca`.

            It is important to perform the following steps in sequence:  
            
            1. **Ensure `akmods` is installed.**  
                RPM Fusion repositories installs `akmods`.  
                ```bash
                rpm-ostree db list | grep akmod
                ``` 

            1. **Install the signing tools:**  
                ```bash
                rpm-ostree install kmodtool mokutil openssl
                ```

            1. **Reboot the system after installation:**            
                ```bash
                systemctl reboot
                ```

            1. **Generate a Secure Boot signing key:**   
                ```bash
                sudo kmodgenca -a    
                ```

                This creates:
                ```
                /etc/pki/akmods/private/*-private_key.pem   # Private Key
                /etc/pki/akmods/certs/public_key.der        # Public Certificate (DER for MOK)
                /etc/pki/akmods/certs/public_key.pem        # Public Certificate (PEM)
                /etc/akmods/akmods.conf                     # Tells akmods which key to use
                ```

            1. **Import the public certificate into MOK:**  
                ```bash
                sudo mokutil --import /etc/pki/akmods/certs/public_key.der
                ```
                - Set a password when prompted.
                - The password will be used to enroll the key with the next reboot.
                
                ⚠️ After BIOS/UEFI Firmware updates, the MOK database may be cleared. If that happens, simply re-import the same key using the command above.

            1. **Reboot and enroll the key:** 
                ```bash
                systemctl reboot
                ```
                During boot, the MOK Manager will appear:
                - Choose Enroll MOK
                - Enter the password  
                - Confirm enrollment

            1. **Install NVIDIA drivers:**  
                ```bash
                # This command will automatically blacklist the open-source 'nouveau' driver.
                rpm-ostree install akmod-nvidia xorg-x11-drv-nvidia-cuda
                ```
                The above command will trigger `akmods` to:
                - Build the `nvidia.ko` kernel module.
                - Sign it using the generated key.
                
            1. **Verify that the module is built and signed:**  
                `akmods` compiles modules asynchronously in the background after installation. Typically this process takes between 1-5 minutes.  

                ```bash
                modinfo nvidia | grep -E 'filename|version|signer'
                ```                
                Expected output:  
                - `filename` → Module Exists  
                - `version` → Driver Version  
                - `signer` → Module is signed and valid for Secure Boot  

                If no output appears, the build is still running or failed.  
                Detailed `akmods` build log:
                ```bash
                journalctl -u akmods --no-pager
                ```

            1. **Reboot after the module has been successfully built:**  
                ```bash
                systemctl reboot
                ```

            1. **Verify the NVIDIA driver is loaded and signed:**  
                1. Kernel Module is loaded: 
                    ```bash
                    lsmod | grep nvidia
                    ```
                    If no output appears, the NVIDIA driver did not load and the system is likely using the fallback `nouveau` driver.
                    ```bash
                    lsmod | grep nouveau
                    ```

                1. NVIDIA driver is operational:  
                    Shows the GPU model, driver version and active processes.
                    ```bash
                    nvidia-smi
                    ``` 

                1. Confirm that the module is signed under Secure Boot:
                    ```bash
                    modinfo $(modinfo -n nvidia) | grep signer
                    ```

            1. **Rebuild modules on kernel updates:** (Optional)   
                Whenever kernels update, `akmods` should automatically rebuild the modules and sign them with the created key.  
                If the build fails, rebuild manually:
                ```bash
                sudo akmods --force --rebuild
                ``` 
                ```bash
                sudo rpm-ostree reboot
                ```
    

## 📦 User Applications

1. **Enable the Flathub Repository:**  
    Add the [Flathub](https://flathub.org/en) Repository. It is the primary source for Flatpak applications.

    ```bash
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    ```

1. **Update Existing Flatpak Applications:**  
    Ensure all installed Flatpak applications are up to date.

    ```bash
    flatpak update -y
    ```

1. **Install Applications via Flatpak:**  
    1. Search for an application: (e.g Chrome)

        ```bash
        flatpak search chrome
        ```

    1. Install the application: (e.g Chrome)

        ```bash
        flatpak install flathub com.google.Chrome
        ```

1. **Batch Install Flatpak Apps:**  
    1. Maintain a list of preferred applications in `setup_guide_flatpak_apps.md` using the following format:  
        ```markdown
        - App Name: FlatpakID
        ```

    1. The following command installs all applications listed in that file:

        ```bash
        grep -oE ':[[:space:]]*\S+' setup_guide_flatpak_apps.md | 
            sed 's/^:[[:space:]]*//' | 
            xargs -r flatpak install -y flathub
        ```
        ```bash
        awk -F ':' '/:/ {gsub(/^[ \t]+/, "", $2); print $2}' setup_guide_flatpak_apps.md |
        xargs -r flatpak install -y flathub
        ```