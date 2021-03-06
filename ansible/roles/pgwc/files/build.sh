#!/bin/bash
cd $(dirname ${BASH_SOURCE[0]})
SERVICE=3
CPUS=${CPUS:-$(nproc)}
SGX_SERVICE=0
SERVICE_NAME="Collocated CP and DP"
source ./services.cfg
export NGIC_DIR=$PWD
echo "------------------------------------------------------------------------------"
echo " NGIC_DIR exported as $NGIC_DIR"
echo "------------------------------------------------------------------------------"

HUGEPGSZ=`cat /proc/meminfo  | grep Hugepagesize | cut -d : -f 2 | tr -d ' '`
MODPROBE="/sbin/modprobe"
INSMOD="/sbin/insmod"
DPDK_DOWNLOAD="https://fast.dpdk.org/rel/dpdk-18.02.tar.gz"
DPDK_DIR=$NGIC_DIR/dpdk
LINUX_SGX_SDK="https://github.com/intel/linux-sgx.git"
LINUX_SGX_SDK_BRANCH_TAG="sgx_1.9"
CP_NUMA_NODE=0
DP_NUMA_NODE=0

install_libs()
{
    echo "Install libs needed to build and run NGIC..."
    sudo apt-get update
    sudo apt-get -y install curl build-essential linux-headers-$(uname -r) \
         git unzip libpcap0.8-dev gcc libjson0-dev make libc6 libc6-dev \
         g++-multilib libzmq3-dev libcurl4-openssl-dev libssl-dev cmake python-pip
    sudo pip install zmq
}
download_hyperscan()
{
    source /etc/os-release
    if [[ $VERSION_ID != "16.04" ]] ; then
        echo "Download boost manually "$VERSION_ID
        wget http://sourceforge.net/projects/boost/files/boost/1.58.0/boost_1_58_0.tar.gz
        tar -xf boost_1_58_0.tar.gz
        pushd boost_1_58_0
        sudo apt-get -y install g++
        ./bootstrap.sh --prefix=/usr/local
        ./b2
        ./b2 install
        popd
    else
        sudo apt-get -y install libboost-all-dev
    fi
    echo "Downloading HS and dependent libraries"
    sudo apt-get -y install cmake ragel
    wget https://github.com/01org/hyperscan/archive/v4.1.0.tar.gz
    tar -xvf v4.1.0.tar.gz
    pushd hyperscan-4.1.0
    mkdir build; pushd build
    cmake -DCMAKE_CXX_COMPILER=c++ ..
    make -j $CPUS install
    popd; popd;
}
download_dpdk_zip()
{
    echo "Download DPDK zip"
    wget --no-check-certificate "${DPDK_DOWNLOAD}"
    if [ $? -ne 0 ] ; then
        echo "Failed to download dpdk submodule."
        return
    fi
    tar -xzvf "${DPDK_DOWNLOAD##*/}"
    rm -rf "$NGIC_DIR"/dpdk/
    rm -f "${DPDK_DOWNLOAD##*/}"
    mv "$NGIC_DIR"/dpdk-*/ "$NGIC_DIR"/dpdk

    echo ""
    echo "Applying AVX not supported patch for resolved dpdk-18.02 i40e driver issue.."
    patch -d $DPDK_DIR -p1 < $NGIC_DIR/patches/v2-net-i40e-fix-avx2-driver-check-for-rx-rearm.diff
    if [ $? -ne 0 ] ; then
        echo "Failed to apply AVX patch, please check the errors."
        return
    fi

    echo "AVX patch successfully applied to dpdk."

}

install_dpdk()
{
    echo "Build DPDK"
    export RTE_TARGET=x86_64-native-linuxapp-gcc
    cp -f dpdk-18.02_common_linuxapp "$DPDK_DIR"/config/common_linuxapp

    pushd "$DPDK_DIR"
#        make -j 10 install T="$RTE_TARGET"
    make -j $CPUS install T="$RTE_TARGET"
    if [ $? -ne 0 ] ; then
        echo "Failed to build dpdk, please check the errors."
        return
    fi

    if lsmod | grep rte_kni >&/dev/null; then
        echo -e "\n*************************************"
        echo "rte_kni.ko module already loaded..!!!"
        echo -e "*************************************\n"
    else
        sudo $INSMOD "$RTE_TARGET"/kmod/rte_kni.ko

        if lsmod | grep rte_kni >&/dev/null; then
            echo -e "\n*********************************"
            echo "Inserted 'rte_kni.ko' module..!!!"
            echo -e "*********************************\n"
        else
            echo -e "\n**********************************************"
            echo "ERROR: 'rte_kni.ko' module failed to load..!!!"
            echo -e "**********************************************\n"
        fi

    fi

    sudo modinfo igb_uio
    if [ $? -ne 0 ] ; then
        sudo $MODPROBE -v uio
        sudo $INSMOD "$RTE_TARGET"/kmod/igb_uio.ko
        sudo cp -f "$RTE_TARGET"/kmod/igb_uio.ko /lib/modules/"$(uname -r)"
        echo "uio" | sudo tee -a /etc/modules
        echo "igb_uio" | sudo tee -a /etc/modules
        sudo depmod
    fi
    popd
}

configure_services()
{
    echo ""
    opt=$1
    case $opt in
        cp) echo "Control Plane Settings"
            SERVICE=1
            SERVICE_NAME="CP"
            recom_memory=1024
            memory=`cat config/cp_config.cfg  | grep "MEMORY=" | head -n 1 | cut -d '=' -f 2`
            setup_numa_node
            setup_hugepages
            return;;

        dp) echo "Data Plane Setting"
            SERVICE=2
            SERVICE_NAME="DP"
            recom_memory=4096
            memory=`cat config/dp_config.cfg  | grep "MEMORY=" | head -n 1 | cut -d '=' -f 2`
            setup_numa_node
            download_hyperscan
            setup_hugepages
            return;;

        cpdp) echo "Control and Data Plane Setting"
              SERVICE=3
              SERVICE_NAME="Collocated CP and DP"
              setup_collocated_memory
              setup_hugepages
              return;;

        *) echo
           echo "Please select appropriate option."
           echo ;;
    esac

}
setup_numa_node()
{
    if [ `cat config/cp_config.cfg  | grep "NUMA0_MEMORY=0" | wc -l` != 0 ]; then
        CP_NUMA_NODE=1
    fi
    if [ `cat config/dp_config.cfg  | grep "NUMA0_MEMORY=0" | wc -l` != 0 ]; then
        DP_NUMA_NODE=1
    fi
}


setup_collocated_memory()
{

    dp_memory=`cat config/dp_config.cfg  | grep MEMORY | cut -d = -f 2 | tr -d ' '`
    cp_memory=`cat config/cp_config.cfg  | grep MEMORY | cut -d = -f 2 | tr -d ' '`
    memory=$(($cp_memory + $dp_memory))
}

setup_hugepages()
{
    Pages=16
    cp_pages=8
    dp_pages=8
    echo "SERVICE_NAME=\"$SERVICE_NAME\" " > ./services.cfg
    echo "SERVICE=$SERVICE" >> ./services.cfg
    echo "SGX_SERVICE=$SGX_SERVICE" >> ./services.cfg
    echo "CP_NUMA_NODE=$CP_NUMA_NODE" >> ./services.cfg
    echo "DP_NUMA_NODE=$DP_NUMA_NODE" >> ./services.cfg
    if [[ "$HUGEPGSZ" = "2048kB" ]] ; then
        #---- Calculate number of pages base on configure MEMORY and page size
        Hugepgsz=`echo $HUGEPGSZ | tr -d 'kB'`
        Pages=$((($memory*1024) / $Hugepgsz))
        if [ $SERVICE == 3 ] ; then
            cp_pages=$((($cp_memory*1024) / $Hugepgsz))
            dp_pages=$((($dp_memory*1024) / $Hugepgsz))
        fi
        echo "MEMORY (MB) : " $memory
        echo "Number of pages : " $Pages
    fi
    case $SERVICE in
        [1]) echo "Control Plane NUMA memory Settings"
             echo "$Pages" > /sys/devices/system/node/node$CP_NUMA_NODE/hugepages/hugepages-$HUGEPGSZ/nr_hugepages
             echo "CP_NUMA_PAGES=$Pages" >> ./services.cfg
             echo "DP_NUMA_PAGES=0" >> ./services.cfg
             return;;
        [2]) echo "Data Plane NUMA memory Settings"
             echo "$Pages" > /sys/devices/system/node/node$DP_NUMA_NODE/hugepages/hugepages-$HUGEPGSZ/nr_hugepages
             echo "DP_NUMA_PAGES=$Pages" >> ./services.cfg
             echo "CP_NUMA_PAGES=0" >> ./services.cfg
             return;;

        [3]) echo "Control and Data Plane NUMA memory Settings"
             if [ $CP_NUMA_NODE == $DP_NUMA_NODE ] ; then
                 echo "$Pages" > /sys/devices/system/node/node$CP_NUMA_NODE/hugepages/hugepages-$HUGEPGSZ/nr_hugepages
                 echo "CP_NUMA_PAGES=$Pages" >> ./services.cfg
                 echo "DP_NUMA_PAGES=$Pages" >> ./services.cfg
             else
                 echo "$cp_pages" > /sys/devices/system/node/node$CP_NUMA_NODE/hugepages/hugepages-$HUGEPGSZ/nr_hugepages
                 echo "$dp_pages" > /sys/devices/system/node/node$DP_NUMA_NODE/hugepages/hugepages-$HUGEPGSZ/nr_hugepages
                 echo "CP_NUMA_PAGES=$cp_pages" >> ./services.cfg
                 echo "DP_NUMA_PAGES=$dp_pages" >> ./services.cfg
             fi
             return;;
        *) echo
           echo "Invalid service configuration."
           echo ;;
    esac

    sudo service procps start
    grep -s '/dev/hugepages' /proc/mounts
    if [ $? -ne 0 ] ; then
        echo "Creating /mnt/huge and mounting as hugetlbfs"
        sudo mkdir -p /mnt/huge
        sudo mount -t hugetlbfs nodev /mnt/huge
        echo "nodev /mnt/huge hugetlbfs defaults 0 0" | sudo tee -a /etc/fstab > /dev/null
    fi

}
download_linux_sgx()
{
    echo "Download Linux SGX SDK....."
    git clone --branch $LINUX_SGX_SDK_BRANCH_TAG $LINUX_SGX_SDK
    if [ $? -ne 0 ] ; then
        echo "Failed to clone Linux SGX SDK, please check the errors."
        return
    fi
}

build_ngic()
{
    pushd $NGIC_DIR
    source setenv.sh
    make -j $CPUS clean
    if [ $SERVICE == 2 ] || [ $SERVICE == 3 ] ; then
        echo "Building DP..."
        make -j $CPUS WHAT="dp" || { echo -e "\nDP: Make failed\n"; }
    fi
    if [ $SERVICE == 1 ] || [ $SERVICE == 3 ] ; then
        echo "Building CP..."
        make -j $CPUS WHAT="cp" || { echo -e "\nCP: Make failed\n"; }
    fi
    popd
}

install_libs
download_dpdk_zip
install_dpdk
if [ "$SGX_SERVICE" -eq 1 ] ; then
    download_linux_sgx
    export SGX_BUILD=1
else
    export SGX_BUILD=0
fi
configure_services $1
build_ngic

