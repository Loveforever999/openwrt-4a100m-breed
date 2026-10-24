#!/usr/bin/env python3
"""把小米 4A 百兆的 DTS 分区表改成 Breed 布局（firmware @ 0x50000）。"""
import glob
import sys

files = glob.glob(
    "openwrt/target/linux/ramips/dts/*xiaomi_mi-router-4a-100m.dts"
)
if not files:
    sys.exit("找不到 DTS 文件")
path = files[0]
print("目标文件:", path)

BREED = """partitions {
			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			partition@0 {
				label = "u-boot";
				reg = <0x0 0x30000>;
				read-only;
			};

			partition@30000 {
				label = "u-boot-env";
				reg = <0x30000 0x10000>;
			};

			factory: partition@40000 {
				label = "factory";
				reg = <0x40000 0x10000>;
				read-only;
			};

			partition@50000 {
				label = "firmware";
				reg = <0x50000 0xfb0000>;
			};
		};"""

src = open(path, encoding="utf-8").read()

start = src.index("partitions {")
i = start + len("partitions {")
depth = 1
while depth > 0:
    if src[i] == "{":
        depth += 1
    elif src[i] == "}":
        depth -= 1
    i += 1
while src[i] != ";":
    i += 1
i += 1

src = src[:start] + BREED + src[i:]
open(path, "w", encoding="utf-8").write(src)
print("已替换分区表:")
print(BREED)
