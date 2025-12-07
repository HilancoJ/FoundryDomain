# Fedora Silverblue Setup Guide

This guide covers the essential steps for setting up **Fedora Silverblue**.  
Including the operating system installation, layering system drivers and installing applications.



## 📜 Table of Contents
- Download and Install Fedora Silverblue
- Enhanced GPU Configurations
  - AMD/Intel Drivers
  - NVIDIA Drivers
- Hardware Monitoring and Cooling
- User Applications



## 📥 Download and Install Fedora Silverblue

1. **Download the ISO:**  
    The latest [Fedora Silverblue ISO](https://fedoraproject.org/atomic-desktops/silverblue/download) image can be downloaded from the official website.

1. **Verify the ISO:**  
    Verify the downloaded image [checksum](https://fedoraproject.org/security) and signature to ensure its authenticity.  
    - Linux:
        ```bash
        sha256sum Fedora-Silverblue-ostree-*.iso
        ```
    - Windows (Command Prompt):
        ```cmd
        certutil -hashfile "Fedora-Silverblue-ostree-*.iso" SHA256
    - Windows (PowerShell):
        ```powershell
        Get-FileHash "Fedora-Silverblue-ostree-*.iso" -Algorithm SHA256
        ```

1. **Create Installation Media**:  
    Use [Fedora Media Writer](https://docs.fedoraproject.org/en-US/fedora/latest/preparing-boot-media/#_fedora_media_writer) or a similar tool to create a bootable USB drive.

1. **Boot the installer:**  
    Boot the system in **UEFI/BIOS** mode and launch the prepared installation media. 

1. **Partitioning:**  
    The Fedora installer provides an automated partitioning option.  
    Alternatively, following these steps for a custom partitioning setup. 
    1. **EFI System Partition:**   
        EFI (Extensible Firmware Interface) stores the bootloader and UEFI firmware entries.
        * Format: `FAT32` (Appears as `efi` in the installer.)
        * Size: 1 GB
        * Mountpoint: `/boot/efi`

    1. **Boot Partition:**  
        Contains the kernel and initramfs. 
        * Format: `ext4`
        * Size: 10 GB
        * Mountpoint: `/boot`

    1. **Operating System:**  
        Holds the immutable OSTree deployment and system subvolumes.
        * Format: `btrfs`
        * Size: Remaining storage.
        * Mountpoint: `/`

    1. **Additional Storage:**  
        Depending on the use case, the following filesystems are available.

        * `btrfs` → Modern CoW (copy-on-write) filesystem supporting **snapshots**, subvolumes, transparent compression, checksums, send/receive and built-in RAID. Excellent for systems that rely on rollback features.

        * `ext2` → A simple legacy filesystem without journaling. Lightweight but mostly obsolete due to the lack of modern reliability features.

        * `ext3` → An ext2-based filesystem with journaling. More reliable than ext2 but slower and largely replaced by ext4.

        * `ext4` → Most common Linux filesystem. Fast, stable, widely supported, low overhead and reliable. Good for external SSDs, servers and general-purpose storage. Does not provide built-in **snapshot** capabilities.

        * `f2fs` → Flash-friendly filesystem optimized for SSDs, SD cards and mobile devices. Offers excellent performance on flash media.

        * `ntfs` → The primary Windows filesystem. Appropriate for external drives that need Windows compatibility. Linux support is provided through drivers, with varying performance.

        * `xfs` → A high-performance filesystem optimized for large files and parallel I/O. Ideal for servers, NAS systems, media processing and large data volumes. It does not support shrinking once created.

1. **Upgrade Base System:**  
    Fetch the latest base image and upgrade all core system packages. A new immutable deployment will be created.
    ```bash
    rpm-ostree upgrade
    ```

1. **Reboot the system to apply the new deployment:**
    ```bash
    systemctl reboot
    ```



## 🚀 Enhanced GPU Configurations
This section is only required if enhanced GPU capabilities are needed.  
The default GPU drivers are sufficient for most practical purposes. 
    
---

**Note:**  
Most OSTree operations such as `rpm-ostree install`, `rpm-ostree upgrade` and `systemctl reboot` do not require `sudo`.  
They automatically elevate privileges when needed.

Commands that modify **kernel modules**, **Secure Boot keys** or **kernel arguments** do require `sudo`, including:
- `mokutil`
- `kmodgenca`
- `akmods`
- `rpm-ostree kargs`
- etc.

---

1. **Enable RPM Fusion Repositories:**  
    [RPM Fusion](https://rpmfusion.org/) is a community-maintained third-party repository that provides additional software not included in Fedora due to licensing, patent or policy restrictions.  

    Both **Free** and **Non-Free** [repositories](https://rpmfusion.org/Configuration) are required for full codec and hardware support.

    1. **Install RPM Fusion Repositories:**
        ```bash
        rpm-ostree install \
            https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
            https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
        ```

    1. **Verify that the new deployment was created:** (Optional)  
        This command can be reused after any major installation step.
        ```bash
        rpm-ostree status
        ```  

        Expected output:  
        - A new deployment entry appears with **(pending)**.
        - `Version` → Current Fedora Silverblue release and revision.
        - `BaseCommit` → OSTree commit hash for the deployed base image.
        - `GPGSignature` → Confirms the deployment is trusted and correctly signed.
        - `LayeredPackages` → Packages layered on top of the immutable base. (e.g. RPM Fusion Repositories)
        - `LocalPackages` → Locally provided RPMs. (e.g. Previously installed helper packages)

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
        - `akmod-nvidia` → Provides the proprietary NVIDIA driver, including kernel modules, user-space libraries, OpenGL, Vulkan and hardware acceleration.  
        - `xorg-x11-drv-nvidia-cuda` → Adds CUDA and NVDEC/NVENC support for GPU computing and video encoding/decoding.     

        ⚠️ [Secure Boot](https://fedoraproject.org/wiki/Secureboot) requires all kernel modules to be signed with a key trusted by the System Firmware (UEFI/BIOS).  
        Since the NVIDIA kernel module is **not** signed by default, Fedora Silverblue will block it when Secure Boot is enabled.  
        To load the driver, the module must be **built and manually signed** with a trusted Machine Owner Key (MOK).
        
        High-level Workflow:   
        1. Install Signing Tools
        1. Generate the Key (`kmodgenca`)
        1. Enroll the Key (`mokutil`)
        1. Install NVIDIA Drivers
        1. Build and Sign Modules (`akmods`)
        1. Verify the Signed Module

        The process is based on the [RPM Fusion Secure Boot](https://rpmfusion.org/Howto/Secure%20Boot) guide.  
        The following packages are required:
        - `akmods` → (Automatic Kernel Module) automatically rebuilds and signs kernel modules when a new kernel is installed. 
        - `kmodgenca` → Automatically generates private key and public certificate pairs used for signing. It is provided by the `akmods` package. 
        - `kmodtool` → Helps create the directory structure, metadata and specification files used for building kernel modules. It is an internal helper used by `akmods`. 
        - `mokutil` → Manages Machine Owner Keys (MOK) for Secure Boot. It allows importing custom keys that the UEFI Firmware will trust. Enabling the system to load signed kernel modules.
        - `openssl` → Provides cryptographic utilities used for generating and managing private keys and certificates. Internal helper used by `kmodgenca`.

        It is important to perform the following steps **in sequence**:  

        1. **Install the signing tools:**  
            ```bash
            rpm-ostree install akmods
            ```
            ```bash
            rpm-ostree install kmodtool
            ```
            ```bash
            rpm-ostree install mokutil      # Typically pre-installed.
            ```
            ```bash
            rpm-ostree install openssl      # Typically pre-installed.
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
            ```bash
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
            
            ⚠️ After UEFI/BIOS Firmware updates, the MOK database may be cleared. If that happens, simply re-import the same key using the command above.

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
            rpm-ostree install akmod-nvidia xorg-x11-drv-nvidia-cuda
            ```

        1. **Reboot to apply the new deployment:**  
            🛠️ Booting into the new deployment will trigger `akmods` to:
            - Build the `nvidia.ko` kernel module.
            - Sign it using the generated key.

            ```bash
            systemctl reboot
            ```
            
        1. **Verify that the NVIDIA module has been built:**  
            `akmods` compiles modules asynchronously in the background.  
            This usually takes **1-5 minutes** after the first boot into the new deployment.  
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

        1. **Reboot again after the NVIDIA module has been built:**  
            This ensures the newly built NVIDIA module loads correctly.
            ```bash
            systemctl reboot
            ```

        1. **Verify the NVIDIA driver is loaded and signed:**  
            1. **Check that the Kernel Module is loaded:** 
                ```bash
                lsmod | grep nvidia
                ```
                
                If no output appears, the NVIDIA driver did **not** load and the system is still using the fallback `nouveau` driver.  
                ```bash
                lsmod | grep nouveau
                ```
                
                If `nouveau` is active, the NVIDIA driver cannot load.  
                Verify that all prior steps completed successfully:  
                - The Secure Boot key was enrolled
                - `akmods` built the NVIDIA module
                - The system booted into the updated deployment
                
                The NVIDIA kernel module **must** load before proceeding.

            1. **Confirm the NVIDIA driver is operational:**  
                Shows the GPU model, driver version and active processes.
                ```bash
                nvidia-smi
                ``` 

                Although `akmods` already blacklists the open-source `nouveau` driver, it is recommended to manually apply the blacklist.  
                This will guarantee that `nouveau` stays disabled across all future deployments. 
                ```bash
                sudo rpm-ostree kargs --append=modprobe.blacklist=nouveau   # Disable Module.
                sudo rpm-ostree kargs --append=nouveau.modeset=0            # Disable KMS (Kernel Mode Setting) fallback.
                systemctl reboot
                ```

        1. **Rebuild modules on kernel updates:** (Optional)   
            Whenever kernels update, `akmods` should automatically rebuild the modules and sign them with the created key.  
            If the build fails, rebuild manually:
            ```bash
            sudo akmods --force --rebuild
            ``` 
            ```bash
            systemctl reboot
            ```



## ❄️ Hardware Monitoring and Cooling





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
        awk -F ':' '/:/ {gsub(/^[ \t]+/, "", $2); print $2}' setup_guide_flatpak_apps.md |
        xargs -r flatpak install -y flathub
        ```