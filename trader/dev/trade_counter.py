import csv
from collections import Counter

def count_trades(csv_data):
    """Count buy and sell trades from CSV data."""
    reader = csv.DictReader(csv_data.splitlines())
    trade_counts = Counter("buy" if float(row["amount"]) > 0 else "sell" for row in reader)
    return trade_counts

# Example usage
csv_data = """txid,refid,time,type,subtype,aclass,asset,wallet,amount,fee,balance,amountusd
LFWBMP-6KB4V-XXC6PU,TQBES7-AENPX-HHJ3J5,2025-01-01 16:33:06,trade,,currency,USD,spot / main,-979.3789,0,0.0000,-979.38
LYS6X3-MM4LQ-2PDAZX,TQBES7-AENPX-HHJ3J5,2025-01-01 16:33:06,trade,,currency,ADA,spot / main,1103.62749009,2.42798095,1101.19950914,1015.78
LRIK7D-4VESV-W3PUGM,TDW225-ELY6T-MNQCGP,2025-01-01 18:57:09,trade,,currency,ADA,spot / main,-550.59975457,0,550.59975457,-506.77
LOBFPX-6GBUW-XIULVQ,TDW225-ELY6T-MNQCGP,2025-01-01 18:57:09,trade,,currency,USD,spot / main,506.5518,1.1144,505.4374,506.55
LXOJTZ-ZNTBK-KGMIFW,TSS7WM-JANXS-MHQDGD,2025-01-01 19:08:18,trade,,currency,ADA,spot / main,-550.59975457,0,0.00000000,-506.77
LBM5AC-GMJGN-DSOVAL,TSS7WM-JANXS-MHQDGD,2025-01-01 19:08:18,trade,,currency,USD,spot / main,510.1896,1.1224,1014.5046,510.19
LYLQLQ-47CLI-SBEYLZ,TCT2XJ-7U5D4-RRYAFQ,2025-01-01 19:44:39,trade,,currency,USD,spot / main,-1014.5046,0,0.0000,-1014.50
LYEXCZ-NBPK3-2R34WH,TCT2XJ-7U5D4-RRYAFQ,2025-01-01 19:44:39,trade,,currency,ADA,spot / main,1108.60886337,2.43893937,1106.16992400,1020.36
LWKJWI-EEFXU-MM4AQK,TP65P4-QAJB2-D2IM4F,2025-01-01 20:33:29,trade,,currency,ADA,spot / main,-1106.16992400,0,.00000000,-1018.12"""

print(count_trades(csv_data))

