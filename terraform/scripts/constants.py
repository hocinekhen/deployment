'''
Created on May 17, 2018

constant defination files

@author: amiwankh
'''

INPUT_FILE_PATH="../../c3po_ngic_input.cfg"
TERRAFORM_VAR_FILE_PATH="../input.tfvars"
HOST_TYPE_FILE_PATH="../host_type.cfg"

TF_FRAME_TYPE="FRAME_TYPE"
FRAME_TYPE="FRAME_TYPE"
FRAME="FRAME"


# Input file constants
INSTANCE_TYPE="INSTANCE_TYPE"
INSTANCE_COUNT="INSTANCE_COUNT"
HOST_TYPE="HOST_TYPE"
INSTANCE_CPU="CPU"
INSTANCE_MEMORY="MEMORY"
INSTANCE_CORE_RANGE="CORE_RANGE"
INSTANCE_DISK="DISK"
NETWORKS="NETWORKS"
NETWORK="NETWORK"

# Variable for optional physical interfaces
S1MME_PHY_DEV_MME="S1MME_PHY_DEVICE"
S1U_PHY_DEVICE_SGWU="S1U_PHY_DEVICE"
SGI_PHY_DEVICE_PGWU="SGI_PHY_DEVICE"
S5S8_PHY_DEVICE_SGWU="SGWU_S5S8_PHY_DEVICE"
S5S8_PHY_DEVICE_PGWU="PGWU_S5S8_PHY_DEVICE"

# Teraform variable for optional physical interfaces
TF_S1MME_PHY_DEV_MME="S1MME_PHY_DEV"
TF_S1U_PHY_DEV_SGWU="SGWU_S1U_PHY_DEV"
TF_SGI_PHY_DEV_PGWU="PGWU_SGI_PHY_DEV"
TF_S5S8_PHY_DEV_SGWU="SGWU_S5S8_PHY_DEV"
TF_S5S8_PHY_DEV_PGWU="PGWU_S5S8_PHY_DEV"

EX_MGMT="EX_MGMT"
MGMT="MGMT"
S1MME="S1MME"
S11="S11"
S6A="S6A"
DB="DB"
S5S8_SGWC="S5S8_SGWC"
S5S8_PGWC="S5S8_PGWC"
FPCNB="FPCNB"
FPCSB="FPCSB"
S1U="S1U"
S5S8_SGWU="S5S8_SGWU"
S5S8_PGWU="S5S8_PGWU"
SGI="SGI"
CTF_RF="CTF"

MME=[S11,S1MME,S6A]
HSS=[DB,S6A]
DB=[DB]
DNS=[MGMT]
SGWC =[S5S8_SGWC,S11,FPCNB]
SPGWC =[S5S8_SGWC,S11,FPCNB]
PGWC=[S5S8_PGWC,FPCNB]
FPC=[FPCSB,FPCNB]
SGWU=[S1U,S5S8_SGWU,FPCSB]
SPGWU=[S1U,SGI,FPCSB]
PGWU=[SGI,S5S8_PGWU,FPCSB]
CTF=[MGMT,CTF_RF]
IL_NPERF=[EX_MGMT,S1U,SGI]

EX_MGMT_IP="EX_MGMT_IP"
MGMT_IP="MGMT_IP"
S1MME_IP="S1MME_IP"
S11_IP="S11_IP"
S6A_IP="S6A_IP"
DB_IP="DB_IP"
S5S8_SGWC_IP="S5S8_SGWC_IP"
S5S8_PGWC_IP="S5S8_PGWC_IP"
FPCNB_IP="FPCNB_IP"
FPCSB_IP="FPCSB_IP"
S1U_IP="S1U_IP"
S5S8_SGWU_IP="S5S8_SGWU_IP"
S5S8_PGWU_IP="S5S8_PGWU_IP"
SGI_IP="SGI_IP"

INSTANCE_SGWC="SGWC"
INSTANCE_SPGWC="SPGWC"
INSTANCE_SPGWU="SPGWU"
INSTANCE_SGWU="SGWU"
INSTANCE_PGWC="PGWC"
INSTANCE_PGWU="PGWU"
INSTANCE_FPC="FPC"
INSTANCE_MME="MME"
INSTANCE_HSS="HSS"
INSTANCE_DB="DB"


INSTANCE_TYPES = [ INSTANCE_SGWC, INSTANCE_SGWU, INSTANCE_PGWC, INSTANCE_PGWU, INSTANCE_FPC, INSTANCE_MME , INSTANCE_HSS, INSTANCE_DB, INSTANCE_SPGWC, INSTANCE_SPGWU ]

MME_CONN=[INSTANCE_HSS,INSTANCE_SGWC]
HSS_CONN=[INSTANCE_MME,INSTANCE_DB]
DB_CONN=[INSTANCE_HSS]
SGWC_CONN=[INSTANCE_MME,INSTANCE_PGWC,INSTANCE_FPC]
PGWC_CONN=[INSTANCE_SGWC,INSTANCE_FPC]
FPC_CONN=[INSTANCE_SGWC,INSTANCE_PGWC]
SGWU_CONN=[INSTANCE_FPC,INSTANCE_PGWU]
PGWU_CONN=[INSTANCE_FPC,INSTANCE_SGWU]

TF_IP_S11_MACVTAP_CP1 = "IP_S11_MACVTAP_CP1"
TF_IP_S11_VM_NGIC_CP1_PCI = "IP_S11_VM_NGIC_CP1_PCI"
TF_IP_S5S8_SGWC_VM_NGIC_CP1_PCI = "IP_S5S8_SGWC_VM_NGIC_CP1_PCI"
TF_IP_S5S8_PGWC_VM_NGIC_CP2_PCI = "IP_S5S8_PGWC_VM_NGIC_CP2_PCI"
TF_IP_ODL_NB_VM_NGIC_CP1_PCI = "IP_ODL_NB_VM_NGIC_CP1_PCI"
TF_IP_ODL_NB_VM_NGIC_CP2_PCI = "IP_ODL_NB_VM_NGIC_CP2_PCI"
TF_IP_ODL_NB_VM_FPC_ODL1_PCI = "IP_ODL_NB_VM_FPC_ODL1_PCI"
TF_IP_ODL_SB_VM_FPC_ODL1_PCI = "IP_ODL_SB_VM_FPC_ODL1_PCI"
TF_IP_ODL_SB_VM_NGIC_DP1_PCI = "IP_ODL_SB_VM_NGIC_DP1_PCI"
TF_IP_ODL_SB_VM_NGIC_DP2_PCI = "IP_ODL_SB_VM_NGIC_DP2_PCI"
TF_IP_S1U_VM_NGIC_DP1_PCI = "IP_S1U_VM_NGIC_DP1_PCI"
TF_IP_S5S8_VM_NGIC_DP1_PCI = "IP_S5S8_VM_NGIC_DP1_PCI"
TF_IP_S5S8_VM_NGIC_DP2_PCI = "IP_S5S8_VM_NGIC_DP2_PCI"
TF_IP_SGI_VM_NGIC_DP2_PCI = "IP_SGI_VM_NGIC_DP2_PCI"
TF_IP_MME_S11_VM_C3PO_MME1_PCI = "IP_MME_S11_VM_C3PO_MME1_PCI"
TF_IP_MME_S1MME_VM_C3PO_MME1_PCI = "IP_MME_S1MME_VM_C3PO_MME1_PCI"
TF_IP_MME_S6_VM_C3PO_MME1_PCI = "IP_MME_S6_VM_C3PO_MME1_PCI"
TF_IP_HSS_S6_VM_C3PO_HSS1_PCI= "IP_HSS_S6_VM_C3PO_HSS1_PCI"
TF_IP_HSS_DB_VM_C3PO_HSS1_PCI="IP_HSS_DB_VM_C3PO_HSS1_PCI"
TF_IP_DBN_HSS_VM_C3PO_DBN1_PCI="IP_DBN_HSS_VM_C3PO_DBN1_PCI"

# Terraform template params for vm count
TF_INSTANCE_COUNT_SGWC="SGWC_VM_COUNT"
TF_INSTANCE_COUNT_SPGWC="SPGWC_VM_COUNT"
TF_INSTANCE_COUNT_SGWU="SGWU_VM_COUNT"
TF_INSTANCE_COUNT_SPGWU="SPGWU_VM_COUNT"
TF_INSTANCE_COUNT_PGWC="PGWC_VM_COUNT"
TF_INSTANCE_COUNT_PGWU="PGWU_VM_COUNT"
TF_INSTANCE_COUNT_FPC="FPC_VM_COUNT"
TF_INSTANCE_COUNT_MME="MME_VM_COUNT"
TF_INSTANCE_COUNT_HSS="HSS_VM_COUNT"
TF_INSTANCE_COUNT_DB="DB_VM_COUNT"

#Terraform template params for CPU count
TF_CPU_COUNT_SGWC="SGWC_CPU"
TF_CPU_COUNT_SPGWC="SPGWC_CPU"
TF_CPU_COUNT_PGWC="PGWC_CPU"
TF_CPU_COUNT_SGWU="SGWU_CPU"
TF_CPU_COUNT_SPGWU="SPGWU_CPU"
TF_CPU_COUNT_PGWU="PGWU_CPU"
TF_CPU_COUNT_FPC="FPC_CPU"
TF_CPU_COUNT_MME="MME_CPU"
TF_CPU_COUNT_FPC="FPC_CPU"
TF_CPU_COUNT_HSS="HSS_CPU"
TF_CPU_COUNT_DB="DB_CPU"

# Terraform template params for CPU CORE details
TF_CORE_RANGE_MME = "CORE_RANGE_MME"
TF_CORE_RANGE_HSS = "CORE_RANGE_HSS"
TF_CORE_RANGE_DB = "CORE_RANGE_DB"
TF_CORE_RANGE_FPC = "CORE_RANGE_FPC"
TF_CORE_RANGE_SGWC = "CORE_RANGE_SGWC"
TF_CORE_RANGE_PGWC = "CORE_RANGE_PGWC"
TF_CORE_RANGE_SPGWC = "CORE_RANGE_SPGWC"
TF_CORE_RANGE_SGWU = "CORE_RANGE_SGWU"
TF_CORE_RANGE_PGWU = "CORE_RANGE_PGWU"
TF_CORE_RANGE_SPGWU = "CORE_RANGE_SPGWU"

# Terraform template params for MEMORY
TF_MEMORY_SGWC="SGWC_MEM"
TF_MEMORY_PGWC="PGWC_MEM"
TF_MEMORY_SPGWC="SPGWC_MEM"
TF_MEMORY_SGWU="SGWU_MEM"
TF_MEMORY_PGWU="PGWU_MEM"
TF_MEMORY_SPGWU="SPGWU_MEM"
TF_MEMORY_FPC="FPC_MEM"
TF_MEMORY_MME="MME_MEM"
TF_MEMORY_HSS="HSS_MEM"
TF_MEMORY_DB="DB_MEM"

# Terraform template params for DISK
TF_DISK_SGWC="SGWC_DISK_SIZE"
TF_DISK_SPGWC="SPGWC_DISK_SIZE"
TF_DISK_SGWU="SGWU_DISK_SIZE"
TF_DISK_SPGWU="SPGWU_DISK_SIZE"
TF_DISK_PGWC="PGWC_DISK_SIZE"
TF_DISK_PGWU="PGWU_DISK_SIZE"
TF_DISK_FPC="FPC_DISK_SIZE"
TF_DISK_MME="MME_DISK_SIZE"
TF_DISK_HSS="HSS_DISK_SIZE"
TF_DISK_DB="DB_DISK_SIZE"
